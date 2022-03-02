import numpy as np
import pandas as pd
from pathlib import Path

PACKAGE_DIR = Path(__file__).parent.parent

class Leads:

    def __init__(self,city):
        self.city=city

    def load_data(self):
        foodagency_path=PACKAGE_DIR.joinpath(f'UKFoodAgency{self.city}.csv')
        self.df=pd.read_csv(foodagency_path)
        self.df=self.df.reset_index(drop=True)
        return self.df

    def clean_data(self):
        self.df=self.df.rename(columns={"PostCode": "postcode"})
        self.df['Geocode.Longitude']=pd.to_numeric(self.df['Geocode.Longitude'],downcast='float')
        self.df['Geocode.Latitude']=pd.to_numeric(self.df['Geocode.Latitude'],downcast='float')
        self.df=self.df.rename(columns={"Geocode.Latitude": "latitude", "Geocode.Longitude": "longitude"})
        self.df['latlon']=self.df.apply(
            lambda row: str(round(row['latitude'],4))+str(round(row['longitude'],4)),
            axis=1)
        return self.df

    def merge_df(self,uber_df):
        self._col_to_merge='latlon'
        self.in_common=self.df.merge(uber_df,on=[self._col_to_merge])
        return

    def gross_leads(self):
        list_incommon=self.in_common[self._col_to_merge]
        self.not_uber=self.df[~self.df[self._col_to_merge].isin(list_incommon)].copy()
        return

    def get_chains(self,cut_off):
        self.not_uber
        chains_count=pd.DataFrame(self.not_uber['BusinessName'].value_counts())
        chains_count=chains_count[chains_df['BusinessName']>cut_off]

        chains_list=chains_count.reset_index['index'].values.tolist()

        chains_lead=self.not_uber[self.not_uber['BusinessName'].isin(chains_list)]
        return chains_lead,chains_count
