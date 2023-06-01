import pandas as pd
import numpy as np

import csv
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as stats
import seaborn as sb

from scipy import stats
import requests
from datetime import datetime



# *****Acquire & Prepare*****

def get_sanant_amr_data():
    """ """
    #Acquire the data from csv
    df = pd.read_csv('HUDpro_amr_unmerged.csv')
    
    # Create a dataframe that only contains information for San Antonio
    df = df.loc[(df['City']== 'SAN ANTONIO, TX')].T
    # Create a dataframe that only return information for 2 bedroom units in San Antonio
    # Drop 'City' and 'Beds' from dataframe
    # Label the axis 'Date'
    df = df.rename(columns={246:'1 Bed', 247:'AMR', 248:'3 Bed'}).drop(index=
                        ['City', 'Beds'], columns= ['1 Bed', '3 Bed']).rename_axis('Date')
    
    # Create a list of the date strings.
    date_strings = ['1/1/2017', '2/1/2017', '3/1/2017', '4/1/2017', '5/1/2017', '6/1/2017',         '7/1/2017', '8/1/2017', '9/1/2017', '10/1/2017', '11/1/2017', '12/1/2017', '1/1/2018', '2/1/2018', '3/1/2018', '4/1/2018', '5/1/2018', '6/1/2018', '7/1/2018', '8/1/2018', '9/1/2018', '10/1/2018', '11/1/2018', '12/1/2018', '1/1/2019', '2/1/2019', '3/1/2019', '4/1/2019', '5/1/2019', '6/1/2019', '7/1/2019', '8/1/2019', '9/1/2019', '10/1/2019', '11/1/2019', '12/1/2019', '1/1/2020', '2/1/2020', '3/1/2020', '4/1/2020', '5/1/2020', '6/1/2020', '7/1/2020', '8/1/2020', '9/1/2020', '10/1/2020', '11/1/2020', '12/1/2020', '1/1/2021', '2/1/2021', '3/1/2021', '4/1/2021', '5/1/2021', '6/1/2021', '7/1/2021', '8/1/2021', '9/1/2021', '10/1/2021', '11/1/2021', '12/1/2021', '1/1/2022', '2/1/2022', '3/1/2022', '4/1/2022', '5/1/2022', '6/1/2022', '7/1/2022', '8/1/2022', '9/1/2022', '10/1/2022', '11/1/2022', '12/1/2022', '1/1/2023', '2/1/2023', '3/1/2023']
    # Create a pandas DatetimeIndex using the list of date strings.
    date_index = pd.DatetimeIndex(date_strings)
    # Set my index as date_index 
    df = df.set_index(date_index)
    
    # Remove noise non-integer values from AMR column
    df['AMR']= df['AMR'].str.replace('$','').str.replace(',','')
    
    return df