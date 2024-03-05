from flask_restful import Resource
from flask import jsonify
from flask import Response
from avgpos_scraper import AvgPos_Finder

class PlayerAvgPos(Resource):
      
      def get(self,matchid): 
        if matchid:
            obj = AvgPos_Finder()
            result = obj.find_avgpos(matchid)
            if result:
                 response = Response("CSV succesfully exported", status=200, content_type='text/plain')
            else:
                return jsonify({'error': 'Match ID not found for the given search query.'}), 404
        else:
            return jsonify({'error': 'Invalid request body. Missing matchid field.'}), 400
        
        return response