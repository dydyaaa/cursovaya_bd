from flask import Blueprint, jsonify, request
from app.utils import login_required, permission_required
from ..services.user_manager import UserManager
from ..services.calculator import Calculator


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
        return jsonify({"result": "User login and password are required!"}), 400
    
    return UserManager.login(user_login, password)


@user_bp.route('/api/change_password', methods=['POST'])
@login_required
def change_password(current_user):
    
    data = request.json
    user_password_first = data.get('user_password_first')
    user_password_second = data.get('user_password_second')
    
    if user_password_first != user_password_second:
        return jsonify({"result": "Пароли не свопадают!"})
    
    return UserManager.change_password(current_user, user_password_first)


@user_bp.route('/api/calculator/osago', methods=['GET', 'POST'])
def calculator():
    
    data = request.json
    
    car_brand = data.get('car_brand')
    car_model = data.get('car_model')
    year = data.get('year')
    duration = data.get('duration')
    drivers = data.get('drivers')
    
    return Calculator.calculation_osago(car_brand,
                                        car_model,
                                        year,
                                        duration,
                                        drivers)
    