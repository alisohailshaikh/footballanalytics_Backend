import requests 
import datetime
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pyodbc

class Stats_Finder:
    headers = []

    def __init__(self):
        self.headers = {
            'authority': 'api.sofascore.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'if-none-match': 'W/"adef37e0f6"',
            'origin': 'https://www.sofascore.com',
            'referer': 'https://www.sofascore.com/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }

        self.headers['If-Modified-Since']= datetime.datetime.now().isoformat()

    def find_stats(self,matchid):
        link = f"https://api.sofascore.com/api/v1/event/{matchid}/statistics"
        response = requests.get(link, headers=self.headers)
        stats = response.json()
        stats1 = [x for x in stats['statistics'] if x['period'] != 'a']
        for x in stats1:
            print(x['period'])
            if x['period'] == '1ST':
                for y in x['groups']:
                    y['period'] = '1st'
            elif x['period'] == '2ND':
                for y in x['groups']:
                    y['period'] = '2nd'
            elif x['period'] == 'ALL':
                for y in x['groups']:
                    y['period'] = 'ALL'
        
        stats1 = stats1[0]['groups'] + stats1[1]['groups'] + stats1[2]['groups']
        dataframes_by_group = {}

        for stats_group in stats1:
            group_name = stats_group['groupName']
            statistics_items = stats_group['statisticsItems']
            period = stats_group['period']

            df = pd.DataFrame(statistics_items)
            df['period'] = period

            if group_name in dataframes_by_group:
                dataframes_by_group[group_name] = pd.concat([dataframes_by_group[group_name], df])
            else:
                dataframes_by_group[group_name] = df

        dataframes_by_group['Shots'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue'], inplace = True)
        dataframes_by_group['Shots'].reset_index(drop=True, inplace=True)
       
        df_Exp = dataframes_by_group['Match overview'][dataframes_by_group['Match overview']['name'].str.contains('Expected goals')]
        df_Exp.reset_index(drop=True, inplace=True)
        df_Exp.drop(columns = ['name', 'compareCode', 'valueType', 'homeValue', 'awayValue'], inplace = True)
     
        df_Pos = dataframes_by_group['Match overview'][dataframes_by_group['Match overview']['name'].str.contains('Ball possession')]
        df_Pos.drop(columns = ['name', 'compareCode', 'valueType', 'homeValue', 'awayValue', 'statisticsType'], inplace = True)
        df_Pos.reset_index(drop=True, inplace=True)

        dataframes_by_group['Match overview'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue'], inplace = True)

        df_tv=dataframes_by_group['Match overview']
        df_tv = df_tv[(df_tv['name'] != 'Ball possession') & (df_tv['name'] != 'Expected goals')]
        df_tv.reset_index(drop=True, inplace=True)

        dataframes_by_group['Attack'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue'], inplace = True)
        dataframes_by_group['Attack'].reset_index(drop=True, inplace = True)   

        dataframes_by_group['Passes'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue'], inplace = True)
        dataframes_by_group['Passes'].reset_index(drop=True, inplace = True)    

        dataframes_by_group['Passes']['home'] = dataframes_by_group['Passes']['home'].str.split('/').str[0]
        dataframes_by_group['Passes']['away'] = dataframes_by_group['Passes']['away'].str.split('/').str[0]

        #in home and away columns remove values after "/"
        dataframes_by_group['Passes']['home'] = dataframes_by_group['Passes']['home'].str.split('(').str[0]
        dataframes_by_group['Passes']['away'] = dataframes_by_group['Passes']['away'].str.split('(').str[0]

        
        dataframes_by_group['Duels']['home'] = dataframes_by_group['Duels']['home'].str.split('/').str[0]
        dataframes_by_group['Duels']['away'] = dataframes_by_group['Duels']['away'].str.split('/').str[0]

        dataframes_by_group['Duels'].reset_index(drop=True, inplace = True) 

        df_Duels = dataframes_by_group['Duels'][dataframes_by_group['Duels']['name'] == 'Duels']
        df_Duels.drop(columns = ['compareCode', 'valueType', 'home', 'away'], inplace = True)
        df_Duels.reset_index(drop=True, inplace = True)

        dataframes_by_group['Duels'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue'], inplace = True)
        dataframes_by_group['Duels'].reset_index(drop=True, inplace = True) 
        #remove rows where name = Duels
        dataframes_by_group['Duels'] = dataframes_by_group['Duels'][dataframes_by_group['Duels']['name'] != 'Duels']
     
    
        

        df_TacklesWon = dataframes_by_group['Defending'][dataframes_by_group['Defending']['name'] == 'Tackles won']

        df_TacklesWon.drop(columns = ['compareCode', 'valueType', 'home', 'away'], inplace = True)
        df_TacklesWon.reset_index(drop=True, inplace = True)

        dataframes_by_group['Defending'] = dataframes_by_group['Defending'][dataframes_by_group['Defending']['name']!='Tackles won']
        dataframes_by_group['Defending'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue', 'statisticsType'], inplace = True)

        dataframes_by_group['Defending'].reset_index(drop=True, inplace = True) 
        #run this
        dataframes_by_group['Defending'] = dataframes_by_group['Defending'][dataframes_by_group['Defending']['period'] != 'ALL']
        df_TacklesWon = df_TacklesWon[df_TacklesWon['period'] != 'ALL']

        df_Duels = df_Duels[df_Duels['period'] != 'ALL']




        shots = dataframes_by_group['Shots']
        passes = dataframes_by_group['Passes']
        duels = dataframes_by_group['Duels']
        defending = dataframes_by_group['Defending']
        shotsextra = dataframes_by_group['Attack']

        frames = [shots, df_tv, shotsextra, passes, duels, defending]
        totalstats = pd.concat(frames)

        cards = totalstats[(totalstats['name'] == 'Fouls')]

        totalstats = totalstats[(totalstats['period'] != 'ALL')]

        if "Red cards" not in totalstats["name"].values:
    # Create a row where name is 'Red Cards' and period is '1st' and '2nd' and all rest are 0, statistic type is negative
            red_cards = pd.DataFrame({'name': ['Red cards'], 'home': [0], 'away': [0], 'period': ['1st'], 'statisticsType': ['negative']})
            red_cards = pd.DataFrame({'name': ['Red cards'], 'home': [0], 'away': [0], 'period': ['2nd'], 'statisticsType': ['negative']})
            totalstats = pd.concat([totalstats, red_cards], ignore_index=True)
        # Check if "Red Cards" column already exists
        if "Yellow cards" not in totalstats["name"].values:
            # Create a row where name is 'Red Cards' and period is '1st' and '2nd' and all rest are 0, statistic type is negative
            y_cards = pd.DataFrame({'name': ['Yellow cards'], 'home': [0], 'away': [0], 'period': ['1st'], 'statisticsType': ['negative']})
            y_cards = pd.DataFrame({'name': ['Yellow cards'], 'home': [0], 'away': [0], 'period': ['2nd'], 'statisticsType': ['negative']})
            totalstats = pd.concat([totalstats, y_cards], ignore_index=True)


        df_Exp['matchid'] = matchid
        df_Pos['matchid'] = matchid
        totalstats['matchid'] = matchid
        cards['matchid'] = matchid
        df_TacklesWon['matchid'] = matchid
        df_Duels['matchid'] = matchid

        try:
            load_dotenv()
            username = os.environ['usernamemysql']
            password = os.environ['passwordmysql'] 
            server = os.environ['servermysql']
            database = os.environ['databasemysql'] 
            driver = os.environ['drivermysql']

            engine = create_engine(f'mysql+pymysql://{username}:{password}@{server}/{database}')
        

            df_Exp.to_sql(name='expected',con=engine,if_exists='replace')
            df_Pos.to_sql(name='possession',con=engine,if_exists='replace')
            totalstats.to_sql(name='totalstats',con=engine,if_exists='replace')
            cards.to_sql(name='cards',con=engine,if_exists='replace')
            df_TacklesWon.to_sql(name='tackleswon_stats',con=engine,if_exists='replace')
            df_Duels.to_sql(name='duels_stats',con=engine,if_exists='replace')

            
        
            msg = True
        except Exception as e:
            print(f"Error occurred while writing to CSV: {e}")
            msg = False


        return msg


            
