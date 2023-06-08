import pandas as pd
from prepare_hud_aggregate import get_hud_macro_data
from wrangle_HUDpro_amr_data import get_sanant_amr_data
from wrangle_hud_micro import get_hud_micro_data
from wrangle_rapid import rapid_api_mvp_prep

# Creating a function for it 
def wrangle_data():
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
    hud = get_hud_macro_data()
    amr = get_sanant_amr_data()
    
    # converting the hud index datetime
    hud.index = pd.to_datetime(hud.index)


    # creating merged df
    merged = pd.merge(left=hud, right=amr, how='outer', right_index=True, left_index=True)
    
    # filling in witht he correct number
    merged['fmr'].fillna(1286, inplace=True)
    
    # dropping the null values that are not necessary
    merged.dropna(inplace=True)
    
    # changed amr to float
    merged['AMR'] = merged['AMR'].astype(float)
    
    # creating the difference 
    merged['diff'] =  merged['AMR'] - merged['fmr']
    
    # creating the percent difference in terms of fmr
    merged['percent_diff'] =  (merged['AMR'] - merged['fmr']) / merged['fmr']
    
    # changing name for accureacy (its the median not the average)
    merged = merged.rename({'AMR': 'mmr'}, axis=1)
    
    # creating the train
    train = merged[merged.index <= '2022-02-01']
    
    # creating the test 
    test =  merged[merged.index > '2022-02-01']
    
    # return the merged df, train df, and test df
    return merged, train, test



def wrangle_micro_data(filename):
    '''
    This function combines the get_hud_micro_data output and the 
    rapid_api_mvp_prep output. First it makes the column names 
    pythonic, then adds columns for the absolute difference between 
    AMR and FMR, the percent_difference between AMR and FMR in terms 
    of FMR and .
    
    Arguments: the filename of the rapid api data .csv as a string.
    Returns: a dataframe of ZIP Code level market and FMR data for
            two-bedroom properties.
    '''
    
    # get prepped rapid api data from wrangle_rapid.py
    df_rapid = rapid_api_mvp_prep(filename) 
    
    # get column names as a list
    cols = df_rapid.columns.to_list()
    
    # establish a list of more pythonic column names
    new_cols = ['bedrooms', 'average_rent', 'min_rent',
            'max_rent', 'num_properties', 'zip_code']
    
    # zip old and new column names together into a dictionary
    # and use dict to rename df_rapid columns
    df_rapid = df_rapid.rename(columns = dict(zip(cols, new_cols)))
    
    # get hud zip code level data from wrangle_hud_micro
    df_hud = get_hud_micro_data()
    
    # combine the two dataframes on date and zip code
    df = df_rapid.merge(df_hud, how='inner', on=['date', 'zip_code'])
    
    # add column 'diff' for absolute difference between AMR and FMR
    df['diff'] = df.average_rent - df.two_bed_fmr
    
    # add column 'percent_diff' for percent difference in AMR and FMR
    # in terms of AMR
    df['percent_diff'] = ((df.average_rent - df.two_bed_fmr) / df.two_bed_fmr) * 100
    
    return df
    
    
    