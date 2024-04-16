import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

payload = {
    'user_id': 123,
    'username': 'example_user',
}

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFsaSIsInVzZXJfZW1haWwiOiJhbGluZXd1c2VyQGdtYWlsLmNvbSJ9.mr7qSYPT4yyV32q6fVI9jRl5lK_FSNZofhZJivQbFLE'

try:
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    print("Decoded Payload:", decoded_payload)
except jwt.ExpiredSignatureError:
    print("Token has expired.")
except jwt.InvalidTokenError:
    print("Invalid token.")