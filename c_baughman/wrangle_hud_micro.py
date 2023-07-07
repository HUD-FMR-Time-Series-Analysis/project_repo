# wrangle_hud_micro.py

import numpy as np
import pandas as pd
import os
import requests
from env import hud_token
from datetime import datetime
#========================================================


# the list of desired hud entities
entity_ids = ['METRO41700M41700']



# a function to get the current list of years for hud

def get_year_list():
    '''
    This function creates a list of years beginning with 2018 up to one year before the
    current year. 2018 correlates to the first year that HUD MSA Small Area data was available
    so that starting point is fixed. The function adds a new year at the end of the calendar year. 
    HUD generally publishes new rates in September for implementation with the Federal Fiscal Year 
    which begins October 1st of year prior. This lag to the start of the calendar year gives time 
    to sure that the database is updated before adding the next year to the query. As the HUD API 
    uses a different query format for current year, this list will not include the current year as
    that is not specified to default to the current year
    
    Arguments: None
    
    Returns: A list of years from 2018 to present.
    '''
    start_year = 2018  # desired starting year
    current_year = datetime.now().year

    year_range = list(range(start_year, current_year + 1))
    
    return year_range

def resample_hud_data(df):
    '''
    This function takes in a dataframe of hud fmr rates and resamples it to monthly data by forward filling and then shifting backwards by three months to align with the federal fiscal year.
    
    Arguments: a dataframe of fmr data
    
    Returns: a resampled dataframe of fmr data
    '''
    df['date'] = pd.to_datetime(df.year)
    df.set_index('date', inplace=True)
    # shift the fmr rates backwards by three months to reflect federal fiscal year
    df = df.resample('M').ffill().shift(periods=-3, freq='M')
    # format date index as strings for alignment with retail rent dataframe
    df.index = df.index.strftime('%Y-%m')
    
    return df
    

# a function to get hud fmr data for an entity_id such as an MSA code

def get_entity_data(entity_id):
    '''
    This function takes in a single HUD entity (in this case Metropolitan Statistical Area)
    and requests the Fair Market Rent Small Area Data for that entity for the current year. This current year response is converted to a .json and then a DataFrame and then
    each prior is queried and and concatenated to the original df. Requires a HUD API User Token
    which can be acquired here: https://www.huduser.gov/portal/dataset/fmr-api.html
    Entity_ids can be found here: https://www.huduser.gov/portal/datasets/geotools.html
    
    Arguments: a HUD entity id
    
    Returns: a DataFrame of Fair Market Rent rates for each ZIP code in entity
    '''
    header = {'Authorization': f'Bearer {hud_token}'}

    years = get_year_list()
    df = pd.DataFrame()

    for year in years:
        url = f'https://www.huduser.gov/hudapi/public/fmr/data/{entity_id}?year={year}'
        response = requests.get(url, headers=header)
        data = response.json()
        dum = pd.DataFrame(data['data']['basicdata'])
        dum['year'] = data['data']['year']
        dum['entity_id'] = entity_id
        dum['area_name'] = data['data']['area_name']
        df = pd.concat([df, dum])
        
    df_monthly = pd.DataFrame()
    zip_codes = df.zip_code.unique().tolist()
    for zip_code in zip_codes:
        df_zip = df[df.zip_code == zip_code]
        future = pd.DataFrame({'year':[str(int(datetime.now().year)+1)], 'zip_code':[zip_code]})
        df_zip = pd.concat([df_zip, future], ignore_index=True)
        df_zip = resample_hud_data(df_zip)
        df_monthly = pd.concat([df_monthly, df_zip])
    
    # convert index to datetime format
    df_monthly.index = pd.to_datetime(df_monthly.index)   

    return df_monthly


def get_yearly_entity_data(entity_id):
    '''
    This function takes in a single HUD entity (in this case Metropolitan Statistical Area)
    and requests the Fair Market Rent Small Area Data for that entity for the current year. This current year response is converted to a .json and then a DataFrame and then
    each prior is queried and and concatenated to the original df. Requires a HUD API User Token
    which can be acquired here: https://www.huduser.gov/portal/dataset/fmr-api.html
    Entity_ids can be found here: https://www.huduser.gov/portal/datasets/geotools.html
    
    Arguments: a HUD entity id
    
    Returns: a DataFrame of Fair Market Rent rates for each ZIP code in entity
    '''
    header = {'Authorization': f'Bearer {hud_token}'}

    years = get_year_list()
    df = pd.DataFrame()

    for year in years:
        url = f'https://www.huduser.gov/hudapi/public/fmr/data/{entity_id}?year={year}'
        response = requests.get(url, headers=header)
        data = response.json()
        dum = pd.DataFrame(data['data']['basicdata'])
        dum['year'] = data['data']['year']
        dum['entity_id'] = entity_id
        dum['area_name'] = data['data']['area_name']
        df = pd.concat([df, dum])
        
    return df


# a parent function to get entity_ids for a list of hud entity_ids.
def new_hud_micro_data(entity_ids = entity_ids):
    '''
    This function takes in a list of HUD entities (in this case Metropolitan Statistical Areas)
    and requests the Fair Market Rent
    Small Area Data using the HUD API for each entity in the entity_ids list. It then creates a
    new column "entity_id" and concatenates all of the entity DataFrames into a single DataFrame.
    Entity_ids can be found here: 
    https://www.huduser.gov/portal/datasets/geotools.html
    
    Arguments: a list of HUD entity_ids.
    
    Returns: a DataFrame of HUD FMR for each ZIP code and year from 2018-present for all HUD
            entities in entity_id list.
    '''
    df = pd.DataFrame()
    
    for entity_id in entity_ids:
        
        df = pd.concat([df, get_entity_data(entity_id)])

        
    return df
    
    
def get_hud_micro_data():
    '''
    This function checks to see if there is a local version of 'hud_micro.csv'.
    If it finds one, it reads it into a DataFrame and returns that df.
    If it does not find one, it runs 'new_hud_data()' to pull the data
    from the host and convert to a df. Then it writes that df to a local
    file 'hud_micro.csv' and returns the df. Function relies
    on other functions in the wrangle.py module.
    '''
    if os.path.isfile('hud_micro.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('hud_micro.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = clean_hud_micro(new_hud_micro_data())
        
        # Cache data
        df.to_csv('hud_micro.csv')
        
    return df



def clean_hud_micro(df):
    '''
    This function takes in the new_hud_micro dataframe and drops
    unnecessary columns and changes column names to pythonic ones.
    '''
    
    df = df.rename(columns={'Two-Bedroom' : 'two_bed_fmr'})
    df = df[['zip_code', 'two_bed_fmr']]
    
    return df
        

    
