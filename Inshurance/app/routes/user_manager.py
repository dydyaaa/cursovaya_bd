from flask import Blueprint, jsonify, request
from app.utils import login_required, permission_required
from ..services.user_manager import UserManager


user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/api/home', methods=['GET'])
def home_page():
    return jsonify({"result": "home page feels ok!"}), 200


@user_bp.route('/api/register', methods=['POST'])
def register():
    
    data = request.json
    user_login = data.get('user_login')
    password = data.get('password')
    
    if not user_login or not password:
        return jsonify({"result": "User login and password are required!"}), 400
    
    return UserManager.register(user_login, password)


@user_bp.route('/api/login', methods=['POST'])
def login():
    
    data = request.json
    user_login = data.get('user_login')
    password = data.get('password')
    
    if not user_login or not password:
        print(user_login, password)
        print(data)
        return jsonify({"result": "User login and password are required!"}), 400
    
    return UserManager.login(user_login, password)


@user_bp.route('/api/become_client', methods=['POST'])
@login_required
@permission_required('client')
def become_client(current_user):
    
    data = request.json
    
    return UserManager.become_client(data, current_user)