from flask import jsonify
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
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
        
        client_id = execute_query('SELECT client_id FROM clients WHERE user_id = %s', (user_id, ))[0][0]
        
        query = ''' SELECT brand_id FROM brands
                    WHERE brand = %s AND (model = %s OR model = 'default')
                    LIMIT 1
                '''
        
        params = (car_brand, car_model)
        
        brand_id = execute_query(query, params)[0]
        
        duration_map = {
            "1 день": timedelta(days=1),
            "1 месяц": relativedelta(months=1),
            "3 месяца": relativedelta(months=3),
            "6 месяцев": relativedelta(months=6),
            "1 год": relativedelta(years=1),
        }
        
        delta = duration_map.get(policy_duration)
        date_stop = datetime.strptime(date_start, '%Y-%m-%d') + delta
        date_stop = date_stop.strftime("%Y-%m-%d")
        
        cost = Calculator.calculation(policy_type,
                                      region,
                                      car_brand,
                                      car_model,
                                      year_manufacture,
                                      policy_duration,
                                      drivers)
        query = ''' SELECT * FROM Cars
                    WHERE state_number = %s
                '''
        params = (state_number,)
        
        if not execute_query(query, params):
        
            query = ''' INSERT INTO Cars (
                            brand_id,
                            year_manufacture,
                            state_number,
                            damage_description
                        )
                        VALUES (%s, %s, %s, %s)
                        RETURNING car_id
                    '''
            params = (brand_id, year_manufacture, state_number, damage_description)
            
            car_id = execute_query(query, params)[0][0]
            
        else:
            
            car_id = execute_query('SELECT car_id FROM Cars WHERE state_number = %s', (state_number, ))[0]
            
            query = ''' SELECT status, policy_type 
                        FROM Policies p 
                        JOIN cars c
                        ON p.car_id = c.car_id
                        WHERE c.state_number = %s
                    '''
            params = (state_number, )
            
            policy = execute_query(query, params, return_json=True)
            
            if policy:
                if (policy[0].get('status') == 'Действующий' or policy[0].get('status') == 'На проверке') and policy[0].get('policy_type') == policy_type:
                    return jsonify({"result": "Полис на этот автомобиль уже оформлен!"}), 403
            
        query = ''' INSERT INTO Policies (
                        policy_type,
                        date_start,
                        date_stop,
                        policy_cost,
                        car_id,
                        client_id,
                        region,
                        status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING policy_id
                '''    
        params = (policy_type, date_start, date_stop, cost, car_id, client_id, region, 'На проверке')

        policy_id = execute_query(query, params)[0]
        
        for driver in drivers:
            
            query = ''' SELECT * FROM Drivers
                        WHERE license_number = %s
                    '''
                    
            params = (driver.get('license_number'), )
            
            if not execute_query(query, params):
            
                query = ''' INSERT INTO Drivers (
                                policy_id,
                                driver_first_name,
                                driver_last_name,
                                driver_surname,
                                license_number,
                                first_license_date,
                                driver_birth
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        '''
                params = (policy_id,
                        driver.get('driver_first_name'), 
                        driver.get('driver_last_name'), 
                        driver.get('driver_surname'), 
                        driver.get('license_number'), 
                        driver.get('first_license_date'), 
                        driver.get('driver_birth'))
                
                execute_query(query, params)
            
        return jsonify({"result": cost}), 200
    
    
    def add_drivers(policy_id,
                    drivers):
        
        for driver in drivers:
            
            query = ''' SELECT * FROM Drivers
                        WHERE license_number = %s
                    '''
                    
            params = (driver.get('license_number'), )
            
            if not execute_query(query, params):
            
                query = ''' INSERT INTO Drivers (
                                policy_id,
                                driver_first_name,
                                driver_last_name,
                                driver_surname,
                                license_number,
                                first_license_date,
                                driver_birth
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        '''
                        
                params = (policy_id,
                        driver.get('driver_first_name'), 
                        driver.get('driver_last_name'), 
                        driver.get('driver_surname'), 
                        driver.get('license_number'), 
                        driver.get('first_license_date'), 
                        driver.get('driver_birth'))
                
                execute_query(query, params)
        
        query = ''' SELECT * FROM Policies p 
                    JOIN Cars c
                    ON c.car_id = p.car_id
                    JOIN Brands b
                    ON c.brand_id = b.brand_id
                    WHERE policy_id = %s
                '''
        
        params = (policy_id, )
        
        old_policy = execute_query(query, params, return_json=True)[0]
        
        cost = Calculator.calculation(old_policy.get('policy_type'),
                                      old_policy.get('region'),
                                      old_policy.get('brand'),
                                      old_policy.get('model'),
                                      old_policy.get('year_manufacture'),
                                      old_policy.get('policy_duration'),
                                      drivers)
        
        query = ''' UPDATE Policies 
                    SET policy_cost = %s
                    WHERE policy_id = %s
                '''
        
        params = (cost, policy_id)
        execute_query(query, params)
        
        return jsonify({"result": "Успешно!"}), 200
    
    
    def get_my_policies(user_id):
        
        query = ''' SELECT * FROM Policies p
                    JOIN Clients c
                    ON p.client_id = c.client_id
                    WHERE c.user_id = %s
                '''
                
        params = (user_id, )
        
        policies = execute_query(query, params, return_json=True)
        
        return jsonify({"result": policies}), 200
    
    
    def get_full_policy(current_user,
                        policy_id):
        
        # прoверить доступность полиса, вернуть всю инфу о полисе
        pass