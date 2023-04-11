import sys
sys.path.append('E:/tool/venv\Lib\site-packages')
import pandas as pd
from pycaret.classification import *


import warnings
warnings.filterwarnings('ignore')


pd.set_option('display.max_columns', None)


def execute():

    df = pd.read_parquet('E:/tool\src\media/projects/data/2023/01/23/ola.csv.parquet', engine='pyarrow')
    df.columns = df.columns.str.upper()
    # my padas data frame

    df = df.drop(['UNNAMED: 0'], axis=1)

    df = df.dropna() 

    df['RATING'] = 4

    df['MMM-YY'] = pd.to_datetime(df['MMM-YY'])

    df['DATEOFJOINING'] = pd.to_datetime(df['DATEOFJOINING'])

    df['GENDER'].fillna(0, inplace=True)

    df['GENDER'] = df['GENDER'].astype(str)

    s = setup(data = df, target ='GENDER', silent=True)
    best = compare_models()
    save_model(best, 'best_model')
execute()
www.neuralnexus.cloud,neuralnexus.cloud