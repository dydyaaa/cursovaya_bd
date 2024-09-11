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
                return jsonify({"result": "Неверный пароль!"}), 403
            
    
    def become_client(data, current_user):
    
        birth_day = data.get('birth_day')
        client_name = data.get('client_name')
        passport_series = data.get('passport_series')
        passport_number = data.get('passport_number')
        contact_number = data.get('contact_number')
        address = data.get('address')
        user_id = current_user[0].get('user_id')
        
        query = """SELECT * FROM Clients WHERE user_id = %s"""
        params = (user_id,)
        result = execute_query(query, params)
        
        if result:
            return jsonify({"result": "Вы уже подали заявку!"}), 403
        
        query = """SELECT * FROM Clients WHERE passport_series = %s AND passport_number = %s"""
        params = (passport_series, passport_number)
        result = execute_query(query, params)
        
        if result:
            return jsonify({"result": "Пользователь с таким паспортом уже зарегистрирован!"}), 403
        
        query = """SELECT * FROM Clients WHERE contact_number = %s"""
        params = (contact_number, )
        result = execute_query(query, params)
        
        if result:
            return jsonify({"result": "Пользователь с таким номером уже зарегистрирован!"}), 403
    
        birth_date = datetime.datetime.strptime(birth_day, '%Y-%m-%d')
        today = datetime.datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            return jsonify({"result": "Для того, чтобы стать клиентом, Вы дожны быть совершеннолетним!"}), 403
            
        query = """INSERT INTO Clients (client_name, birth_day, passport_series, passport_number, contact_number, address, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (client_name, birth_day, passport_series, passport_number, contact_number, address, user_id)
        
        execute_query(query, params)
        
        query = """UPDATE Users SET user_role = %s WHERE user_id = %s"""
        params = ('Client', user_id)
        
        execute_query(query, params)
        
        return jsonify({"result": "ok"}), 200


    def change_client_data(data, current_user):
        print('DEBUUUUUG')
        birth_day = data.get('birth_day')
        client_name = data.get('client_name')
        passport_series = data.get('passport_series')
        passport_number = data.get('passport_number')
        contact_number = data.get('contact_number')
        address = data.get('address')
        user_id = current_user[0].get('user_id')
        
        query = """SELECT * FROM Clients WHERE passport_series = %s AND passport_number = %s AND user_id != %s"""
        params = (passport_series, passport_number, user_id)
        result = execute_query(query, params)
        
        if result:
            return jsonify({"result": "Пользователь с таким паспортом уже зарегистрирован!"}), 403
        
        query = """SELECT * FROM Clients WHERE contact_number = %s AND user_id != %s"""
        params = (contact_number, user_id)
        result = execute_query(query, params)
        
        if result:
            return jsonify({"result": "Пользователь с таким номером уже зарегистрирован!"}), 403
    
        birth_date = datetime.datetime.strptime(birth_day, '%Y-%m-%d')
        today = datetime.datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            return jsonify({"result": "Для того, чтобы стать клиентом, Вы дожны быть совершеннолетним!"}), 403
            
        
        query = """UPDATE Clients 
           SET client_name = %s, 
               birth_day = %s, 
               passport_series = %s, 
               passport_number = %s, 
               contact_number = %s, 
               address = %s, 
               status = %s
           WHERE user_id = %s""" 

        params = (client_name, birth_day, passport_series, passport_number, contact_number, address, 'На проверке', user_id)
        execute_query(query, params)
            
        return jsonify({"result": "ok"}), 200
    
    
    def change_password(current_user, password):
        
        password_hash = generate_password_hash(password)
        query = "UPDATE Users SET password_hash = %s WHERE user_id = %s"
        params = (password_hash, current_user[0]['user_id'])
        execute_query(query, params)
        
        return jsonify({"result": "Пароль успешно сменен"})
    
    
    def profile(current_user):
        
        query = "SELECT * FROM Clients WHERE user_id = %s"
        params = (current_user[0]['user_id'], )
        client = execute_query(query, params, return_json=True)
        if client:
            client[0]['birth_day'] = client[0]['birth_day'].strftime('%d.%m.%Y')
        else:
            client = None
        return jsonify({"result": current_user, "client": client}), 200
    
    
    def calculator(*args):
        
        return jsonify({"result": "Дорого"}), 200
    
    @staticmethod
    def create_token(user_login):
        
        payload = {
            'user_login': user_login,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)  
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return token