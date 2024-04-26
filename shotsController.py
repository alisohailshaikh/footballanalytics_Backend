from flask_restful import Resource
from flask import jsonify
from flask import Response
from shot_scraper import Shots_Finder
from flask_cors import CORS, cross_origin

class PlayerShots(Resource):
    @cross_origin()
    def get(self,matchid):
        if matchid:
            playershotsobj = Shots_Finder()
            result = playershotsobj.find_Shots(matchid)
            if result:
                 response = Response("CSV succesfully exported", status=200, content_type='text/plain')
            else:
                response = Response("No match ID found for search query", status=404, content_type='text/plain')
        else:
            response = Response("Invalid request body", status=400, content_type='text/plain')
        
        return response