import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from wrangle import wrangle_data

# plotting defaults
plt.rc('figure', figsize=(13, 7))
plt.style.use('seaborn-whitegrid')
plt.rc('font', size=16)

# getting data
df, train, test = wrangle_data()

# assigning target
y = df['diff']

def get_disparity_graph():
    '''
    This function gets the line graph showing the MMR and FMR cost changes over time
    '''
    
    # plot the mmr and fmr lines
    df.mmr.plot(label='Median Market Rent')
    df.fmr.plot(label='Fair Market Rent (40%)')
    
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
    # get data
    df, train, test = wrangle_data()
    
    # get target
    y = df['diff']
    
    # resample to 6 month with the mean and create a bar plot
    y.resample('6M').mean().plot.bar(width=.9, ec='black')
    
    # establish titles and axis lables
    plt.title('Average Difference by 6 Month Period')
    plt.xlabel('6-Month-Interval')
    plt.ylabel('Difference in Price')
    
    # only get the grid lines to folloow the x axis
    plt.grid(axis='x')
    
    # show the function
    plt.show()
    
    return
