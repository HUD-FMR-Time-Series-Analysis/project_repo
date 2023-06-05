import pandas as pd
from prepare_hud_aggregate import get_hud_macro_data
from wrangle_HUDpro_amr_data import get_sanant_amr_data
import warnings
warnings.filterwarnings('ignore')


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
    
    # normalize the index
    merged.index = merged.index.normalize()
    
    # changed amr to float
    merged['AMR'] = merged['AMR'].astype(float)
    
    # creating the difference 
    merged['diff'] =  merged['AMR'] - merged['fmr']
    
    # creating the percent difference in terms of fmr
    merged['percent_diff'] =  ((merged['AMR'] - merged['fmr']) / merged['fmr']) * 100
    
    # changing name for accureacy (its the median not the average)
    merged = merged.rename({'AMR': 'mmr'}, axis=1)
    
    # splitting 12 month(test), 24month(validate), 39 month(train)
    test = merged[-12:]
    validate = merged[-36:-12]
    train = merged[:-36]
    
    # return the merged df, train df, and test df
    return merged, train, validate, test
