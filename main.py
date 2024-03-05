from flask import Flask
from flask_restful import Api 
import matchController
import playerstatsController
import shotsController
import avposController
import statsController

app = Flask(__name__) 
api = Api(app) 
  
api.add_resource(matchController.getMatchID, '/matchid') 
api.add_resource(playerstatsController.PlayerStats, '/playerstats/<matchid>')
api.add_resource(shotsController.PlayerShots, '/playershots/<matchid>')
api.add_resource(avposController.PlayerAvgPos, '/avgpos/<matchid>')
api.add_resource(statsController.Stats, '/stats/<matchid>')
  

if __name__ == '__main__': 
  
    app.run(debug = True) 