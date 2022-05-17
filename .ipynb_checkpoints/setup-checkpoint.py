import datetime
import os
import pandas as pd

def correct_format(date): 
    """checks whether the date has the correct format MM/DD/YYYY"""
    format = '%m/%d/%Y'
    res = True
    try:
        res = bool(datetime.datetime.strptime(date, format))
    except ValueError:
        res = False
    return res

def generate_dates(start: str, end: str) -> list: 
    """
    generates a list of stringified dates in MM/DD/YYYY format, endpoints inclusive
    """
    assert correct_format(start) and correct_format(end), "dates must be in MM/DD/YYYY format"
    start = datetime.datetime.strptime(start, "%m/%d/%Y")
    end = datetime.datetime.strptime(end, "%m/%d/%Y")
    dates_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days + 1)]
    string_dates = list(map(lambda date: datetime.datetime.strftime(date, "%m/%d/%Y"), dates_generated))
    return string_dates

def file_name_from_date(date:str)->str: 
    assert correct_format(date), 'date must be in MM/DD/YYYY format'
    year = date[-4:]
    month = date[:2]
    day = date[3:5]
    return f'CAISO-netdemand-{year}{month}{day}.csv'

def get_df_old(file:str, path:str='') -> pd.DataFrame: 
    """
    produces a formatted dataframe from the csv at the destination path/file
    works from 04/10/2018-08/16/2021 - after that the format changes
    """
    if path: 
        file = path + file
    raw = pd.read_csv(file, sep='delimiter', engine='python')

    def rows_as_key_value(row, delete_first=False): 
        """
        returns: [key_name, [values]] for this particular row. 
        necessary for the last row of the raw csv due to an error in the formatting of the csv
        """
        split = lambda string: string.split(',')
        series = list(map(split, row))[0]
        if delete_first: 
            series = series[1:]
        key = series.pop(0)
        return [key, series]

    data = {}
    columns = [raw.columns, raw.iloc[0], raw.iloc[1], raw.iloc[2]]
    for i in range(len(columns)): 
        key, value = rows_as_key_value(columns[i], delete_first=(i==3))
        data.update({key: value})

    df = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in data.items() ])).iloc[:-1, :] # skip last row - 00:00 of next day
    return df

def get_df_new(file:str, path:str='')-> pd.DataFrame: 
    if path: 
        file = path + file
    df = pd.read_csv(file).iloc[:, :-1].transpose()
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df.drop("Day-ahead net forecast", axis=1, inplace=True)
    return df

def set_dt_index_old(df:pd.DataFrame, date:str)->pd.DataFrame:
    index = list(map(lambda x: datetime.datetime.strptime(date + ' ' + x, "%m/%d/%Y %H:%M"), list(df.iloc[:, 0])))
    df.index=pd.DatetimeIndex(index)
    df.drop("Net Demand " + date, axis=1, inplace=True)
    df.index.names = ['Timestamp']
    return df

def set_dt_index_new(df:pd.DataFrame, date:str)->pd.DataFrame:
    index = list(map(lambda x: datetime.datetime.strptime(date + ' ' + x, "%m/%d/%Y %H:%M"), list(df.index)))
    df.index=pd.DatetimeIndex(index)
    df.index.names = ['Timestamp']
    return df
 

if __name__ == '__main__': 
    #setup the first download as formatted csv in ./scraped-data. 
    # all subsequent ones will be appended in downloads.py
    path = './scraped-data/daily/'
    csv = os.listdir(path)[1]
    df = get_df_old(csv, path)
    df = set_dt_index(df, "04/10/2018")
    df.to_csv('./scraped-data/caiso-net-demand.csv')
