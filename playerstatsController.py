from flask_restful import Resource
from flask import jsonify
from flask import Response
from playerstats_scraper import PlayerStats_Finder

class PlayerStats(Resource):
      
      def get(self,matchid): 
        if matchid:
            playerstatsobj = PlayerStats_Finder()
            result = playerstatsobj.find_playerstats(matchid)
            if result:
                 response = Response("CSV succesfully exported", status=200, content_type='text/plain')
            else:
                return jsonify({'error': 'Match ID not found for the given search query.'}), 404
        else:
            return jsonify({'error': 'Invalid request body. Missing matchid field.'}), 400
        
        return response