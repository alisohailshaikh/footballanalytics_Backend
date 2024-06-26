from flask import Flask
from flask_restful import Api 
import matchController
import playerstatsController
import shotsController
import avposController
import statsController
import userController
import overview_controller
from flask_cors import CORS


app = Flask(__name__) 
cors = CORS(app)
api = Api(app) 
app.config['CORS_HEADERS'] = 'Content-Type'

  
api.add_resource(matchController.getMatchID, '/matchid') 
api.add_resource(playerstatsController.PlayerStats, '/playerstats/<matchid>')
api.add_resource(shotsController.PlayerShots, '/playershots/<matchid>')
api.add_resource(avposController.PlayerAvgPos, '/avgpos/<matchid>')
api.add_resource(statsController.Stats, '/stats/<matchid>')
api.add_resource(userController.Users,'/users')
api.add_resource(overview_controller.Overview,'/overview/<matchid>')
  

if __name__ == '__main__': 
  
    app.run(debug = True) 