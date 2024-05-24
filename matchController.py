from flask_restful import Resource
from flask import jsonify, request 
from flask import Response
from match_scaper import MatchIDFinder



class getMatchID(Resource): 
    
    def post(self): 
        search_query = request.json.get('search_query')
        if search_query:
            match = MatchIDFinder()
            match_id = match.find_match_id(search_query)
            if match_id:
                response = Response(match_id, status=200, content_type='text/plain')
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response
            else:
                return Response("Match id not found", status=404, content_type='text/plain')
        else:
            return Response("wrong query", status=400, content_type='text/plain')
    
  