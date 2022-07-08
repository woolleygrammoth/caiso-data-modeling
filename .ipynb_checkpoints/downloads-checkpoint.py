from setup import generate_dates, get_df_old, get_df_new, set_dt_index_old, set_dt_index_new, file_name_from_date
from web_actions import download_net_demand
import pandas as pd
import os
import time
import datetime

start = '04/10/2018'
end = '04/10/2018'

for date in generate_dates(start, end): 
    log = 'scraped-data/download_logs.txt'
#     with open(log, 'r') as f: 
#         contents = f.read()
#     # if date not already logged
#     if date not in contents: 
        # download net demand for date into daily folder
    download_net_demand(date)
    time.sleep(2) #give the download time
        # open day_csv in daily folder & set its index
    file_name = file_name_from_date(date)
    df = get_df_old(file_name, path='./scraped-data/daily/')
    today_df = set_dt_index_old(df, date)
        # master_df = pd.read_csv('./scraped-data/caiso-net-demand.csv', index_col="Timestamp")
        # concatenate daily csv to master csv 
        # master_df = pd.concat([master_df, day_df])
        # master_df.drop_duplicates(subset='Timestamp', inplace=True)
        # overwrite the master csv
    today_df.to_csv('./scraped-data/caiso-net-demand.csv')

    # delete current file from downloads
    with open(log, 'a') as f: 
        f.write(date + '\n')
    os.remove('./scraped-data/daily/' + file_name)
