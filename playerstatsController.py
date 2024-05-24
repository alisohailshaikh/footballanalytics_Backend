from flask_restful import Resource
from flask import jsonify
from flask import Response
from playerstats_scraper import PlayerStats_Finder
from flask_cors import CORS, cross_origin
class PlayerStats(Resource):
      @cross_origin()
      def get(self,matchid): 
        if matchid:
            playerstatsobj = PlayerStats_Finder()
            result = playerstatsobj.find_playerstats(matchid)
            if result:
                 response = Response("CSV succesfully exported from player stats", status=200, content_type='text/plain')
            else:
                 response = Response("Cannot write to csv", status=400, content_type='text/plain')
        else:
           response = Response("error", status=404, content_type='text/plain')
        
        return response