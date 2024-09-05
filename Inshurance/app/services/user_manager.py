import datetime
import jwt
from app.utils import execute_query
from flask import current_app as app


class UserManager():
    
    def register_agent():
        pass
    
    
    def register_client(user_login):
        
        query = f'SELECT * FROM Users WHERE user_login={user_login}'
        result = execute_query(query)
    
    
    def login():
        pass
    
    
    @staticmethod
    def create_token(user_login):
        
        payload = {
            'username': user_login,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)  
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return token