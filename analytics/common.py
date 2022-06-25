import datetime as dt
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MultiLabelBinarizer

RAW_DATASET_LABELS = ["ResponseId","MainBranch","Employment","Country","US_State","UK_Country","EdLevel","Age1stCode","LearnCode","YearsCode","YearsCodePro","DevType","OrgSize","Currency","CompTotal","CompFreq","LanguageHaveWorkedWith","LanguageWantToWorkWith","DatabaseHaveWorkedWith","DatabaseWantToWorkWith","PlatformHaveWorkedWith","PlatformWantToWorkWith","WebframeHaveWorkedWith","WebframeWantToWorkWith","MiscTechHaveWorkedWith","MiscTechWantToWorkWith","ToolsTechHaveWorkedWith","ToolsTechWantToWorkWith","NEWCollabToolsHaveWorkedWith","NEWCollabToolsWantToWorkWith","OpSys","NEWStuck","NEWSOSites","SOVisitFreq","SOAccount","SOPartFreq","SOComm","NEWOtherComms","Age","Gender","Trans","Sexuality","Ethnicity","Accessibility","MentalHealth","SurveyLength","SurveyEase","ConvertedCompYearly"]

def log(f):
    def wrapper(df, *args, **kwargs):
        start = dt.datetime.now()
        result = f(df, *args, **kwargs)
        stop = dt.datetime.now()
        print(f'{f.__name__}:\n  runtime={stop - start}, end shape={result.shape}')
        return result
    return wrapper

class DataLoader:
    salary_min = 15_000
    salary_max = 300_000

    def __init__(self, df=None, path=None):
        self.encodings = {}
        self.counts = {'US': 0, 'UK': 0}
        self.last_location = {'US': '', 'UK': ''}
        self.is_path_loaded = path is not None

        self._check_load_args(df, path)
        
        self.df = self.get_df(df=df) if df is not None else self.get_df(path=path)

    def _check_load_args(self, df=None, path=None):
        if df is None and path is None:
            raise ValueError('Must provide path or df')

    def get_df(self, df=None, path=None):
        self._check_load_args(df, path)

        df_raw =  df if df is not None else pd.read_csv(path)
        return (df_raw
            .pipe(self._start_pipeline)
            .pipe(self._select)
            .pipe(self._clean)
            .pipe(self._remove_outliers)
            .pipe(self._handle_missing)
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
            'Country',
            'DevType',
            'LanguageHaveWorkedWith',
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
            },
        })
        # replace Age > 'Prefer not to say' and nan with mean
        df = df.replace({'Age': {'Prefer not to say': np.nan}})
        df['Age'] = df[['Age']].fillna(df['Age'].mean(skipna=True))

        # fill missing
        df['EdLevel'] = df[['EdLevel']].fillna(df['EdLevel'].mode()[0])
        df['DevType'] = df[['DevType']].fillna('MissingDevType')
        df['LanguageHaveWorkedWith'] = (df[['LanguageHaveWorkedWith']]
            .fillna('MissingLanguageHaveWorkedWith'))
        df['Country'] = df[['Country']].fillna('missing')

        # convert string numbers to numbers
        string_numbers = ['YearsCode', 'YearsCodePro', 'Age']
        df[string_numbers] = df[string_numbers].apply(pd.to_numeric)
        df = df.round(2)

        return df

    @log 
    def _remove_outliers(self, df):
        # df = df[(np.abs(stats.zscore(df['ConvertedCompYearly'])) < .25)]
        df = df[df['ConvertedCompYearly'] <= self.salary_max]
        df = df[df['ConvertedCompYearly'] >= self.salary_min]

        # remove countries below a certain threshold of records,
        # but not if DataLoader is being used to make a new input
        if(self.is_path_loaded):
            df = df[df['Country'].map(df['Country'].value_counts()) > 100]

        return df

    @log
    def _handle_missing(self, df):
        df['YearsCode'] = df[['YearsCode']].fillna(df['YearsCode'].mean(skipna=True))
        df['YearsCodePro'] = df[['YearsCodePro']].fillna(df['YearsCodePro'].mean(skipna=True))
        df['Age1stCode'] = df[['Age1stCode']].fillna(df['Age1stCode'].mean(skipna=True))
        return df