from flask_restful import Resource
from flask import jsonify
from flask import Response
from avgpos_scraper import AvgPos_Finder
from flask_cors import CORS, cross_origin

class PlayerAvgPos(Resource):
      @cross_origin()
      def get(self,matchid): 
        if matchid:
            obj = AvgPos_Finder()
            result = obj.find_avgpos(matchid)
            if result:
                 response = Response("csv exported successfully from avg pos", status=200, content_type='text/plain')
            else:
                return jsonify({'error': 'Match ID not found for the given search query.'}), 404
        else:
            return jsonify({'error': 'Invalid request body. Missing matchid field.'}), 400
        
        return response