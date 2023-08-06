import pandas as pd
import numpy as np

# Takes in data_path (must be .csv, .txt, or .gz) and returns pandas dataframe
def load_data(data_path):
    if data_path[-1] == 't':
        return pd.read_csv(data_path, sep='\t')
    elif data_path[-1] == 'v':
        return pd.read_csv(data_path, sep=',')
    elif data_path[-1] == 'z':
        return pd.read_csv(data_path, sep='\t', compression='gzip')
    else:
        raise Exception('Unrecognized File Type')

# Removes specified features from dataframe
def remove_features(df, feature_names):
    for feature in feature_names:
        if not col_exists(df, feature):
            continue
        df = df.drop(columns=[feature])
    return df



########################################
# Error Checking
def col_exists(df,feature_name,raise_exception=False):
    try:
        df[feature_name]
        return True
    except:
        if raise_exception:
            raise Exception('Unable to access '+str(feature_name)+': column does not exist')
        else:
            print('Unable to access '+str(feature_name)+': column does not exist')
            return False
