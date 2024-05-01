from flask_restful import Resource
from flask import jsonify
from flask import Response
from flask import request
import pyodbc
import bcrypt
import jwt
from dotenv import load_dotenv
import os

load_dotenv()


class Users(Resource):
    def post(self):
        json_body = request.json
        if 'username' in json_body and 'user_email' in json_body and 'user_password' in json_body:
            return self.register()
        elif 'user_email' in json_body and 'user_password' in json_body:
            return self.login()
        else:
            response = Response("Missing arguments", status=400, content_type='text/plain')
            return response
        
    def login(self):
        load_dotenv()
        username = os.environ['username']
        password = os.environ['password'] 
        server = os.environ['server']
        database = os.environ['database'] 
        driver = os.environ['driver']

        cxnstring = (f"Driver={driver};"
                    f"Server={server};"
                    f"Database={database};"
                    f"UID={username};"
                    f"PWD={password};")
    
        
        cxn = pyodbc.connect(cxnstring)
        cursor = cxn.cursor()
        
        #parsing through json request body
        json_body = request.json
        email = json_body.get('user_email')
        password = json_body.get('user_password')
        if not all([password, email]):
             response = Response("missing arguements", status=404, content_type='text/plain')
             return response
        
        #checking for email 
        sql = "SELECT user_password FROM users WHERE user_email = ?"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if (result is None):
            response = Response("error", status=404, content_type='text/plain')
            return response


        if bcrypt.checkpw(password.encode('utf-8'),result[0].encode('utf-8')):
            sql = "SELECT username FROM users WHERE user_email = ?"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
            SECRET_KEY = os.environ.get('SECRET_KEY')
            payload = {
                'username': result[0],
                'user_email': email,
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            response = Response(token, status=200, content_type='text/plain')
            return response
        else:
            response = Response("error", status=404, content_type='text/plain')
            return response
            
    
    def register(self):

        load_dotenv()
        username = os.environ['username']
        password = os.environ['password'] 
        server = os.environ['server']
        database = os.environ['database'] 
        driver = os.environ['driver']

        cxnstring = (f"Driver={driver};"
                    f"Server={server};"
                    f"Database={database};"
                    f"UID={username};"
                    f"PWD={password};")

        cxn = pyodbc.connect(cxnstring)
        cursor = cxn.cursor()

        #parsing through json request body
        json_body = request.json
        name = json_body.get('username')
        email = json_body.get('user_email')
        password = json_body.get('user_password')
        if not all([name, password, email]):
             response = Response("missing arguements", status=404, content_type='text/plain')
             return response
        
        #checking for email 
        sql = "SELECT user_email FROM users WHERE user_email = ?"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result is not None:
            response = Response("email already exists", status=404, content_type='text/plain')
            return response
        
        #hash password
        salt = bcrypt.gensalt(10)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        
        #registering
        sql = "INSERT INTO users (username, user_email, user_password) VALUES (?, ?, ?)"
        result = cursor.execute(sql, (name, email, hashed_password))
        if result:
            response = Response("Query successfully run", status=200, content_type='text/plain')
            cxn.commit()
        else:
            return jsonify({'error': 'Query did not work'}), 404
        
        return response
            

