import re
import warnings
from math import radians, cos, sin, asin, sqrt

def get_postcode(fulladdress):
    try:
        postcode=re.search(r'[A-Z][A-Z][0-9]\s[0-9][A-Z][A-Z]', fulladdress).group(0)
    except Exception:
        postcode= 'nomatch'
        try:
            postcode=re.search(r'[A-Z][A-Z][0-9][0-9]\s[0-9][A-Z][A-Z]', fulladdress).group(0)
        except Exception:
            postcode= 'nomatch'
            try:
                postcode=re.search(r'[A-Z][0-9]\s[0-9][A-Z][A-Z]', fulladdress).group(0)
            except Exception:
                postcode= 'nomatch'
                try:
                    postcode=re.search(r'[A-Z][0-9][0-9]\s[0-9][A-Z][A-Z]', fulladdress).group(0)
                except Exception:
                    postcode= 'nomatch'
                    try:
                        postcode=re.search(r'[A-Z][0-9][A-Z]\s[0-9][A-Z][A-Z]', fulladdress).group(0)
                    except Exception:
                        postcode= 'nomatch'
                        try:
                            postcode=re.search(r'[A-Z][A-Z][0-9][A-Z]\s[0-9][A-Z][A-Z]', fulladdress).group(0)
                        except Exception:
                            postcode= 'nomatch'
                            try:
                                postcode=re.search(r'\s[A-Z][A-Z][0-9][0-9]', fulladdress).group(0)
                            except Exception:
                                postcode= 'nomatch'
                                try:
                                    postcode=re.search(r'\s[A-Z][A-Z][0-9]', fulladdress).group(0)
                                except Exception:
                                    postcode= 'nomatch'
                                    try:
                                        postcode=re.search(r'\s[A-Z][0-9][0-9]', fulladdress).group(0)
                                    except Exception:
                                        postcode= 'nomatch'

    return postcode

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def return_paretto(df,column_name,column_name_sum,threshold):
    #df is a grouped dataframe

    grouped_df=df
    grouped_df=grouped_df.rename(columns={column_name_sum: "count"})
    grouped_df=grouped_df.reset_index().sort_values(by=['count'],ascending=False).reset_index(drop=True)

    total=grouped_df['count'].sum()
    grouped_df['percentage']=(grouped_df['count']/total)*100

    index_paretto=grouped_df['percentage'].cumsum().searchsorted(threshold)
    paretto_list=grouped_df[column_name][0:index_paretto+1].values.tolist()
    return grouped_df, paretto_list

def match_restaurant(uber_df,lat, long,min_dist=0.005):
    distances = uber_df.apply(
        lambda row: haversine(lat, long, float(row['latitude']), float(row['longitude'])),
        axis=1)
    closest=distances.min()
    if closest>min_dist:
        return 'nomatch'
    else:
        return uber_df.loc[distances.idxmin(), 'name'],closest
