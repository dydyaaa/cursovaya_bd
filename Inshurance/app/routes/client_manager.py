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