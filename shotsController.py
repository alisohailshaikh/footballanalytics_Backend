from flask_restful import Resource
from flask import jsonify
from flask import Response
from shot_scraper import Shots_Finder

class PlayerShots(Resource):

    def get(self,matchid):
        if matchid:
            playershotsobj = Shots_Finder()
            result = playershotsobj.find_Shots(matchid)
            if result:
                 response = Response("CSV succesfully exported", status=200, content_type='text/plain')
            else:
                return jsonify({'error': 'Match ID not found for the given search query.'}), 404
        else:
            return jsonify({'error': 'Invalid request body. Missing matchid field.'}), 400
        
        return response