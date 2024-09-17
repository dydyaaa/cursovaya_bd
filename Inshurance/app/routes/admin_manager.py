from flask import Blueprint, jsonify, request
from app.utils import login_required, permission_required
from ..services.admin_manager import AdminManager


admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/api/execute_sql', methods=['POST'])
@login_required
@permission_required('Admin')
def execute_sql(current_user):
    data = request.json
    sql_query = data.get('sql_query')
    return AdminManager.execute_sql(sql_query)