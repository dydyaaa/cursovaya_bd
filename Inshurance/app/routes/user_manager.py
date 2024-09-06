from flask import Blueprint, jsonify, request
from app.utils import execute_query
from ..services.user_manager import UserManager


user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/api/home', methods=['GET'])
def home_page():
    return jsonify({"result": "home page feels ok!"}), 200


@user_bp.route('/api/register/agents', methods=['GET', 'POST'])
def register_agents():
    return jsonify({"result": "register_agents"}), 200


@user_bp.route('/api/register/clients', methods=['POST'])
def register_clients():
    
    data = request.json
    user_login = data.get('user_login')
    password = data.get('password')
    
    if not user_login or not password:
        return jsonify({"result": "User login and password are required!"}), 400
    
    UserManager.register_client(user_login, password)
    
    return jsonify({"result": "register_clients"}), 200


@user_bp.route('/api/login', methods=['GET', 'POST'])
def login():
    
    data = request.json
    user_login = data.get('user_login')
    password = data.get('password')
    
    if not user_login or password:
        return jsonify({"result": "User login and password are required!"}), 400
    
    # UserManager.login
    
    return jsonify({"result": "login"}), 200
