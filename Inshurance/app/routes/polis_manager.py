from flask import Blueprint, jsonify, request
from app.utils import login_required, permission_required
from ..services.polis_manager import PolisManager


polis_bp = Blueprint('polis_bp', __name__)

@polis_bp.route('/api/get_my_polis', methods=['GET'])
@login_required
@permission_required('Client')
def get_my_polis(current_user):
    return PolisManager.get_my_polis(current_user)


@polis_bp.route('/api/get_my_insurance', methods=['GET'])
@login_required
@permission_required('Client')
def get_my_insurance(current_user):
    return PolisManager.get_my_insurance(current_user)


@polis_bp.route('/api/make_new_polis', methods=['POST'])
@login_required
@permission_required('Client')
def make_new_policy(current_user):
    
    data = request.json
    
    policy_type = data.get('policy_type')
    date_start = data.get('date_start')
    date_stop = data.get('date_stop')
    sum_insurance = data.get('sum_insurance')
    
    return PolisManager.make_new_policy(policy_type, 
                                        date_start, 
                                        date_stop, 
                                        sum_insurance, 
                                        current_user)


@polis_bp.route('/api/make_new_inshurance', methods=['GET', 'POST'])
@login_required
@permission_required('Client')
def make_new_inshurance(current_user):
    if request.method == 'POST':
        data = request.json 
        
        policy_id = data.get('policy_id')
        date = data.get('date')
        description = data.get('description')
        sum_payment = data.get('sum_payment')
        
        return PolisManager.make_new_inshurance(policy_id,
                                                date,
                                                description,
                                                sum_payment,
                                                current_user)
    
    return PolisManager.get_my_polis(current_user)