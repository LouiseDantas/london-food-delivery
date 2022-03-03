import numpy as np
import pandas as pd
from pathlib import Path
from leads.utils import return_paretto,haversine,match_restaurant

PACKAGE_DIR = Path(__file__).parent.parent

class Leads:

    def __init__(self,city):
        self.city=city

    def load_data(self):
        foodagency_path=PACKAGE_DIR.joinpath(f'UKFoodAgency{self.city}.csv')
        self.df=pd.read_csv(foodagency_path)
        self.df=self.df.reset_index(drop=True)
        return

    def clean_data(self):
        self.df=self.df.rename(columns={"PostCode": "postcode"})
        self.df['Geocode.Longitude']=pd.to_numeric(self.df['Geocode.Longitude'],downcast='float')
        self.df['Geocode.Latitude']=pd.to_numeric(self.df['Geocode.Latitude'],downcast='float')
        self.df=self.df.rename(columns={"Geocode.Latitude": "latitude", "Geocode.Longitude": "longitude"})
        self.df['latlon']=self.df.apply(
            lambda row: str(round(row['latitude'],4))+str(round(row['longitude'],4)),
            axis=1)
        self.df['latlon'] = self.df['latlon'].astype(str)
        self.df=self.df.drop(columns=['Unnamed: 0'])
        return

    def merge_df(self,uber_df):
        self._col_to_merge='latlon'
        self.in_common=self.df.merge(uber_df,how='inner',on=[self._col_to_merge])
        return

    def gross_leads(self):
        list_incommon=self.in_common[self._col_to_merge]
        self.not_uber=self.df[~self.df[self._col_to_merge].isin(list_incommon)].copy()
        self.hot_leads=self.not_uber
        return

    def get_chains(self,cut_off):
        self.not_uber
        chains_count=pd.DataFrame(self.hot_leads['BusinessName'].value_counts())
        chains_count=chains_count[chains_count['BusinessName']>cut_off]

        chains_list=chains_count.reset_index()['index'].values.tolist()

        self.hot_leads=self.hot_leads[self.hot_leads['BusinessName'].isin(chains_list)]
        return self.hot_leads,chains_count

    def top_categories(self,uber_df,group_col='merchant_category',sum_col='reviews_count',threshold_=80):
        cat_most_ordered=pd.DataFrame(uber_df.groupby([group_col])[sum_col].sum())
        (cat_most_ordered,most_ordered_list)=return_paretto(cat_most_ordered,group_col,sum_col,threshold_)
        business_list=self.in_common[self.in_common[group_col].isin(most_ordered_list)]['BusinessType'].unique()
        self.hot_leads=self.hot_leads[self.hot_leads['BusinessType'].isin(business_list)]
        return

    def nearby(self,uber_df,min_dist):
        test=self.hot_leads
        test=test.dropna(subset=['latitude','longitude'])
        uber_df=uber_df.dropna(subset=['latitude','longitude'])
        test['nearby_uber']=test.apply(lambda row: match_restaurant(uber_df,row['latitude'], row['longitude'],min_dist), axis=1)
        test=test[test['nearby_uber']!='nomatch']
        test['Uber_closest_rest'], test['distance_km'] = test['nearby_uber'].str
        test=test.drop(columns=['nearby_uber'])
        return test
