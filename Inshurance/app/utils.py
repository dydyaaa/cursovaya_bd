import psycopg2
from flask import request, jsonify
from flask import current_app as app
import jwt
from functools import wraps
import logging


def execute_query(query, params=None, return_json=None):
    query_type = query.strip().split()[0].upper()
    
    try:
        connection = psycopg2.connect(
            host='0.0.0.0',
            user='admin',
            password='root',
            database='postgres'
        )

        connection.autocommit = True

        with connection.cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if query_type != 'SELECT':
                connection.close()
                return None
            else:
                result = cursor.fetchall()
                if return_json == True:
                    colnames = [desc[0] for desc in cursor.description]
                    result_dict = [dict(zip(colnames, row)) for row in result]
                    connection.close()
                    return result_dict
                else:
                    connection.close()
                    return result

    except Exception as e:
        return e

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            query = "SELECT * FROM Users WHERE user_login = %s"
            params = (f'{data['user_login']}',)
            current_user = execute_query(query, params, return_json=True)
        except:
            return jsonify({"result": "Invalid token!"}), 403
        
        if not current_user:
            return jsonify({"result": "Invalid token!"}), 403

        else:
        
           return f(current_user, *args, **kwargs)
    
    return decorated_function


def permission_required(necessary_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = args[0]

            role_rank = {
                'client': 1,
                'agent': 2,
                'admin': 3
            }
            
            current_role = role_rank.get(current_user[0].get('user_role'), 0)
            necessary_rank = role_rank.get(necessary_role, 0)
            if current_role >= necessary_rank:
                return f(*args, **kwargs)
            else:
                return jsonify({"message": "Forbidden"}), 403

        return decorated_function
    return decorator