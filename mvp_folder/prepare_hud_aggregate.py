# prepare_hud_aggregate.py

import numpy as np
import pandas as pd

# this is the entity_id for San Antonio - New Braunfels MSA
entity_id = 'METRO41700M41700'

def get_hud_macro_data(entity_id):
    '''
    This function takes in a HUD entity_id and searches the FMR historical data .csv
    for the FMR rates for that entity between 2017 and 2023. Then only the FMR rates
    for those years are kept and the columns are renamed to the years of the data.
    The dataframe is then grouped by the 2023 column and aggregated on the first instance.
    This is necessary as there are often multiple counties in a Metropolitan Statistical
    Area(entity_id). The data for each county is the same so grouping on the first county
    doesn't alter the rate information. The dataframe is then transposed so that the 
    years are rows. The index is then cast to datetime and set as index. The dataframe is
    then resampled to monthly and FMR values filled forward in order to match the monthly
    retail data that will be retrieved via another function. Filling forward is correct as
    the FMR rates are the same for the entire year. New FMR rates go into effect at the 
    beginning of the federal fiscal year, which is October 1st of the prior year. For this 
    reason, the resampled data is shifted backwards by three months to match the
    fiscal year. Finally, the datetime index is formatted as a year-month string to align
    with the retail dataframe later.
    
    Arguments: a HUD entity id
    
    Returns: a DataFrame of FMR rates by year for that entity id
    '''
    df = pd.read_csv('FMR_All_1983_2023_rev.csv', encoding='latin1')
    df = df[df.msa23 == entity_id].reset_index(drop=True)
    cols = ['fmr23_2', 'fmr22_2', 'fmr21_2', 'fmr20_2', 'fmr19_2', 'fmr18_2', 'fmr17_2']
    df = df[cols]
    df.rename(columns={'fmr23_2':'2023', 'fmr22_2':'2022','fmr21_2':'2021','fmr20_2':'2020',
                      'fmr19_2':'2019','fmr18_2':'2018','fmr17_2':'2017',}, inplace=True)
    df = df.groupby('2023').first().reset_index().T
    df = df.rename(columns={0:'fmr'})
    df['date'] = pd.to_datetime(df.index)
    df.set_index('date', inplace=True)
    # shift the fmr rates backwards by three months to reflect federal fiscal year
    df = df.resample('M').ffill().shift(periods=-3, freq='M')
    # format date index as strings for alignment with retail rent dataframe
    df.index = df.index.strftime('%Y-%m')

    return df