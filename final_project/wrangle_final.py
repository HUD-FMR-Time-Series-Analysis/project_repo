import pandas as pd
import numpy as np

import csv
from scipy import stats
import requests
from datetime import datetime
import os
import geopandas

### Wrangle Dataset 1 ###

# HUD FMR for SA/NB, TX Metro Area
def get_hud_metro_data():
    '''
    Arguments: a HUD entity id
    Returns: a DataFrame of all info from csv
    '''
    df = pd.read_csv('FMR_All_1983_2023_rev.csv', encoding='latin1')

    return df

def clean_hud_metro_data(entity_id = 'METRO41700M41700'):
    '''
    This function cleas the hud macro data.
    Steps:
        Filter by entity id
        Keep columns of interest 
        Rename columns
        Transpose DF
        Change index to datetime
        Resample to monthly, fill the nulls, and shift the dates by 3 months
    '''
    # get data
    df = get_hud_metro_data()
    
    # filter by entity id, reset index, and drop old index
    df = df[df.msa23 == entity_id].reset_index(drop=True)

    # filter by columns of interest
    cols = ['fmr23_2', 'fmr22_2', 'fmr21_2', 'fmr20_2', 'fmr19_2', 'fmr18_2', 'fmr17_2']
    df = df[cols]
    
    # rename columns for human friendliness
    df.rename(columns={'fmr23_2':'2023', 'fmr22_2':'2022','fmr21_2':'2021','fmr20_2':'2020',
                  'fmr19_2':'2019','fmr18_2':'2018','fmr17_2':'2017',}, inplace=True)
    
    # get only the first values and transpose the df
    df = df.iloc[[0]].T

    # rename the col
    df = df.rename(columns={0:'fmr'})

    # change index to datetime
    df.index = pd.to_datetime(df.index)

    # resamnple to monthly and shift to october as the strt date to match federal fiscal years
    df = df.resample('M').ffill().shift(periods=-3, freq='M')
    
    # change index to string form
    df.index = df.index.strftime('%Y-%m')
    
    # exit and return the df
    return df


def get_mmr_data():
    '''
    Open MMR csv and provide it in a df 
    '''
    #Acquire the data from csv
    df = pd.read_csv('HUDpro_amr_unmerged.csv')
    
    # exit and return df
    return df

def clean_mmr_data():
    '''
    This function gets the mmr data and cleans it removing unnecessary columns and rows.
    The function also sets the index to datetime and converts the mmr column to a integer
    '''
    # get data
    df = get_mmr_data()

    # Create a dataframe that only contains information for San Antonio
    df = df.loc[(df['City']== 'SAN ANTONIO, TX')].T

    # drop unnecessayr rows and columns, rename the index, rename the focus variable 'mmr'
    df = df.drop(index=['City', 'Beds'], columns= [246, 248]).rename_axis('date').rename({247:'mmr'}, axis=1)

    # changing index to date
    df.index = pd.to_datetime(df.index)

    # Remove non-integer values from mmr column
    df['mmr']= df['mmr'].str.replace('$','').str.replace(',','').astype(int)

    return df

def wrangle_metro_data():
    '''
    Arguments: none
    Actions: gets both data sets, changes the fmr index to datetime, merges bothe data sets, imputes missing fmr data with last value, drops the mmr data, adds column with the difference between them
    Returns: merged data frame ready for exploration
    Modules:
        import pandas as pd
        from prepare_hud_aggregate import get_hud_macro_data
        from wrangle_HUDpro_amr_data import get_sanant_amr_data
    Notes: csv's required for hud and sanantonio market rent data must be in the same folder as this function for it to work 
    '''
    # get data
    hud = clean_hud_metro_data()
    mmr = clean_mmr_data()
    
    # converting the hud index datetime
    hud.index = pd.to_datetime(hud.index)

    # creating merged df
    df = pd.merge(left=hud, right=mmr, how='outer', right_index=True, left_index=True)
    
    # filling in with the correct number
    df['fmr'].fillna(1286, inplace=True)
    
    # dropping the null values that are not necessary
    df.dropna(inplace=True)
    
    # creating the difference 
    df['diff'] =  df['mmr'] - df['fmr']
    
    # creating the percent difference in terms of fmr
    df['percent_diff'] =  (df['mmr'] - df['fmr']) / df['fmr'] * 100
    
    # splitting 12 month(test), 24month(validate), 39 month(train)
    test = df[-12:]
    validate = df[-36:-12]
    train = df[:-36]
    
    # return the merged df, train df, and test df
    return df, train, validate, test

#### Wrangle Dataset 2 ####
def get_hud_zipcode_data():
    '''
    Arguments: none
    Actions:
    Returns:
    Modules:
        import pandas as pd
        imoprt requests
        from env import hud_token
        from datetime import datetime
    '''
    # a variable to hold the xpected or future file name
    filename = '''hud_zipcode_data.csv'''
    
    # if the file is present in the directory 
    if os.path.isfile(filename):
      
        # read the csv and assign it to the variable df
        df = pd.read_csv(filename, index_col=0)
        
        # return the dataframe and exit the funtion
        return df
    
    # if the file is not present
    else: 
    
        # set header for the api request
        headers = {'Authorization': f'Bearer {hud_token}'}

        # get a list of years
        years = pd.period_range(start=2018, end=datetime.now().year, freq='Y').to_series().astype(str).reset_index(drop=True).to_list()

        # intialize a df
        df = pd.DataFrame()

        # for each year
        for year in years:

            # insert entity id and year into the url
            url = f'https://www.huduser.gov/hudapi/public/fmr/data/METRO41700M41700?year={year}'

            # store the reposnse
            response = requests.get(url, headers=headers)

            # take out the data as a dict
            data = response.json()

            # create a dummy df to store the basic data info
            dum = pd.DataFrame(data['data']['basicdata'])

            # add a year column
            dum['year'] = data['data']['year']

            # add the dummy 
            df = pd.concat([df, dum])
        
        # cache the data
        df.to_csv(filename)
        
        # exit and return the final df
        return df

def clean_hud_zipcode_data():
    '''
    Arguments: None
    Actions: 
        Set DateTimeIndex
        Resample the dataframe to monthly, shift 3 months for federal fiscal calendar, and forward fill missing data
        Remove unneeded columns
        Change data types
    Returns: clean hud zipcode dataframe
    Modules:
        from datetime import datetime
        import pandas as pd
        from wrangle import get_hud_zipcode_data
    '''
    # get data
    hud_zip = get_hud_zipcode_data()

    # convert to year format
    hud_zip['date'] = pd.to_datetime(hud_zip['year'], format='%Y')

    # set the index
    hud_zip = hud_zip.set_index('date')

    # initialize a dataframe
    df = pd.DataFrame()

    # get all the unique zip codes
    zip_codes = hud_zip.zip_code.unique().tolist()

    # for each zip code
    for zip_code in zip_codes:

        # isolate the zipcode
        df_zip = hud_zip[hud_zip.zip_code == zip_code]

        # resample and shift 3 months
        df_zip = df_zip.resample('M').ffill().shift(periods=-3, freq='M')

        # get a range of missing months after the dhift
        missing_dates = pd.period_range(start = df_zip.index[-1], end = datetime.now(), freq='M')

        # concatenate the individual zipcode with the missing index dates and forward fill the missing components
        df_zip = pd.concat([df_zip, pd.DataFrame(index=missing_dates)]).ffill()

        # add the finished zipcode df to the complete df
        df = pd.concat([df, df_zip])

    # set index name 
    df.index.name = 'date'
    
    # set index to datetime and str ro remove the ending
    df.index = pd.to_datetime(df.index, format = '%Y-%m').strftime('%Y-%m')
    
    # reset to date time to have dates that start at the beginning of the month
    df.index = pd.to_datetime(df.index)
    
    # drop unnecessary columns and rename column
    df = df.drop(['Efficiency', 'One-Bedroom', 'Three-Bedroom',
       'Four-Bedroom', 'year'], axis=1).rename({'Two-Bedroom':'two_bed_fmr'}, axis=1)

    # change zipcode dtype
    df['zip_code'] = df['zip_code'].astype(int).astype(str)
    
    
    return df

# 
def clean_rapid_zipcode_data(filename = 'rapid_zipcode_data.csv'):
    '''
    Argument: the filename for the rapid_api csv data as a string literal
    Actions: This extracts the important historical data from the messy csv acquired from rapid api and returns a dataframe
    Modules:
        import pandas as pd
    '''
    
    # get the data from the csv name
    df = pd.read_csv(filename, index_col=0)

    # convert strings into dictionaries and assign the series to a variable
    rental_data = df.T.rentalData.apply(eval)
    
    # initialize df
    df = pd.DataFrame()

    # for each zipcode in the rental_data keys
    for zipcode in rental_data.keys():

        # For each date in the in history for each zipcode
        for date in rental_data[zipcode]['history'].keys():

            # lastly, for each dictionary in the detailed data based on zipcode and date
            for i, n in enumerate(rental_data[zipcode]['history'][date]['detailed']):
                
                # dictionary to hold date and zipcode 
                new_info = {'date':pd.to_datetime(date), 'zipcode':zipcode}

                # add date to the dict 
                rental_data[zipcode]['history'][date]['detailed'][i].update(new_info)

            # created a place holder df with that informatiuon
            dum = pd.DataFrame(rental_data[zipcode]['history'][date]['detailed'])

            # combine it with the intialized df and save as the new one
            df = pd.concat([df, dum])
    
    # set index to date
    df = df.set_index('date').sort_index()
    
    # only 2 bedrooms 
    df = df[df['bedrooms'] == 2]
    
    # drop bedrooms
    df = df.drop('bedrooms', axis=1)
    
    # make list of new column names
    new_cols = ['average_rent', 'min_rent', 'max_rent', 'num_properties', 'zip_code']
    
    # rename columns
    df = df.rename(columns = dict(zip(df.columns, new_cols)))
    
    # exit function and return newly created df
    return df

def wrangle_zipcode_data():
    '''
    Arguments: none
    Actions:
        Gets data
        Merges both hud and rapid api datasets
        Creates new features
    Returns: wrangled df
    Modules:
        import pandas as pd
    '''
    # get cleaned zipcode data
    hud = clean_hud_zipcode_data()
    rapid = clean_rapid_zipcode_data()

    # combine the two dataframes on date and zip code
    df = rapid.merge(hud, how='inner', on=['date', 'zip_code'])

    # add column 'diff' for absolute difference between MMR and FMR
    df['diff'] = df.average_rent - df.two_bed_fmr

    # add column 'percent_diff' for percent difference in MMR and FMR
    df['percent_diff'] = ((df.average_rent - df.two_bed_fmr) / df.two_bed_fmr) * 100

    # getting different areas of affordability
    df['afford_min'] = df['min_rent'] - df['two_bed_fmr'] <= 0
    df['afford_avg'] = df['average_rent'] - df['two_bed_fmr'] <= 0
    df['afford_max'] = df['max_rent'] - df['two_bed_fmr'] <= 0

    # getting an affordability score using all the true and falses
    df['affordability'] = df[['afford_min', 'afford_max', 'afford_avg']].sum(axis=1)

    # exit function and return wrangled df
    return df

### Wrangle Dataset 3 ###
def clean_zcta_gdf(filename = 'zcta_of_interest.shp'):
    '''
    Arguments:
    Actions: This function creates a GeoDataFrame with the zip code tabulation areas that are present in the San Antonio, New Braunfels metro area as defined by the Census Bureau and HUD. 
        Prepares the GeoDataFrame for merging with other DataFrames
    '''
    # read file
    gdf = geopandas.read_file(filename)

    # rename for merge
    gdf = gdf.rename({'ZCTA5CE20':'zip_code'}, axis=1)

    # drop unnecessary columns
    gdf = gdf.drop(['GEOID20', 'CLASSFP20', 'MTFCC20', 'FUNCSTAT20', 'ALAND20',
           'AWATER20', 'INTPTLAT20', 'INTPTLON20'], axis=1)

    return gdf

def wrangle_gdf(date = '2023-05'):
    '''
    Arguments: None
    Actions:
        Loads data
        Gets columns of interest
        Merges the zipcode data to the gdf 
    Returns: a geodataframe with affordability information for 2023-05
    Module: 
        import geopandas
        import pandas as pd
    '''
    # get zipcode data
    df = wrangle_zipcode_data()
    gdf = clean_zcta_gdf()
    
    # columns of interest
    cols = ['zip_code', 'affordability', 'num_properties']
    
    # get the dates of interest
    df = df.loc[date][cols]
    
    # merging data
    gdf = df.merge(gdf, how='inner', on='zip_code')

    # setting index to zipcode
    gdf = gdf.set_index('zip_code')

    # set to gdf
    gdf = geopandas.GeoDataFrame(gdf)
    
    return gdf