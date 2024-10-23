from flask import jsonify
from datetime import datetime
from app.utils import execute_query
from ..services.calculator import Calculator


class ClientManager:
    
    def become_client(client_first_name,
                      client_last_name,
                      client_surname,
                      birth_day,
                      passport_series,
                      passport_number,
                      contact_number,
                      address,
                      client_email,
                      user_id):
        
        query = ''' SELECT * FROM Clients
                    WHERE user_id = %s
                '''
        params = (user_id, )
        
        if execute_query(query, params):
            return jsonify({"result": "Вы уже зарегестрированы!"}), 403
        
        birth_date = datetime.strptime(birth_day, '%Y-%m-%d')
        today = datetime.today()
        
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            return jsonify({"result": "Чтобы стать клиентом, Вы должны быть совершеннолетним!"}), 403
        
        query = ''' 
                SELECT * FROM Clients
                WHERE passport_series = %s AND passport_number = %s;
                '''
                
        params = (passport_series, passport_number)
        if execute_query(query, params):
            return jsonify({"result": "Клиент с таким паспортом уже зарегистрирован!"}), 403
        
        query = '''
                SELECT * FROM Clients
                WHERE contact_number = %s;
                '''
        
        params = (contact_number,)
        if execute_query(query, params):
            return jsonify({"result": "Пользователь с таким номером уже зарегестрирован!"}), 403

        query = ''' 
                SELECT * FROM Clients
                WHERE client_email = %s;
                '''
                
        params = (client_email,)
        if execute_query(query, params):
            return jsonify({"result": "Клиент с таким e-mail уже зарегистрирован!"}), 403
        
        query = '''
                INSERT INTO Clients (
                    client_first_name, 
                    client_last_name, 
                    client_surname, 
                    birth_day, 
                    passport_series, 
                    passport_number, 
                    contact_number, 
                    address, 
                    client_email, 
                    user_id
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                
        params = (client_first_name, client_last_name, client_surname, birth_day, 
                  passport_series, passport_number, contact_number, 
                  address, client_email, user_id)
        
        execute_query(query, params)
        
        query = ''' UPDATE Users
                    SET user_role = 'Client'
                    WHERE user_id = %s
                '''
        
        params = (user_id, )
        
        execute_query(query, params)
        
        return jsonify({"result": "Успешно!"}), 200
    
    def change_client_data(client_first_name,
                           client_last_name,
                           client_surname,
                           birth_day,
                           passport_series,
                           passport_number,
                           contact_number,
                           address,
                           client_email,
                           user_id):
        
        birth_date = datetime.strptime(birth_day, '%Y-%m-%d')
        today = datetime.today()
        
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            return jsonify({"result": "Чтобы стать клиентом, Вы должны быть совершеннолетним!"}), 403
        
        query = ''' 
                SELECT * FROM Clients
                WHERE passport_series = %s AND passport_number = %s AND user_id != %s;
                '''
                
        params = (passport_series, passport_number, user_id)
        if execute_query(query, params):
            return jsonify({"result": "Клиент с таким паспортом уже зарегистрирован!"}), 403
        
        query = '''
                SELECT * FROM Clients
                WHERE contact_number = %s AND user_id != %s;
                '''
        
        params = (contact_number, user_id)
        if execute_query(query, params):
            return jsonify({"result": "Пользователь с таким номером уже зарегестрирован!"}), 403

        query = ''' 
                SELECT * FROM Clients
                WHERE client_email = %s AND user_id != %s;
                '''
                
        params = (client_email, user_id)
        if execute_query(query, params):
            return jsonify({"result": "Клиент с таким e-mail уже зарегистрирован!"}), 403
        
        query = ''' UPDATE Clients
                    SET client_first_name = %s,
                        client_last_name = %s,
                        client_surname = %s,
                        birth_day = %s,
                        passport_series = %s,
                        passport_number = %s,
                        contact_number = %s,
                        address = %s,
                        client_email = %s
                    WHERE user_id = %s
                '''
                
        params = (client_first_name, client_last_name, client_surname, birth_day, 
                  passport_series, passport_number, contact_number, 
                  address, client_email, user_id)
        
        execute_query(query, params)
        
        return({"result": "Успешно!"}), 200
    
    def make_new_policy(policy_type,
                        date_start,
                        policy_duration,
                        region,
                        user_id,
                        car_brand,
                        car_model,
                        year_manufacture,
                        state_number,
                        damage_description,
                        drivers):
        
        cost = Calculator.calculation(policy_type,
                                      region,
                                      car_brand,
                                      car_model,
                                      year_manufacture,
                                      policy_duration,
                                      drivers)
        
        return jsonify({"result": cost}), 200