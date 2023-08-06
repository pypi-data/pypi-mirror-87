#!/usr/local/bin/python3
import requests
import pandas as pd
import os

def download_csv(source_data, zoom = 'regioni'):
    r = requests.get(source_data.replace('placeholder', zoom))
    url_content = r.content
    txt_file = open('last_update_{}.txt'.format(zoom), 'wb')
    txt_file.write(url_content)
    txt_file.close()
    read_file = pd.read_csv('last_update_{}.txt'.format(zoom))
    read_file.to_csv('last_update_{}.csv'.format(zoom))
    df = pd.read_csv('last_update_{}.csv'.format(zoom))

    os.remove('last_update_{}.txt'.format(zoom)) 
    
    return df