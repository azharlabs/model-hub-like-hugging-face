import sys
sys.path.append('E:/tool/venv\Lib\site-packages')
import pandas as pd


pd.set_option('display.max_columns', None)


def dataframe():

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
    df = df.head(5)

    return list(df.columns), list(df.values)

print(dataframe())
