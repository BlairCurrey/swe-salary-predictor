import datetime as dt
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder


def log(f):
    def wrapper(df, *args, **kwargs):
        start = dt.datetime.now()
        result = f(df, *args, **kwargs)
        stop = dt.datetime.now()
        print(f'{f.__name__}:\n  runtime={stop - start}, end shape={result.shape}')
        return result
    return wrapper

class DataLoader:
    def __init__(self, path):
        self.encodings = {}
        self.counts = {'US': 0, 'UK': 0}
        self.last_location = {'US': '', 'UK': ''}
        self.df = self.get_df(path)

    def get_df(self, path):
        df_raw = pd.read_csv(path)
        return (df_raw
            .pipe(self._start_pipeline)
            .pipe(self._select)
            .pipe(self._clean)
            .pipe(self._remove_outliers)
            .pipe(self._handle_missing)
            .pipe(self._drop)
        )

    @log
    def _start_pipeline(self, df):
        return df.copy()

    @log
    def _select(self, df):
        # drop everything without the label and if not employed full time
        df = df.dropna(subset=['ConvertedCompYearly'])
        df = df[df['Employment'] == 'Employed full-time']

        df = df[[ # select our columns
            'ConvertedCompYearly',
            'EdLevel',
            'Age1stCode',
            'YearsCode',
            'YearsCodePro',
            # 'OrgSize', # TODO: implement or remove
            'Country',
            # 'US_State', # TODO: implemented ohe or remove
            # 'UK_Country', # TODO: implemented ohe or remove
            # 'DevType', # TODO: implemented ohe or remove
            # 'LanguageHaveWorkedWith', # TODO: implemented ohe or remove
            'Age'
        ]]

        return df

    @log
    def _clean(self, df):
        years_map = { 'Less than 1 year': '0.5', 'More than 50 years': '51' }
        df = df.replace({
            'YearsCode': years_map, 
            'YearsCodePro': years_map,
            'Age': {
                'Under 18 years old': 17,
                '18-24 years old': 20,
                '25-34 years old': 29.5,
                '35-44 years old': 39.5,
                '45-54 years old': 49.5,
                '55-64 years old': 59.5,
                '65 years or older': 65
            },
            'EdLevel': {
                'Some college/university study without earning a degree': 'Less than Associates',
                'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)': 'Less than Associates',
                'Something else': 'Less than Associates',
                'Primary/elementary school': 'Less than Associates',
                'Associate degree (A.A., A.S., etc.)': 'Associates',
                'Bachelor’s degree (B.A., B.S., B.Eng., etc.)': 'Bachelors',
                'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)': 'Masters',
                'Other doctoral degree (Ph.D., Ed.D., etc.)': 'Doctorate',
                'Professional degree (JD, MD, etc.)': 'Doctorate',
            },
            'Age1stCode': {
                'Younger than 5 years': 4,
                '5 - 10 years': 7.5,
                '11 - 17 years': 14,
                '18 - 24 years': 21,
                '25 - 34 years': 28.5,
                '35 - 44 years': 39.5,
                '45 - 54 years': 49.5,
                '55 - 64 years': 59.5,
                'Older than 64 years': 65
            }
        })
        # replace Age > 'Prefer not to say' and nan with mean
        df = df.replace({'Age': {'Prefer not to say': np.nan}})
        df['Age'] = df[['Age']].fillna(df['Age'].mean(skipna=True))

        # encode EdLevel
        df['EdLevel'] = df[['EdLevel']].fillna(df['EdLevel'].mode()[0])
        oe = OrdinalEncoder(categories=[['Less than Associates', 'Associates', 
                                        'Bachelors', 'Masters', 'Doctorate']])
        df['EdLevel'] = oe.fit_transform(df['EdLevel'].values.reshape(-1,1))
        self.encodings['EdLevel'] = self._encoder_map(oe)

        # TODO: change to ohe or remove
        # convert country and state (if any for UK/US)
        # to compound location and one-hot-enconde
        # df['Location'] = (df[['Country', 'US_State', 'UK_Country']]
        #     .fillna('')
        #     .apply(lambda row: self._get_location_name(row), axis=1)
        # )

        # TODO: one-hot-encode these lists or remove
        # DevType - WIP turns ; delimited list into python list
        # df['DevType'] = df[['DevType']].fillna('missing')
        # # change dev type list string to list and get all unique values
        # df['DevType'] = df['DevType'].apply(lambda x: x.split(';'))
        # dev_types = df["DevType"].explode().unique()
        # # encode dev types and apply to each list
        # le.fit(dev_types)
        # df['DevType'] = df['DevType'].apply(lambda x: x.split(';'))

        # TODO: one-hot-encode these lists or remove
        # LanguageHaveWorkedWith - WIP

        # one hot encode Country
        df['Country'] = df[['Country']].fillna('missing')
        df = self._get_ohe_df(df, ['Country'])

        # convert string numbers to numbers
        string_numbers = ['YearsCode', 'YearsCodePro', 'Age']
        df[string_numbers] = df[string_numbers].apply(pd.to_numeric)
        df = df.round(2)

        return df

    @log 
    def _remove_outliers(self, df):
        # df = df[(np.abs(stats.zscore(df['ConvertedCompYearly'])) < .25)]
        df = df[df['ConvertedCompYearly'] <= 300000]
        df = df[df['ConvertedCompYearly'] >= 15000]

        # remove countries below a certain threshold of records
        df = df[df['Country'].map(df['Country'].value_counts()) > 100]

        return df

    @log
    def _handle_missing(self, df):
        df['YearsCode'] = df[['YearsCode']].fillna(df['YearsCode'].mean(skipna=True))
        df['YearsCodePro'] = df[['YearsCodePro']].fillna(df['YearsCodePro'].mean(skipna=True))
        df['Age1stCode'] = df[['Age1stCode']].fillna(df['Age1stCode'].mean(skipna=True))

        # fill other encoded values with "missing"

        return df

    def _drop(self, df):
        return df.drop(['Country'], axis=1)

    def _encoder_map(self, encoder):
        # returns map of labels to encoded values - helpful for inspecting
        # return dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))
        return [dict(enumerate(mapping)) for mapping in encoder.categories_][0]
    
    def _get_location_name(self, row):
        if row['Country'] == 'United States of America':
            return 'US_' + row['US_State']
        elif row['Country'] == 'United Kingdom of Great Britain and Northern Ireland':
            return 'UK_' + row['UK_Country']
        else:
            return row['Country']
    
    def _get_ohe_df(self, df, columns):
        ohe = OneHotEncoder()
        feature_arr = ohe.fit_transform(df[columns]).toarray()
        feature_labels = np.array(ohe.categories_).ravel()
        df_features = pd.DataFrame(feature_arr, columns=feature_labels)

        # for c in columns:
        #     self.encodings[c] = self._encoder_map(ohe)

        df.reset_index(drop=True, inplace=True)
        df_features.reset_index(drop=True, inplace=True)
        df = pd.concat([df, df_features], axis=1)

        return df