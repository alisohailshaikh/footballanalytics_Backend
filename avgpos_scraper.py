import requests 
import datetime
import pandas as pd
import pyodbc
from sqlalchemy import create_engine

class AvgPos_Finder:
    headers = []

    def __init__(self):
        self.headers = {
            'authority': 'api.sofascore.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
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

    def find_avgpos(self,matchid):
            link = f"https://api.sofascore.com/api/v1/event/{matchid}/average-positions"
            response = requests.get(link, headers=self.headers)
            positions= response.json()

            for x in positions:
                print(x)
                if x=='home':
                    for y in positions[x]:
                        y['type']='home'
                        print(y)
                elif x=='away':
                    for y in positions[x]:
                        y['type']='away'
                        print(y)
                else:
                    for y in positions[x]:
                        y['type']='subs'

            all_positions= positions['home']+positions['away']+positions['substitutions']
            df= pd.DataFrame(all_positions)
            df[['name', 'position', 'jerseyNumber']] = df['player'].apply(lambda x: pd.Series({'name': x['name'], 'position': x['position'], 'jerseyNumber': x['jerseyNumber']}) if isinstance(x, dict) else pd.Series({'name': None, 'position': None, 'jerseyNumber': None}))
            df.drop('player', axis=1, inplace=True)
            cols = df.columns.tolist()
            cols = cols[-3:] + cols[:-3]
            df = df[cols]
            df[['PlayerInname', 'PlayerInposition', 'PlayerInjerseyNumber']] = df['playerIn'].apply(lambda x: pd.Series({'name': x['name'], 'position': x['position'], 'jerseyNumber': x['jerseyNumber']}) if isinstance(x, dict) else pd.Series({'name': None, 'position': None, 'jerseyNumber': None}))
            df.drop('playerIn', axis=1, inplace=True)
            df[['PlayerOutname', 'PlayerOutposition', 'PlayerOutjerseyNumber']] = df['playerOut'].apply(lambda x: pd.Series({'name': x['name'], 'position': x['position'], 'jerseyNumber': x['jerseyNumber']}) if isinstance(x, dict) else pd.Series({'name': None, 'position': None, 'jerseyNumber': None}))
            df.drop('playerOut', axis=1, inplace=True)
            df[df['type']=='subs']
            df['subbedIn']= df['name'].isin(df['PlayerInname'])
            df.drop('isHome', axis=1, inplace=True)
            df.drop('incidentType', axis=1, inplace=True)
            df.drop(['PlayerInname', 'PlayerInposition', 'PlayerInjerseyNumber', 'PlayerOutname', 'PlayerOutposition', 'PlayerOutjerseyNumber'], axis=1, inplace=True)
            df= df.dropna(axis=1, how='all')
            df= df[df['type']!='subs']

            df['match_id'] = matchid

            cxnstring = ("Driver={ODBC Driver 17 for SQL Server};"
                    "Server=DESKTOP-PSGPR9D\\SQLEXPRESS;"
                    "Database=FootballAnalytics;"
                    "Trusted_Connection=yes;")
            cxn = pyodbc.connect(cxnstring)
            cursor = cxn.cursor()

            engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % cxnstring)

            df.to_sql(name='avg_positions',con=engine,if_exists='replace')


            try:
                # df.to_csv('avg_positions.csv', index=False)
                msg = True
            except Exception as e:
                print(f"Error occurred while writing to CSV: {e}")
                msg = False
            return msg


