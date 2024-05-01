import requests 
import datetime
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


class PlayerStats_Finder:
    headers = []

    def __init__(self):
        self.headers = {
            'authority': 'api.sofascore.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'if-none-match': 'W/"ae3bef61a0"',
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

    def find_playerstats(self,matchid):
        link = f"https://api.sofascore.com/api/v1/event/{matchid}/lineups"
        response = requests.get(link, headers=self.headers)
        pstats=response.json()
        for x in pstats:
            print(x)
            if x == 'home':
                for y in pstats[x]['players']:
                    y['type'] = 'home'
                    print(y)
            elif x == 'away':
                for y in pstats[x]['players']:
                    y['type'] = 'away'
                    print(y)
        
        allP=pstats['home']['players'] + pstats['away']['players']
        df= pd.DataFrame(allP)

        df[['name', 'ID']] = df['player'].apply(lambda x: pd.Series({'name': x['name'], 'id': x['id']}) if isinstance(x, dict) else pd.Series({'name': None, 'id': None, 'jerseyNumber': None}))
        df.drop('player', axis=1, inplace=True)
        cols = df.columns.tolist()
        cols = cols[-2:] + cols[:-2]
        df = df[cols]

        df[['totalPass', 'accuratePass', 'totalLongBalls', 'accurateLongBalls', 'savedShotsFromInsideTheBox', 'saves', 'minutesPlayed', 'touches', 'rating', 'possessionLostCtrl', 'ratingVersions', 'goalsPrevented']] = df['statistics'].apply(lambda x: pd.Series({'totalPass': x.get('totalPass'), 'accuratePass': x.get('accuratePass'), 'totalLongBalls': x.get('totalLongBalls'), 'accurateLongBalls': x.get('accurateLongBalls'), 'savedShotsFromInsideTheBox': x.get('savedShotsFromInsideTheBox'), 'saves': x.get('saves'), 'minutesPlayed': x.get('minutesPlayed'), 'touches': x.get('touches'), 'rating': x.get('rating'), 'possessionLostCtrl': x.get('possessionLostCtrl'), 'ratingVersions': x.get('ratingVersions'), 'goalsPrevented': x.get('goalsPrevented')}) if isinstance(x, dict) else pd.Series({'name': None, 'position': None, 'jerseyNumber': None, 'savedShotsFromInsideTheBox': None, 'saves': None, 'minutesPlayed': None, 'touches': None, 'rating': None, 'possessionLostCtrl': None, 'ratingVersions': None, 'goalsPrevented': None}))  
        df.drop('statistics', axis=1, inplace=True)

        df.drop('ratingVersions', axis=1, inplace=True)
        df.drop('jerseyNumber', axis=1, inplace=True)

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
        

            df.to_sql(name='player_stats',con=engine,if_exists='replace')
            msg = True
        except Exception as e:
            print(f"Error occurred while writing to CSV: {e}")
            msg = False


        return msg
    