import pandas as pd
import numpy as np
import pickle

class Encodings:
    def __init__(self, encodings_pickle_str):
        encodings = pickle.loads(encodings_pickle_str)
        self.dev_type_mlb = encodings["dev_type_mlb"]
        self.languages_mlb = encodings["languages_mlb"]
        self.ed_level_oe = encodings["ed_level_oe"]
        self.country_ohe = encodings["country_ohe"]
    
    def get_labels(self):
        return {
            "countries": self.country_ohe.categories_[0],
            "dev_types": self.dev_type_mlb.classes_,
            "languages": self.languages_mlb.classes_,
            "ed_levels": self.ed_level_oe.categories_[0]
        }

    def make_input(self, input_dict):
        df_input = pd.DataFrame(data={
            "EdLevel": [input_dict["ed_level"]], # will be transformed inplace below when encoded
            "Age1stCode": [input_dict["age_first_code"]],
            "YearsCode": [input_dict["years_code"]],
            "YearsCodePro": [input_dict["years_code_pro"]],
            "Age": [input_dict["age"]],
        })
        # encode Country
        country_enc = self.country_ohe.transform(pd.DataFrame(
            data={"Country": [input_dict["country"]]})).toarray()
        df = self.merge_ohe(df_input, self.country_ohe, country_enc)

        # encode Devtype
        dev_type_enc = self.dev_type_mlb.transform(pd.Series([input_dict["dev_type"]]))
        df = self.merge_mlb(df, self.dev_type_mlb, dev_type_enc)

        # encode LanguageHaveWorkedWith
        languages_enc = self.languages_mlb.transform(pd.Series([input_dict["languages"]]))
        df = self.merge_mlb(df, self.languages_mlb, languages_enc)

        # encode Edlevel
        df['EdLevel'] = self.ed_level_oe.transform(df['EdLevel'].values.reshape(-1,1))

        return df.values

    def merge_ohe(self, df, ohe, feature_arr):
        feature_labels = np.array(ohe.categories_).ravel()
        df_features = pd.DataFrame(feature_arr, columns=feature_labels)
        df.reset_index(drop=True, inplace=True)
        df_features.reset_index(drop=True, inplace=True)
        df = pd.concat([df, df_features], axis=1)
        return df

    def merge_mlb(self, df, mlb, encoded):
        return df.join(pd.DataFrame(encoded, columns=mlb.classes_, index=df.index))