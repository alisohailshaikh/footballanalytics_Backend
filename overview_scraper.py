import requests 
import datetime
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pyodbc


class Overview_Finder:
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

    def find_overview(self,matchid):
            response = requests.get(f'https://api.sofascore.com/api/v1/event/{matchid}/incidents', headers=self.headers)
            scores=response.json()
            homescore=scores['incidents'][0]['homeScore']
            awayscore=scores['incidents'][0]['awayScore']

            response = requests.get(f'https://api.sofascore.com/api/v1/event/{matchid}', headers=self.headers)
            info=response.json()
            tourniName=info['event']['tournament']['name']
            countryname=info['event']['tournament']['category']['name']

            season= info['event']['season']['name']
            #only keep last word
            season=season.split()[-1]
            venuecity=info['event']['venue']['city']['name']
            stadium=info['event']['venue']['stadium']['name']
            HomeManger=info['event']['homeTeam']['manager']['name']
            hometeamName=info['event']['homeTeam']['name']
            awayteamName=info['event']['awayTeam']['name']

            if 'awayTeam' in info['event'] and 'manager' in info['event']['awayTeam'] and info['event']['awayTeam']['manager'] is not None:
                AwayManager = info['event']['awayTeam']['manager']['name']
            else:
                AwayManager = "Away Manager"


            df = pd.DataFrame()
            df = pd.concat([df, pd.DataFrame({'homescore': [homescore], 'awayscore': [awayscore], 'tourniName':[tourniName]
                                  , 'countryname': [countryname], 'season': [season], 'venuecity': [venuecity], 'stadium': [stadium], 'HomeManger': [HomeManger], 'hometeamName': [hometeamName], 'awayteamName': [awayteamName], 'AwayManger': [AwayManager]
                                  })], ignore_index=True)
        
            
            load_dotenv()
            username = os.environ['usernamemysql']
            password = os.environ['passwordmysql'] 
            server = os.environ['servermysql']
            database = os.environ['databasemysql'] 
            driver = os.environ['drivermysql']

            engine = create_engine(f'mysql+pymysql://{username}:{password}@{server}/{database}')

            df.to_sql(name='overview',con=engine,if_exists='replace')

            username = os.environ['username']
            password = os.environ['password'] 
            server = os.environ['server']
            database = os.environ['database'] 
            driver = os.environ['driver']

            cxnstring = (f"Driver={driver};"
                        f"Server={server};"
                        f"Database={database};"
                        f"UID={username};"
                        f"PWD={password};")

            cxn = pyodbc.connect(cxnstring)
            cursor = cxn.cursor()

            sql = "insert into triggerforrefresh values ('pls','work','man')"
            cursor.execute(sql)
            cxn.commit()
            


            try:
                # df.to_csv('avg_positions.csv', index=False)
                msg = True
            except Exception as e:
                print(f"Error occurred while writing to CSV: {e}")
                msg = False
            return msg


