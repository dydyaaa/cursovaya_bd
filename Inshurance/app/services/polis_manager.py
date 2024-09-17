from ..services.user_manager import UserManager
from app.utils import execute_query
import datetime
from flask import current_app as app
from flask import jsonify


class PolisManager:
    
    def get_my_polis(current_user):
        
        query = """SELECT p.policy_id, p.policy_type, p.date_start, p.date_stop, p.policy_cost, p.status
                    FROM Policies p
                    JOIN Clients c
                    ON p.client_id = c.client_id
                    WHERE c.user_id = %s"""
        params = (current_user[0]['user_id'],)
        result = execute_query(query, params, return_json=True)
        
        if result:
            for x in result:
                x['date_start'] = x['date_start'].strftime('%d.%m.%Y')
                x['date_stop'] = x['date_stop'].strftime('%d.%m.%Y')
            return jsonify({"result": result}), 200
        else:
            return jsonify({"result": "У вас нет активных полисов!"}), 200
        
    
    def get_my_insurance(current_user):
        
        query = """SELECT c.date, c.description, c.status, c.sum_payment
                    FROM Cases c
                    JOIN Policies p
                    ON c.policy_id = p.policy_id
                    JOIN Clients cl
                    ON p.client_id = cl.client_id
                    WHERE cl.user_id = %s"""
        params = (current_user[0]['user_id'],)
        result = execute_query(query, params, return_json=True)
        if result:
            result[0]['date'] = result[0]['date'].strftime('%d.%m.%Y')
            return jsonify({"result": result}), 200
        else:
            return jsonify({"result": "У вас нет активных заявок!"}), 200
    
    
    def make_new_policy(policy_type, 
                        date_start, 
                        date_stop, 
                        car_brand, 
                        year_of_manufacture, 
                        sum_insurance, 
                        current_user):
        
        sum_insurance = int(sum_insurance)
        
        date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
        date_stop = datetime.datetime.strptime(date_stop, '%Y-%m-%d')
        
        if sum_insurance < 10000:
            return jsonify({"result": "Сумма выплат не может быть меньше 10.000р"}), 403
        
        if sum_insurance > 5000000:
            return jsonify({"result": "Сумма выплат не может быть больше 5.000.000р"}), 403
        
        if date_start < datetime.datetime.now():
            return jsonify({"result": "Дата начала действия полиса не может быть раньше сегодняшней даты!"}), 403
        
        if date_stop < date_start:
            return jsonify({"result": "Дата начала действия полиса не может быть позже даты окончания!"}), 403
        
        query = """SELECT c.client_id FROM Clients c
                    JOIN Users u 
                    ON c.user_id = u.user_id
                    WHERE u.user_id = %s"""
        params = (current_user[0].get('user_id'),)
        
        client_id = execute_query(query, params)[0][0]
        
        policy_cost = UserManager.calculation(policy_type, 
                                             date_start, 
                                             date_stop, 
                                             car_brand, 
                                             year_of_manufacture,
                                             sum_insurance)
        
        query = """ INSERT INTO Policies (
                                policy_type, 
                                client_id, 
                                date_start, 
                                date_stop, 
                                car_brand,
                                year_of_manufacture,
                                policy_cost,
                                sum_insurance
                                )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (policy_type, 
                  client_id, 
                  date_start, 
                  date_stop, 
                  car_brand, 
                  year_of_manufacture, 
                  policy_cost, 
                  sum_insurance)
        execute_query(query, params)
        
        return jsonify({"result": current_user[0].get('user_id')}), 200
    
    def make_new_inshurance(policy_id, date, description):
        
        query = """SELECT * FROM Policies WHERE policy_id = %s"""
        params = (policy_id, )
        result = execute_query(query, params, return_json=True)
    
        if result[0]['status'] != 'Активный':
            return jsonify({"result": 'Ваш полис не активен!'}), 403
        
        query = """INSERT INTO Cases (
            policy_id, 
            date,
            description
            ) VALUES (%s, %s, %s)"""
            
        params = (policy_id, date, description)
        
        r = execute_query(query, params)
        print(r)
        query = """UPDATE Polisies SET status = 'Рассматривается случай' WHERE policy_id = %s"""
        params= (policy_id, )
        execute_query(query, params) 
        
        return jsonify({"result": "vrode ok"}), 200