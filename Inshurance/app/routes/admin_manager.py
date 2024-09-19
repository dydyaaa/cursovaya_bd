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


@admin_bp.route('/api/tables', methods=['GET'])
@login_required
@permission_required('Admin')
def all_tables(current_user):
    return AdminManager.all_tables()


@admin_bp.route('/api/tables/<table_name>')
@login_required
@permission_required('Admin')
def view_table(current_user, table_name):
    return AdminManager.view_table(table_name)