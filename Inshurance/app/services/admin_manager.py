from ..services.user_manager import UserManager
from app.utils import execute_query
from werkzeug.security import check_password_hash
from flask import current_app as app
from flask import jsonify

class AdminManager:

    def execute_sql(sql_query):
        
        try:
            result = execute_query(sql_query)
            return jsonify({"result": result}), 200
        except Exception as error:
            return jsonify({"result": error}), 200