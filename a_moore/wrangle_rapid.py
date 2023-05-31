import time
import requests
import pandas as pd


### For initial rapid api pull
def get_rapid_api(zipcode_list, rapid_api_key, filename):
    '''
    Arguments: 
        1. a list of zipcodes, with each zipcode in the list a string
        2. the rapid_api_key as a string that can be copied from the website after subscribing to the realty mole api using this website
            https://rapidapi.com/realtymole/api/realty-mole-property-api
        3. a string literal with .csv at the end for the filename of the saved df
    Actions: This fucntion pulls data from the REalty Mole rapid api and saves the messy data as a csv 
    Return: Messy market rent history data
    Modules:
        import time
        import requests
        import pandas as pd
    '''
    # intialize dicitonary
    market_rent_dict = {}
    
    # the headers necessary for the data, the raopid api key entered in the 
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com"
    }

    # For each zipcode in the list of sipcodes entered
    for zipcode in zipcode_list:
        
        # place the zipcode in the endpoint
        url = f"https://realty-mole-property-api.p.rapidapi.com/zipCodes/{zipcode}"
        
        # get the repsonse from the end point using the headers specififed
        response = requests.get(url, headers=headers)

        # if the reponse acts accordingly
        if (
        response.status_code != 204 and
        response.headers["content-type"].strip().startswith("application/json")
        ):
            try:

                # the repsonse is stored in data
                data = response.json()

                # tdata is stored in the dictionary with the zipcode as a key
                market_rent_dict[zipcode] = data

            except ValueError as e:

                print('ValueError', e)
        
        # the pull pauses for 2 seconds in orderreduce the load on the api and prevent error messages
        time.sleep(2)
    
    # the dictionary is turned into a df
    df = pd.DataFrame(market_rent_dict)
    
    # the df is saved as csv using the filename specified above
    df.to_csv(filename)
    
    # the function is exited and the df is returned
    return df

# Preparation for the rapid api data after it is saved as a csv
def rapid_api_mvp_prep(filename):
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
    
    # exit function and return newly created df
    return df
