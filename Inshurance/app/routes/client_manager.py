from flask import Blueprint, jsonify, request
from app.utils import login_required, permission_required
from ..services.client_manager import ClientManager


client_bp = Blueprint('client_bp', __name__)


@client_bp.route('/api/become_client', methods=['POST'])
@login_required
def become_client(current_user):
    
    data = request.json
    
    client_first_name = data.get('client_first_name')
    client_last_name = data.get('client_last_name')
    client_surname = data.get('client_surname')
    birth_day = data.get('birth_day')
    passport_series = data.get('passport_series')
    passport_number = data.get('passport_number')
    contact_number = data.get('contact_number')
    address = data.get('address')
    client_email = data.get('client_email')
    user_id = current_user[0].get('user_id')
    
    return ClientManager.become_client(client_first_name,
                                       client_last_name,
                                       client_surname,
                                       birth_day,
                                       passport_series,
                                       passport_number,
                                       contact_number,
                                       address,
                                       client_email,
                                       user_id)
    

@client_bp.route('/api/change_client_data', methods=['POST'])
@login_required
def change_client_data(current_user):
    
    data = request.json
    
    client_first_name = data.get('client_first_name')
    client_last_name = data.get('client_last_name')
    client_surname = data.get('client_surname')
    birth_day = data.get('birth_day')
    passport_series = data.get('passport_series')
    passport_number = data.get('passport_number')
    contact_number = data.get('contact_number')
    address = data.get('address')
    client_email = data.get('client_email')
    user_id = current_user[0].get('user_id')
    
    return ClientManager.change_client_data(client_first_name,
                                            client_last_name,
                                            client_surname,
                                            birth_day,
                                            passport_series,
                                            passport_number,
                                            contact_number,
                                            address,
                                            client_email,
                                            user_id)
    
    
@client_bp.route('/api/make_new_policy', methods=['POST'])
@login_required
@permission_required('Client')
def make_new_policy(current_user):
    
    data = request.json
    
    policy_type = data.get('policy_type')
    date_start = data.get('date_start')
    policy_duration = data.get('policy_duration')
    region = data.get('region')
    user_id = current_user[0].get('user_id')
    car_brand = data.get('car_brand')
    car_model = data.get('car_model')
    year_manufacture = data.get('year_manufacture')
    state_number = data.get('state_number')
    damage_description = data.get('damage_description')
    drivers = data.get('drivers')
    
    return ClientManager.make_new_policy(policy_type,
                                         date_start,
                                         policy_duration,
                                         region,
                                         user_id,
                                         car_brand,
                                         car_model,
                                         year_manufacture,
                                         state_number,
                                         damage_description,
                                         drivers)
    
    
@client_bp.route('/api/add_driver', methods=['POST'])
@login_required
@permission_required('Client')
def add_drivers(current_user):
    
    data = request.json
    
    policy_id = data.get('policy_id')
    drivers = data.get('drivers')
    
    return ClientManager.add_drivers(policy_id,
                                     drivers)
    

@client_bp.route('/api/get_my_policies', methods=['GET'])
@login_required
@permission_required('Client')
def get_my_policies(current_user):
    
    user_id = current_user[0].get('user_id')
    
    return ClientManager.get_my_policies(user_id)


@client_bp.route('/api/get_full_policy/<int:policy_id>', methods=['GET'])
@login_required
@permission_required('Client')
def get_full_policy(current_user, policy_id):
    
    user_id = current_user[0].get('user_id')
    
    return ClientManager.get_full_policy(user_id,
                                         policy_id)