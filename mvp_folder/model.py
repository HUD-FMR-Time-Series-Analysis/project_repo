# for presentation purposes
import warnings
warnings.filterwarnings("ignore")

# transform
import numpy as np
import pandas as pd

# working with dates
from datetime import datetime

# evaluate
from sklearn.metrics import mean_squared_error
from math import sqrt 

#models
from statsmodels.tsa.api import Holt, ExponentialSmoothing
# data
from wrangle import wrangle_data

# get data
df, train, validate, test1 = wrangle_data()


### HELPER FUNCTIONS ###
def get_eval_df():
    '''
    Creates a dataframe to hold the model target and rmse
    '''
    # Create the empty dataframe
    eval_df = pd.DataFrame(columns=['model_type', 'target_var', 'rmse'])
    
    # exit and return the empty df
    return eval_df

# evaluation function to compute rmse
def evaluate(yhat_df, target_var):
    '''
    This function will take the actual values of the target_var from test, 
    and the predicted values stored in yhat_df, 
    and compute the rmse, rounding to 0 decimal places. 
    it will return the rmse. 
    '''
    # gets the rmse and rounds to 0 decimals places
    rmse = round(sqrt(mean_squared_error(validate[target_var], yhat_df[target_var])), 0)
    
    # returns the rmse 
    return rmse


# function to store rmse for comparison purposes
def append_eval_df(yhat_df, model_type, target_var):
    '''
    this function takes in the yhat_df used, type of model run, and the name of the target variable. 
    It returns the eval_df with the rmse appended to it for that model and target_var. 
    '''
    
    # get the rmse
    rmse = evaluate(yhat_df, target_var)
    
    # create a dictionary to store relevant information
    d = {'model_type': [model_type], 'target_var': [target_var], 'rmse': [rmse]}
    
    # convert to df
    d = pd.DataFrame(d)
    
    # return the df
    return d



### BASELINE MODEL FUNCTIONS ###
def get_baseline_simple_average():
    '''
    This function uses the global train variables o calculate the simple average for each column in train.
    It stores the information for each variable in a df that uses the test.index and returns that df
    '''
    # initialize df
    d = pd.DataFrame(index=validate.index)
    
    # for each column
    for col in train.columns:
        
        # calculate the simple average
        simple_avg = round(train[col].mean(), 2)
        
        # add the simple average into the column
        d[col] = simple_avg
    
    # exit and return df
    return d

def get_baseline_rolling_average(period = 1):
    '''
    This function takes in a period as an argument and calculates the rolling/moving average based on that period.
    It then returns the rolling average for each column in train in a dartaframe
    '''
    # create dict
    d = pd.DataFrame(index=validate.index)
    
    # for each col in train
    for col in train.columns:

        # get the rolling mean
        rolling = round(train[col].rolling(period).mean()[-1], 2)
        
        # add column with rolling mean in it
        d[col] = rolling

    # return the df
    return d

def get_baseline_table():
    '''
    This function creates a datafram with the baseline model rmse's for each feature in the tain df
    '''
    # get eval_df
    eval_df = get_eval_df()
    
    # Create list of baseline tables with the model name as a pairt
    models_and_type = [(get_baseline_simple_average(), 'simple_avg'), (get_baseline_rolling_average(1), '1_month_rolling_average'), (get_baseline_rolling_average(6), '6_month_rolling_avg')]

    # for each df and modeltype
    for model, model_type in models_and_type:

        # for each columns in df
        for col in train.columns:

            # add to the eval_df
            new_eval_df = append_eval_df(model, model_type=model_type,
                                    target_var=col)
            
            # concat new eval with old eval
            eval_df = pd.concat([eval_df, new_eval_df])
    
    # exit and return eval df with all evaluations
    return eval_df.reset_index().drop('index', axis=1)


### NON-BASELINE MODELS ###
# make programmatic
def get_holt_seasonal_trend_forecast(seasonal_periods=12, trend='add', seasonal='add', damped=True):
    '''
    This function takes in hyperparameteers for the holts seasonal trend model and outputs a df with each forecast for each column in the train df
    '''
    # initialize dictionary
    d = pd.DataFrame(index = validate.index)

    # for each column in train
    for col in train.columns:

        # fit on the columns with 12 month seasonality and additive trend and seasonals, with a damped
        hst_fit = ExponentialSmoothing(train[col], seasonal_periods=seasonal_periods, trend=trend, seasonal=seasonal, damped=damped).fit(optimized=True)

        # get forecast for the length or shape
        hst_forecast = hst_fit.forecast(validate.shape[0] + 1)

        # add the forecasted information to the dictionary with only the test index
        d[col] = hst_forecast

    # exit function and return the df
    return d

# function
def get_holts_optimized():
    '''
    This functions models and predicts each column in the global train variable and places the predicted values in a df
    '''
    # intialize df
    d = pd.DataFrame(index=validate.index)

    # for each column in train
    for col in train.columns:

        # initialize a model for the column
        model = Holt(train[col], exponential=False, damped=True)

        # fit the model with optimizaiton 
        model = model.fit(optimized=True)

        # get the predicted values, using the first date in the test index and th last date in the index as start and end positions
        values = model.predict(start = validate.index[0],
                                  end = validate.index[-1])

        # add the values to the dataframe
        d[col] = round(values, 2)

    # exit the function and return the df
    return d

def get_models():
    '''
    This function takes the two best performeing models and presents them in a datframe format
    
    '''
    # get eval_df
    eval_df = get_eval_df()
    
    # Create list of baseline tables with the model name as a pairt
    models_and_type = [(get_holts_optimized(), 'holts_optimized'), (get_holt_seasonal_trend_forecast(), 'holts_seasonal')]

    # for each df and modeltype
    for model, model_type in models_and_type:

        # for each columns in df
        for col in train.columns:

            # add to the eval_df
            new_eval_df = append_eval_df(model, model_type=model_type,
                                    target_var=col)
            
            # concat new eval with old eval
            eval_df = pd.concat([eval_df, new_eval_df])
    
    # exit and return eval df with all evaluations
    return eval_df.reset_index().drop('index', axis=1)


def get_all_models():
    '''
    This function returns a df with all models present
    '''
    # return the functions with both baseline and non-baseline models in one table
    return pd.concat([get_baseline_table(), get_models()]).reset_index().drop('index', axis=1)

