from ..services.user_manager import UserManager
from app.utils import execute_query
from werkzeug.security import check_password_hash
from flask import current_app as app
from flask import jsonify


class AgentManager:

    def policy_to_approve():
        
        query = "SELECT * FROM P"
        
    def clients_to_approve():
        
        query = "SELECT * FROM Clients WHERE status = %s"
        params = ('На проверке',)
        result = execute_query(query, params, return_json=True)
        
        for i in result:
            i['birth_day'] = str(i['birth_day'])
        
        return jsonify({"result": result})
    
    
    def approve_client(client_id):
        query = "UPDATE Clients SET status = %s WHERE client_id = %s"
        params = ('Проверен', client_id)
        execute_query(query, params)
        return jsonify({"result": "successful"})
    
    
    def reject_client(client_id):
        query = "UPDATE Clients SET status = %s WHERE client_id = %s"
        params = ('Отказано', client_id)
        execute_query(query, params)
        return jsonify({"result": "successful"})
    