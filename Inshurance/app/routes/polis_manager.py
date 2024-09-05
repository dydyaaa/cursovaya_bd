from flask import Blueprint, jsonify, request
from app.utils import execute_query


polis_bp = Blueprint('polis_bp', __name__)

@polis_bp.route('/api/get_my_polis', methods=['GET'])
def get_my_polis():
    return jsonify({"result": "get_my_polis"}), 200


@polis_bp.route('/api/get_my_insurance', methods=['GET'])
def get_my_insurance():
    return jsonify({"result": "get_my_insurance"}), 200


@polis_bp.route('/api/add_new_polis', methods=['GET', 'POST'])
def add_new_polis():
    return jsonify({"result": "add_new_polis"}), 200


@polis_bp.route('/api/add_new_insurance', methods=['GET', 'POST'])
def add_new_inshurance():
    return jsonify({"result": "add_new_inshurance"}), 200