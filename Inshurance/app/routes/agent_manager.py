from flask import Blueprint, request
from app.utils import login_required, permission_required
from ..services.agent_manager import AgentManager


agent_bp = Blueprint('agent_pb', __name__)


@agent_bp.route('/api/policy_to_approve', methods=['GET'])
@login_required
@permission_required('Agent')
def policy_to_approve(current_user):
    return AgentManager.policy_to_approve()


@agent_bp.route('/api/all_policy', methods=['GET'])
@login_required
@permission_required('Agent')
def all_policy(current_agent):
    return AgentManager.all_policy()


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


@agent_bp.route('/api/approve_polis', methods=['POST'])
@login_required
@permission_required('Agnet')
def approve_polis(current_user):
    data = request.json
    policy_id = data.get('policy_id')
    return AgentManager.approve_polis(policy_id)


@agent_bp.route('/api/reject_polis', methods=['POST'])
@login_required
@permission_required('Agnet')
def reject_polis(current_user):
    data = request.json
    policy_id = data.get('policy_id')
    return AgentManager.reject_polis(policy_id)


@agent_bp.route('/api/approve_insherance', methods=['POST'])
@login_required
@permission_required('Agent')
def approve_insherance(current_user):
    data = request.json
    case_id = data.get('case_id')
    return AgentManager.approve_insherance(case_id)


@agent_bp.route('/api/reject_insherance', methods=['POST'])
@login_required
@permission_required('Agent')
def reject_insherance(current_user):
    data = request.json
    case_id = data.get('case_id')
    return AgentManager.reject_insherance(case_id)


@agent_bp.route('/api/all_inshurance', methods=['GET'])
@login_required
@permission_required('Agent')
def all_inshurance(current_user):
    return AgentManager.all_insherance()


@agent_bp.route('/api/all_clients', methods=['GET'])
@login_required
@permission_required('Agent')
def all_clients(current_user):
    return AgentManager.all_clients()