from ..services.user_manager import UserManager
from app.utils import execute_query
from werkzeug.security import check_password_hash
from flask import current_app as app
from flask import jsonify

class AdminManager:

    def execute_sql(sql_query):
        
        if ('DROP' in sql_query) or ('DELETE' in sql_query):
            return jsonify({"result": "К сожалению или к счастью, такого нельзя даже админам!"}), 400
        
        try:
            result = execute_query(sql_query)
            return jsonify({"result": str(result)}), 200
        except Exception as error:
            error = str(error)
            return jsonify({"result": error}), 400
        
        
    def all_tables():
        query = """ SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'"""
        result = execute_query(query, return_json=True)
        return jsonify({"result": result})
    
    
    def view_table(table_name):
        query = f"SELECT * FROM {table_name}"
        result = execute_query(query, return_json=True)
        return jsonify({"result": result})