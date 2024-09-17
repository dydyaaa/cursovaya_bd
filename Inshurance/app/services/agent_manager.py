from app.utils import execute_query
from flask import current_app as app
from flask import jsonify


class AgentManager:

    def policy_to_approve():
        
        query = "SELECT * FROM Policies WHERE status = %s"
        params = ('На проверке', )
        result = execute_query(query, params, return_json=True)
        
        for i in result:
            i['date_start'] = str(i['date_start'])
            i['date_stop'] = str(i['date_stop'])
            
        return jsonify({"result": result}), 200
        
        
    def all_policy():
        query = "SELECT * FROM Policies"
        result = execute_query(query, return_json=True)
        
        for i in result:
            i['date_start'] = str(i['date_start'])
            i['date_stop'] = str(i['date_stop'])
        
        return jsonify({"result": result}), 200
    
        
    def clients_to_approve():
        
        query = "SELECT * FROM Clients WHERE status = %s"
        params = ('На проверке',)
        result = execute_query(query, params, return_json=True)
        
        for i in result:
            i['birth_day'] = str(i['birth_day'])
        
        return jsonify({"result": result}), 200
    
    
    def approve_client(client_id):
        query = "UPDATE Clients SET status = %s WHERE client_id = %s"
        params = ('Проверен', client_id)
        execute_query(query, params)
        return jsonify({"result": "successful"}), 200
    
    
    def reject_client(client_id):
        query = "UPDATE Clients SET status = %s WHERE client_id = %s"
        params = ('Отказано', client_id)
        execute_query(query, params)
        return jsonify({"result": "successful"}), 200
    
    
    def approve_polid(policy_id):
        query = "UPDATE Policies SET status = %s WHERE policy_id = %s"
        params = ('Активный', policy_id)
        execute_query(query, params)
        return jsonify("result", "successful"), 200
    