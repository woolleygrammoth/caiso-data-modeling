from setup import generate_dates, get_df_old, get_df_new, set_dt_index_old, set_dt_index_new, file_name_from_date
from web_actions import download_net_demand
import pandas as pd
import os
import time
import datetime

start = '06/02/2022'
end = '06/02/2022'
dates = generate_dates(start, end)

for date in dates: 
    log = './scraped-data/download_logs.txt'
    with open(log, 'r') as f: 
        contents = f.read()
    # if date not already logged
    if date not in contents: 
        # download net demand for date into daily folder
        download_net_demand(date)
        time.sleep(2) #give the download time
        # open day_csv in daily folder & set its index
        file_name = file_name_from_date(date)
        df = get_df_new(file_name, path='./scraped-data/daily/')
        day_df = set_dt_index_new(df, date)
        # open master_csv in ./scraped-data with index_col="Timestamp"
        master_df = pd.read_csv('./scraped-data/caiso-net-demand.csv', index_col="Timestamp")
        # concatenate daily csv to master csv 
        master_df = pd.concat([master_df, day_df])
        # master_df.drop_duplicates(subset='Timestamp', inplace=True)
        # overwrite the master csv
        master_df.to_csv('./scraped-data/caiso-net-demand.csv')
        # log the action to download_logs.txt
        with open(log, 'a') as f: 
            f.write(date + '\n')
        # delete this particular file with os.remove()
        os.remove('./scraped-data/daily/' + file_name)
