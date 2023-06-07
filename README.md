# The Fairness of Fair Market Rent
## Time Series Analysis of HUD's Fair Market Rent (FMR) Rates
Corey Baughman, Mack McGlenn, Aaron Moore, Adriana Nuncio

Codeup: O'Neil Cohort  
June 2023
_____________________________________________________________________________________

### Project Overview

Every year, the Department of Housing and Urban Development releases a list of Fair Market Rents (FMRs) for over 2,600 markets across the United States. The FMR is produced for each combination of property location and number of bedrooms from 0-4. FMR is used as the baseline for various government programs that provide housing assistance to low-income families, such as the Housing Choice Voucher Program (2.7 million units)and the Project-Based Voucher Program (0.3 million units). As such, the accuracy of these values can't be overstated for the sake of the millions of Americans who depend on these programs. Our project's goal is to analyze the difference between HUD's FMR and 3rd party data for market averages to determine the reliability of FMR data in an actual market. If FMRs are too high, public housing agencies (PHAs) will be unable to maximize the number of families who receive assistance. If they're too low, it becomes more difficult for voucher users to acquire adequate housing.
_____________________________________________________________________________________
###  How to Read Our Work


_____________________________________________________________________________________

**Deliverables**

- A complete README.md which walks through the details of this project
- A final report folder which concisely displays the finished version of the project including exploration, findings, modeling, and all .py files needed to reproduce this project.
- Individual folders containing workbooks showing the unpolished groundwork and insights that lead to the final notebook
- Link to stakeholder presentation at [canva.com](link goes here)

#### Data Dictionary 

| Columns | Description |
| :---------| :------------------------ |
| diff | The difference between MMR and FMR. This is calculated as MMR - FMR |
| fmr | The HUD established Fair Market Rate for the entity. We chose to use the rate for two-bedroom properties. |
| mmr | The Median Market Rent. This is the median rent price of two-bedroom rental properties in the San Antonio/New Braunfels area as aggregated from 3rd party data (see the Acquire section for retrieval methodology) We cannot confirm that the boundaries of this area exactly match the boundaries of the federally defined MSA, but it should be close and any mismatch should remain consistent over time. |
| percent_diff | The percentage difference between MMR and FMR expressed in terms of FMR. This is calculated as (MMR - FMR) / FMR. |

#### Glossary

| Word | Definition |
| :---------| :------------------------ |
| CBSA | Core Based Statistical Area (CBSA) is an Office of Management and Budget(OMB) defined area containing a large population nucleus, or urban area, and adjacent communities that have a high degree of integration with that nucleus. There are two types of CBSAs: Metropolitan statistical areas (MSAs) and micropolitan statistical areas (µSAs). 
| Entity ID | An entity id is a code the federal government uses to uniquely identify Metropolitan Statistical Areas. In the case of the San Antonio - New Braunfel MSA, the entity id is 'METRO41700M41700'
| MSA | Metropolitan Statistical Area. This is a federally defined area that is used by the government to aggregate statistics for metropolitan areas. Each MSA is identified by an entity id code.

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
1. Does the HUD FMR rate accurately track 3rd Party market rental data over time?
2. Are there noticeable seasonal trends in the 3rd party data?
3. Are there seasonal trends in the difference between the FMR rates and 3rd party data?
____________________________________________________________________________________

## 2. Acquire
_____________________________________________________________________________________

#### Acquire Actions
Steps Taken:
1. HUD Data
    a. National level FMR historical data was retrieved from https://www.huduser.gov/portal/datasets/FMR/FMR_All_1983_2023_rev.csv
    b. The data for two-bedroom FMR for the San Antonio - New Braunfels (entity_id = 'METRO41700M41700') Metropolitan Statistical Area is then extracted using the prepare_hud_aggregate.py script in this repo.
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
    a. filter rows to only those in our entity_id
    a. chose columns for two bedroom FMRs in years 2017-2023
    a. reassign column names as years and transpose to make years rows
    a. group counties sharing the same entity_id into a single value for the entity
    a. resample the annual rates to monthly rates to align with 3rd party data frequency.
    a. time shift the monthly rates to line up with the federal fiscal year.
    a. there were no null values in the HUD data.
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
    
    
    
https://github.com/HUD-FMR-Time-Series-Analysis/project_repo/blob/main/mvp_folder/wrangle.py

## 4. Exploratory Data Analysis (EDA)

We performed Time Series Analysis on the data using Jupyter Notebooks with python, pandas, matplotlib, seaborn, and statmodels.api. Further analysis was done in Tableau Public. After some initial analysis, we decided not to split the data for exploration as there appeared to be some trend reversal in the newest data and we felt that visual analysis would be impaired by looking at a truncated training dataset. 

Here's what we found:

a. There has been a general widening of the gap between the FMR and 3rd Party Rents during the period from 2017-2023 for the San Antonio - New Braunfels MSA.
b. There appear to be seasonal disparities between the two rates: When the federal rate is updated in October, the gap between rates tends to close, but by summer and early fall, the gap tended to widen.



### Modeling
_____________________________________________________________________________________
##### Features:
* Modeling will be done on all features in the dataset, with a focus on trying to predict the difference between MMR and FMR.

##### Model Evaluation Metric:
* Root Mean Squared Error will be used as the evaluation metric for its applicability to continuous variables.

##### Target:
* While the difference is the target, we will also be modeling and predicting MMR and FMR due to the difference being reliant on both.
* We will also be modeling and predicting MMR and FMR due to the difference being reliant on both.

##### Baseline Models:
* Three baseline models were used, with 1 month rolling average performing the best. The model below is the metrics below are the metrics to beat for the models.

### Results:
* Only two models provided useful predictions, Holts Linear Trend with optimization and Holts Seasonal Trend (ExponentialSmoothing) with a seasonal period of 12 months, additive seasonality, additive overall trend, and damped hyperparameters set.
* When comparing to baseline predicitons, both models outperform the baseline, with Holt' Seasonal Trend performing the best. We will continuw on with Holt's Seasonal Trend into testing.
_____________________________________________________________________________________


### Conclusion & Reccomendations
_____________________________________________________________________________________
### Summary
* There has been a steady increase in the difference between MMR and FMR, with occasioanal decreases in the difference occurring in October, when the FMR voucher amount is adjusted. 
* The best time to use a voucher is between October and March. 
* Modeling was successful when using the baseline RMSE as a benchmark, but we do not believe it has a low enough RMSE to be useful for consumers.

### Recommendations
* There is an adjustment period of 1 year that the FMR takes to account for changes in the market. We recommend doing semi-annual adjustments, with October being the official adjustment and March holding a preliminary adjustment. This recommendation is based on the average shift in difference between March and October.

### Next Steps
* Acquire MMR data from before 2017
* Acquire and explore more locations
* Take a granular look into zip code level data instead of MSA


### Steps to Reproduce
_____________________________________________________________________________________

   1. Clone this repo.
   2. The final_report_mvp.ipynb in the mvp_folder.
   3. The data files are the .csv files included in the repo.
