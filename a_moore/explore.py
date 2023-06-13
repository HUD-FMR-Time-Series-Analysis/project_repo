import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import geopandas
import warnings
warnings.filterwarnings('ignore')
from wrangle_final import clean_zcta_gdf, wrangle_zipcode_data, wrangle_metro_data, wrangle_gdf

# plotting defaults
plt.rc('figure', figsize=(13, 7))
plt.style.use('seaborn-whitegrid')
plt.rc('font', size=16)

# getting data
df, train, validate, test = wrangle_metro_data()
zip_code = wrangle_zipcode_data()
gdf = clean_zcta_gdf()


# assigning target
y = df['diff']

def get_disparity_graph():
    '''
    This function gets the line graph showing the MMR and FMR cost changes over time
    '''
    
    # plot the mmr and fmr lines
    df.mmr.plot(label='Median Market Rent')
    df.fmr.plot(label='Fair Market Rent (40%)')
    plt.fill_between(df.index, df.mmr, df.fmr, color='red', alpha=0.1)
    
    # get a border on the legend
    plt.legend(frameon=True)
    
    # set the title and axis labels
    plt.ylabel('Amount in Dollars')
    plt.xlabel('Year')
    plt.title('Disparity between MMR and FMR Amounts')
    
    # show the chart
    plt.show()
    
    return


def get_target_hist():
    '''
    This function gets the distribution of the mmr and fmr difference
    '''
    # plot the histogram of the target with 25 follar bins
    y.plot.hist(ec='black', bins=[0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400])
    
    # set the title and axis labels
    plt.title('Distribution of the Difference between MMR and FMR')
    plt.ylabel('Number of Occurences')
    plt.xlabel('Difference of MMR and FMR in Dollars')
    
    # set the grid lines
    plt.grid(axis='x')
    
    # show the plot
    plt.show()
    
    return

def get_trend_line_plot():
    '''
    This function gets the line plot of the mmr and fmr difference over three time intervals - monthly, quarterly, and yearly
    '''
    
    # plot the monthly difference 
    y.plot(alpha=.2, label='Monthly')
    
    # plot the quarterly difference
    y.resample('3M').mean().plot(label='Quarterly')
    
    # plot the yearly difference
    y.resample('Y').mean().plot(alpha = .8, label='Yearly')
    
    # set the title and labels
    plt.title('Trend of MMR and FMR Difference Over Time')
    plt.xlabel('Year')
    plt.ylabel('Difference of MMR and FMR')
    
    # change the legend location and give a border
    plt.legend(loc='lower right', frameon=True)
    
    # show the visual
    plt.show()
    
    return

def get_difference_by_month_bar():
    '''
    This function gets the bar chart of the average difference between mmr and fmr per month. 
    
    '''
    
    # assign barechart to ax
    ax = y.groupby(y.index.month).mean().plot.bar(width=.9, ec='black')
    
    # set tick rotation
    plt.xticks(rotation=0)
    
    # set titles and x and y labels
    ax.set(title='Average Difference between Median Market Rate(MMR) \nand Fair Market Rate(FMR) by Month', xlabel='Month', ylabel='Difference between MMR and FMR in Dollars')
    
    plt.grid(axis='x')
    
    # show visual
    plt.show()
    
    return

def get_avg_diff_6m():
    '''
    This function calls a bar chart representing the average difference per 6 month interval from 2017 to now
    '''
    
    # resample to 6 month with the mean and create a bar plot
    y_resample = y.resample('6M').mean()
    y_resample.index = y_resample.index.strftime(date_format='%Y-%m')
    
    y_resample.plot.bar(width=.9, ec='black')
   
    # establish titles and axis lables
    plt.title('Average Semi-Annual Difference')
    plt.xlabel('6-Month-Interval')
    plt.ylabel('Difference in Price')
    plt.xticks(rotation = 55)
    
    # only get the grid lines to folloow the x axis
    plt.grid(axis='x')
    
    # show the function
    plt.show()
    
    return

def get_afforadability_map():
    '''
    This function merges the zip code tabulation area GeoDataFrame with the affordability data frame
    '''
    # get wrangled df
    gdf = wrangle_gdf()
    
    # exit and return a map with the afforability as the focus
    return gdf.explore('affordability', cmap='RdYlGn')

def get_interactive_map():
    '''
    This funciton displays an interactive map showing the changes in affordability fromwhen the dioffreefnce between FMR and MMR were at their lowest and highest for the dates that the zipcode tab data is avaialble.
    Module:
        from matplotlib.colors import ListedColormap
    '''
    # get needed date to matchg the zipcode data
    df = df.loc['2020':]

    # get the minimum and maximum differecne date
    max_diff_date = df['diff'].idxmax().strftime('%Y-%m')
    min_diff_date = df['diff'].idxmin().strftime('%Y-%m')

    # getting max differnce data
    max_difference = zip_code.loc[max_diff_date]

    # getting minimum difference data
    min_difference = zip_code.loc[min_diff_date]

    # getting affordability df with the minuimum and maximum
    min_max_afford = min_difference[['zip_code', 'affordability']]\
                    .rename({'affordability':'min_affordability'}, axis=1)\
                    .merge(max_difference[['zip_code', 'affordability']]\
                    .rename({'affordability': 'max_affordability'}, axis=1))

    # create difference columns
    min_max_afford['difference'] = min_max_afford['min_affordability'] - min_max_afford['max_affordability']

    # establish affordability based on the shifts
    min_max_afford['Affordability'] = np.where(min_max_afford['difference'] == 0, 'No Change', np.where(min_max_afford['difference'] > 0, 'Less Affordable', 'More Affordable'))

    # columns of interest
    cols = ['zip_code', 'Affordability']

    # merging data
    gdf = min_max_afford[cols].merge(gdf, how='inner', on='zip_code')

    # setting index to zipcode
    gdf = gdf.set_index('zip_code')

    # set to gdf
    gdf = geopandas.GeoDataFrame(gdf)

    # get cmap colors
    cmap = ListedColormap(['red', 'green', 'lightgray'])

    # get interactive map
    return gdf.explore('Affordability', cmap=cmap)
    
