import datetime
import jwt
from app.utils import execute_query
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from flask import jsonify


class UserManager:
    
    def register(user_login, password):
        
        query = "SELECT * FROM Users WHERE user_login = %s"
        params = (f'{user_login}',)
        result = execute_query(query, params)
        if not result:
            
            password_hash = generate_password_hash(password)
            
            query = "INSERT INTO Users (user_login, password_hash) VALUES (%s, %s)"
            params = (f'{user_login}', f'{password_hash}')
            result = execute_query(query, params)
            
            token = UserManager.create_token(user_login)
            
            return jsonify({"result": "registered", "token": token}), 200
        else:
            return jsonify({"result": "Пользователь с таким логином уже существует!"}), 400
    
    
    def login(user_login, password):
        
        query = "SELECT * FROM Users WHERE user_login = %s"
        params = (f'{user_login}',)
        result = execute_query(query, params, return_json=True)
        
        if not result:
            return jsonify({"result": "Пользователя с таким логином не существует!"}), 400
        
        else:
            if check_password_hash(result[0]['password_hash'], password):
                token = UserManager.create_token(user_login)
                return jsonify({"result": "Авториязация успешна", "token": token}), 200
            else:
                return jsonify({"result": "Неверный пароль!"}), 400
    
    
    def change_password(current_user, password):
        
        password_hash = generate_password_hash(password)
        query = "UPDATE Users SET password_hash = %s WHERE user_id = %s"
        params = (password_hash, current_user[0]['user_id'])
        execute_query(query, params)
        
        return jsonify({"result": "Пароль успешно сменен"})
    
    
    @staticmethod
    def create_token(user_login):
        
        payload = {
            'user_login': user_login,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)  
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return token