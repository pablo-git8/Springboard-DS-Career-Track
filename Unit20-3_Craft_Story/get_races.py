import numpy as np
import pandas as pd
import xmltodict
import requests
# Treating races data frame

def practices_quali(i):
    '''
    Support function for converting practices and quali columns
    '''
    global races, races_ap
    if i == 'ThirdPractice' or i == 'Sprint':
        # Converting 'ThirdPractice' and 'Sprint' column
        try:
            races[i] = races[i].apply(lambda x: x if x == x else {'Date': np.nan})
            races[i] = races[i].transform(lambda x: x['Date'])
        except:
            races[i] = np.nan
    else:
        # Converting the other columns
        try:
            races[i] = races[i].transform(lambda x: x['Date'])
        except:
            races[i] = np.nan

def season_reader(season):
    global races, races_ap

    # Reading URL and putting into a DF
    url = "http://ergast.com/api/f1/{}".format(season)
    response = requests.get(url)
    races = pd.DataFrame.from_dict(xmltodict.parse(response.text)['MRData']['RaceTable']['Race'])

    # Converting practices and quali functions
    col_list = ['FirstPractice', 'SecondPractice', 'ThirdPractice', 'Qualifying', 'Sprint']
    [practices_quali(i) for i in col_list];

    # Splitting 'Circuit' column for circuit information
    races['CircuitID'] = races['Circuit'].transform(lambda x: x['@circuitId'])
    races['CircuitName'] = races['Circuit'].transform(lambda x: x['CircuitName'])
    races['Locality'] = races['Circuit'].transform(lambda x: x['Location']['Locality'])
    races['Country'] = races['Circuit'].transform(lambda x: x['Location']['Country'])

    # Renaming columns
    races.rename(columns={"@season": "Season", "@round": "round", "Date": "Race"}, errors="raise", inplace=True)

    # Concatenating data frames
    races = pd.concat([races, races_ap], ignore_index=True)
    races_ap = races.copy()

# Empty DF for appending purposes
races_ap = pd.DataFrame()
# Reading seasons from 1950 to 2022
[season_reader(season) for season in range(1950, 2023)];
# Dropping unnecesary columns
races.drop(columns=['@url', 'Circuit', 'Time'], inplace=True)
#Converting datetime columns to datetime
dt_list = ['Race', 'FirstPractice', 'SecondPractice', 'ThirdPractice', 'Qualifying', 'Sprint']
races[dt_list] = races[dt_list].apply(pd.to_datetime, errors='coerce')

return races