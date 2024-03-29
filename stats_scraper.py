import requests 
import datetime
import pandas as pd

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
       
        dataframes_by_group['Expected'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue', 'statisticsType'], inplace = True)
        dataframes_by_group['Expected'].reset_index(drop=True, inplace=True)
     
        dataframes_by_group['Possession']
        dataframes_by_group['Possession'].drop(columns = ['name', 'compareCode', 'valueType', 'homeValue', 'awayValue', 'statisticsType'], inplace = True)
        dataframes_by_group['Possession'].reset_index(drop=True, inplace=True)
    
        dataframes_by_group['TVData'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue'], inplace = True)
        dataframes_by_group['TVData'].reset_index(drop=True, inplace=True)

        dataframes_by_group['Shots extra'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue'], inplace = True)
        dataframes_by_group['Shots extra'].reset_index(drop=True, inplace = True)   

        dataframes_by_group['Passes'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue', 'statisticsType'], inplace = True)
        dataframes_by_group['Passes'].reset_index(drop=True, inplace = True)    

        dataframes_by_group['Passes']['home'] = dataframes_by_group['Passes']['home'].str.split('/').str[0]
        dataframes_by_group['Passes']['away'] = dataframes_by_group['Passes']['away'].str.split('/').str[0]

        dataframes_by_group['Passes']['home'] = dataframes_by_group['Passes']['home'].str.split('(').str[0]
        dataframes_by_group['Passes']['away'] = dataframes_by_group['Passes']['away'].str.split('(').str[0]

        dataframes_by_group['Duels'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue'], inplace = True)
        dataframes_by_group['Duels']['home'] = dataframes_by_group['Duels']['home'].str.split('/').str[0]
        dataframes_by_group['Duels']['away'] = dataframes_by_group['Duels']['away'].str.split('/').str[0]
        dataframes_by_group['Duels'].reset_index(drop=True, inplace = True) 

        dataframes_by_group['Defending'].drop(columns = ['compareCode', 'valueType', 'homeValue', 'awayValue', 'statisticsType'], inplace = True)
        dataframes_by_group['Defending'].reset_index(drop=True, inplace = True) 

        
        shots = dataframes_by_group['Shots']
        expected = dataframes_by_group['Expected']
        possession = dataframes_by_group['Possession']
        tvdata = dataframes_by_group['TVData']
        shotsextra = dataframes_by_group['Shots extra']
        passes = dataframes_by_group['Passes']
        duels = dataframes_by_group['Duels']
        defending = dataframes_by_group['Defending']
        
        try:
            shots.to_csv('stats/shots.csv', index = False)
            expected.to_csv('stats/expected.csv', index = False)
            possession.to_csv('stats/possession.csv', index = False)
            tvdata.to_csv('stats/tvdata.csv', index = False)
            shotsextra.to_csv('stats/shotsextra.csv', index = False)
            passes.to_csv('stats/passes.csv', index = False)
            duels.to_csv('stats/duels.csv', index = False)
            defending.to_csv('stats/defending.csv', index = False)
            msg = True
        except Exception as e:
            print(f"Error occurred while writing to CSV: {e}")
            msg = False


        return msg


            
