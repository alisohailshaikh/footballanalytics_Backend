from flask_restful import Resource
from flask import jsonify
from flask import Response
from stats_scraper import Stats_Finder

class Stats(Resource):
      
      def get(self,matchid): 
        if matchid:
            obj = Stats_Finder()
            result = obj.find_stats(matchid)
            if result:
                 response = Response("CSV succesfully exported", status=200, content_type='text/plain')
            else:
                response = Response("No match ID found for search query", status=404, content_type='text/plain')
        else:
            response = Response("Invalid request body", status=400, content_type='text/plain')
        
        return response