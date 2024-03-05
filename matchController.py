from flask_restful import Resource
from flask import jsonify, request 
from match_scaper import MatchIDFinder


class getMatchID(Resource): 
    
    def post(self): 
        search_query = request.json.get('search_query')
        if search_query:
            match = MatchIDFinder()
            match_id = match.find_match_id(search_query)
            if match_id:
                return jsonify(match_id)
            else:
                return jsonify({'error': 'Match ID not found for the given search query.'}), 404
        else:
            return jsonify({'error': 'Invalid request body. Missing "search_query" field.'}), 400
    
  