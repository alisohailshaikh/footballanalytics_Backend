import requests 
import datetime
import pandas as pd
import math
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

class Shots_Finder:
    headers= []

    def __init__(self):
        self.headers = {
            'authority': 'api.sofascore.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'if-none-match': 'W/"ec2fea3514"',
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

    def find_Shots(self,matchid):
        link = f"https://api.sofascore.com/api/v1/event/{matchid}/shotmap"
        response = requests.get(link, headers=self.headers) 
        shots = response.json()
        df = pd.DataFrame(shots['shotmap'])
        df[['name', 'position', 'jerseyNumber']] = df['player'].apply(lambda x: pd.Series({'name': x['name'], 'position': x['position'], 'jerseyNumber': x['jerseyNumber']}))
        df.drop('player', axis=1, inplace=True)
        cols = df.columns.tolist()
        cols = cols[-3:] + cols[:-3]
        df = df[cols]
        df[['xCoord', 'yCoord']] = df['playerCoordinates'].apply(lambda x: pd.Series({'x': x['x'], 'y': x['y']}))
        df.drop('playerCoordinates', axis=1, inplace=True)
        df[['GoalMouthxCoord', 'GoalMouthyCoord', 'GoalMouthzCoord']] = df['goalMouthCoordinates'].apply(lambda x: pd.Series({'x': x['x'], 'y': x['y'], 'z': x['z']}))
        df.drop('goalMouthCoordinates', axis=1, inplace=True)
        df[['BlockxCoord', 'BlockyCoord']] = df['blockCoordinates'].apply(lambda x: pd.Series({'x': x['x'], 'y': x['y']}) if isinstance(x, dict) else pd.Series({'x': pd.NA, 'y': pd.NA}))
        df.drop('blockCoordinates', axis=1, inplace=True)
        df.drop('id', axis=1, inplace=True)
        df['Minute'] = df['timeSeconds'].apply(lambda x: math.ceil(x/60))
        df.drop('timeSeconds', axis=1, inplace=True)
        df.drop('time', axis=1, inplace=True)
        df.drop('addedTime', axis=1, inplace=True)
        df.drop('reversedPeriodTime', axis=1, inplace=True)
        df.drop('reversedPeriodTimeSeconds', axis=1, inplace=True)
        df[['EndLocation']] = df['draw'].apply(lambda x: pd.Series({'end': x['end']}))
        df.drop('draw', axis=1, inplace=True)
        df[['EndLocxCoord', 'EndLocyCoord']] = df['EndLocation'].apply(lambda x: pd.Series({'x': x['x'], 'y': x['y']}))
        df.drop('EndLocation', axis=1, inplace=True)
        
        df['match_id'] = matchid
        
        try:
            load_dotenv()
            username = os.environ['username']
            password = os.environ['password'] 
            server = os.environ['server']
            database = os.environ['database'] 
            driver = os.environ['driver']


            conn_str = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

            engine = create_engine(conn_str)

            df.to_sql(name='shots',con=engine,if_exists='replace')
            msg = True
        except Exception as e:
            print(f"Error occurred while writing to CSV: {e}")
            msg = False


        return msg


