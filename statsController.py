from flask_restful import Resource
from flask import jsonify
from flask import Response
from stats_scraper import Stats_Finder
from flask_cors import CORS, cross_origin

class Stats(Resource):
      @cross_origin()
      def get(self,matchid): 
        if matchid:
            obj = Stats_Finder()
            result = obj.find_stats(matchid)
            if result:
                 response = Response("CSV succesfully exported from stats", status=200, content_type='text/plain')
                 response.headers.add("Access-Control-Allow-Origin", "*")
            else:
                response = Response("No match ID found for search query", status=404, content_type='text/plain')
        else:
            response = Response("Invalid request body", status=400, content_type='text/plain')
        
        return response