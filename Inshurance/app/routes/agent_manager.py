from flask import Blueprint, jsonify, request
from app.utils import login_required, permission_required
from ..services.agent_manager import AgentManager


agent_bp = Blueprint('agent_pb', __name__)


@agent_bp.route('/api/policy_to_approve', methods=['GET'])
@login_required
@permission_required('Agent')
def policy_to_approve(current_user):
    return jsonify({"result": "policy_to_approve"}), 200


@agent_bp.route('/api/all_policy', methods=['GET'])
@login_required
@permission_required('Agent')
def all_policy(current_agent):
    return jsonify({"result": "all_policy"}), 200


@agent_bp.route('/api/clients_to_approve', methods=['GET'])
@login_required
@permission_required('Agent')
def clients_to_approve(current_user):
    return AgentManager.clients_to_approve()


@agent_bp.route('/api/approve_client', methods=['POST'])
@login_required
@permission_required('Agent')
def approve_client(current_user):
    data = request.json
    client_id = data.get('client_id')
    return AgentManager.approve_client(client_id)


@agent_bp.route('/api/reject_client', methods=['POST'])
@login_required
@permission_required('Agent')
def reject_client(current_user):
    data = request.json
    client_id = data.get('client_id')
    return AgentManager.reject_client(client_id)