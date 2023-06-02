# Clear Title (TBD)
## Time Series Analysis of HUD's Fair Market Rent (FMR) Rates
Corey Baughman, Mack McGlenn, Aaron Moore, Adriana Nuncio

Codeup: O'Neil Cohort 
June 2023
_____________________________________________________________________________________

### Project Overview

Every year, the Department of Housing and Urban Development releases a list of Fair Market Rents for over 2,600 markets across the United States.
The HUD Fair Market Rent is calculated by taking into account features such as the size of the rental unit, the number of bedrooms, and the location of the property. FMR is used as the baseline for various government programs that provide housing assistance to low-income families, such as the Housing Choice Voucher Program and the Project-Based Voucher Program. As such, the accuracy of these values can't be overstated for the sake of the millions of Americans who depend on these programs. Our project's goal is to analyze the margin of error between HUD's FMR and 3rd party data for market averages to determine the reliability of FMR data in an actual market. If FMRs are too high, public housing agencies (PHAs) will be unable to maximize the number of families who receive assistance. If they're too low, it becomes more difficult for voucher users to acquire adequate housing.
_____________________________________________________________________________________
###  How to Read Our Work


_____________________________________________________________________________________

**Deliverables**

- A complete README.md which walks through the details of this project
- A final report folder which concisely displays the finished version of the project including exploration, findings, modeling, and all .py files needed to reproduce this project.
- Individual folders containing workbooks showing the unpolished groundwork and insights that lead to the final notebook
- Link to stakeholder presentation at [canva.com](link goes here)

_____________________________________________________________________

#### Outline:
1. Initial Questions
2. Acquire & Prepare Data
3. Exploration/ Correlation Analysis
4. Statistical Analysis
5. Modeling
6. Conclusion

_____________________________________________________________________________________

## 1. Initial Questions
____________________________________________________________________________________

## 2. Acquire
_____________________________________________________________________________________

#### Acquire Actions
Steps Taken:
1. HUD Data
    a. 
2. Market Rent Data
    The Market Rent data was acquired from Bigger Pockets, a media company and social network focused on commercial and residential real estate investing. This particular dataset was created by Kaylin Cooper, an investor who has been tracking market trends in the top 100 cities in the U.S. since 2017.
- Size at Acquisition: 300 rows x 77 columns 
- Source: https://www.biggerpockets.com/files/user/leahd42/file/webinar-bonus-2022-rental-data


3. Realty Mole Data
    a. Accessed Realty Mole data using rapid api
    b. Saved data as a csv file


Link to functions in acquire.py file:

## 3. Prepare 
_____________________________________________________________________________________
#### Prepare Actions:
Steps Taken:
1. HUD Data
    a. 
2. Market Rent Data
    a. For the sake of reaching MVP, we will only be looking at two bedroom units in San Antonio. We merged this median market rent (MMR) data with HUD's Fair Market Rent (FMR) data into one dataframe. The step by step comments for preparation can be found in the wrangleHUDpro_amr_data.py file. Here are the steps that we took to make sure the dataframes matched for joining:
- Set the dates as the index for the dataframe
- Isolate the market rent for the San Antonio market only
- Keep only the values for 2 bedroom units

3. Realty Mole Data
    a. Converted string to dictionary
    b. Added zipcode and date to dictionaries
    c. Converted dictionary to a dataframe
    d. Set date as the index
    
    
    
Link to functions in acquire.py file:

## 4. Exploratory Data Analysis (EDA)

Short paragraph about how we approached exploration for this data.

Here's what we found:

a. 
b. 
c. 



### Modeling
_____________________________________________________________________________________
A paragraph explaining our approach to modeling. Types of modeling we used, how we split the load, what we found. 

### Results: 
_____________________________________________________________________________________


### Conclusion & Reccomendations
_____________________________________________________________________________________
Here's what we learned from this project:

### Steps to Reproduce
_____________________________________________________________________________________

   1. Clone this repo.
   2. 
   3. 
   4. 
