import os
import pandas as pd
from pathlib import Path
import requests
from pandas import json_normalize


PACKAGE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = PACKAGE_DIR.joinpath('raw_data')
FILES_DIR = PACKAGE_DIR.joinpath('files')

def get_save_data(city:str):
    page=1
    url = f"http://ratings.food.gov.uk/search/^/{city}/{page}/30/json"
    response=requests.get(url).json()

    page_count=int(response['FHRSEstablishment']['Header']['PageCount'])

    df=json_normalize(response['FHRSEstablishment']['EstablishmentCollection']['EstablishmentDetail'])
    for page in range(1,page_count):
        #url = f"http://ratings.food.gov.uk/search/^/{city}/{page}/30/json"
        response = requests.get(url).json()
        df_iter = json_normalize(response['FHRSEstablishment']['EstablishmentCollection']['EstablishmentDetail'])
        df=pd.concat([df, df_iter], axis= 0)
    df.to_csv(f'/home/louisedantas/code/LouiseDantas/competitor-analysis/UKFoodAgency{city}.csv')
