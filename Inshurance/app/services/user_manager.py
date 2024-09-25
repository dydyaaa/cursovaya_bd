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
            return jsonify({"result": "Вы уже подали заявку!"}), 400
        
        query = """SELECT * FROM Clients WHERE passport_series = %s AND passport_number = %s"""
        params = (passport_series, passport_number)
        result = execute_query(query, params)
        
        if result:
            return jsonify({"result": "Пользователь с таким паспортом уже зарегистрирован!"}), 400
        
        query = """SELECT * FROM Clients WHERE contact_number = %s"""
        params = (contact_number, )
        result = execute_query(query, params)
        
        if result:
            return jsonify({"result": "Пользователь с таким номером уже зарегистрирован!"}), 400
    
        birth_date = datetime.datetime.strptime(birth_day, '%Y-%m-%d')
        today = datetime.datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            return jsonify({"result": "Для того, чтобы стать клиентом, Вы дожны быть совершеннолетним!"}), 400
            
        query = """INSERT INTO Clients (client_name, birth_day, passport_series, passport_number, contact_number, address, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (client_name, birth_day, passport_series, passport_number, contact_number, address, user_id)
        
        execute_query(query, params)
        
        query = """UPDATE Users SET user_role = %s WHERE user_id = %s"""
        params = ('Client', user_id)
        
        execute_query(query, params)
        
        return jsonify({"result": "ok"}), 200


    def change_client_data(data, current_user):
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
            return jsonify({"result": "Пользователь с таким паспортом уже зарегистрирован!"}), 400
        
        query = """SELECT * FROM Clients WHERE contact_number = %s AND user_id != %s"""
        params = (contact_number, user_id)
        result = execute_query(query, params)
        
        if result:
            return jsonify({"result": "Пользователь с таким номером уже зарегистрирован!"}), 400
    
        birth_date = datetime.datetime.strptime(birth_day, '%Y-%m-%d')
        today = datetime.datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            return jsonify({"result": "Для того, чтобы стать клиентом, Вы дожны быть совершеннолетним!"}), 400
            
        
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
            client[0]['birth_day'] = client[0]['birth_day'].strftime('%Y.%m.%d')
        else:
            client = None
        return jsonify({"result": current_user, "client": client}), 200
    
    
    def calculator(policy_type, 
                   date_start,
                   date_stop,
                   car_brand,
                   year_of_manufacture,
                   sum_insurance):
        
        result = UserManager.calculation(policy_type, 
                                         date_start,
                                         date_stop,
                                         car_brand,
                                         year_of_manufacture,
                                         sum_insurance)
        
        return jsonify({"result": result})
    
    @staticmethod
    def calculation(policy_type, date_start, date_stop, car_brand, year_of_manufacture, sum_insurance):
        
        policy_coefficients = {
            'ОСАГО': 1.2,
            'КАСКО': 1.5
        }
        
        brand_coefficients = {
        'BMW': 1.1,
        'MERCEDES': 1.2,
        'AUDI': 1.15,
        'TOYOTA': 1.0,
        'HONDA': 1.05,
        'FORD': 1.0,
        'CHEVROLET': 1.0,
        'TESLA': 1.3,
        'VOLKSWAGEN': 1.1,
        'PORSCHE': 1.4,
        'LEXUS': 1.25,
        'NISSAN': 1.05,
        'HYUNDAI': 1.0,
        'KIA': 1.0,
        'VOLVO': 1.2,
        'JAGUAR': 1.35,
        'LAND ROVER': 1.3,
        'MAZDA': 1.05,
        'SUBARU': 1.1,
        'FERRARI': 1.5
    }

        
        if policy_type not in policy_coefficients:
            jsonify({"result": f"Неподдерживаемый тип полиса"}), 400 
    
        if car_brand not in brand_coefficients:
            jsonify({"result": f"Неподдерживаемая марка автомобиля"}), 400
            
        try:
            year_of_manufacture = int(year_of_manufacture)
        except ValueError:
            return jsonify({"result": f"Некорректный год выпуска автомобиля"}), 400
        
        base_cost = sum_insurance * 0.03
        
        policy_coefficient = policy_coefficients[policy_type]
        brand_coefficient = brand_coefficients[car_brand]
        
        current_year = datetime.datetime.now().year
        age_of_car = current_year - year_of_manufacture
        
        age_coefficient = 1.5 if age_of_car > 5 else 1.2 if age_of_car > 3 else 1.0
        
        total_cost = base_cost * policy_coefficient * brand_coefficient * age_coefficient
        
        if isinstance(date_start, str):
            date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
        if isinstance(date_stop, str):
            date_stop = datetime.datetime.strptime(date_stop, '%Y-%m-%d')
        period_in_years = (date_stop - date_start).days / 365.0
        
        if period_in_years < 1:
            total_cost *= 1.2  
        elif period_in_years > 3:
            total_cost *= 0.8  
    
        total_cost *= period_in_years
        
        total_cost = round(total_cost, 0)
        
        return total_cost
    
    
    def test_route():
        
        query = "SELECT * FROM Users"
        result = execute_query(query)
        
        return jsonify({"result": result}), 200
    
    @staticmethod
    def create_token(user_login):
        
        payload = {
            'user_login': user_login,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)  
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return token