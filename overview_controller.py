from flask_restful import Resource
from flask import jsonify
from flask import Response
from overview_scraper import Overview_Finder
from flask_cors import CORS, cross_origin

class Overview(Resource):
      @cross_origin()
      def get(self,matchid): 
        if matchid:
            obj = Overview_Finder()
            result = obj.find_overview(matchid)
            if result:
                 response = Response("csv exported successfully from overview", status=200, content_type='text/plain')
            else:
                return jsonify({'error': 'Match ID not found for the given search query.'}), 404
        else:
            return jsonify({'error': 'Invalid request body. Missing matchid field.'}), 400
        
        return response