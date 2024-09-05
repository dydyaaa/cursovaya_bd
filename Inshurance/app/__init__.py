from flask import Flask, jsonify
import datetime
import logging
import json
import os


def create_app():
    
    app = Flask(__name__)
    
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'settings.json'))

    with open(config_path) as config_file:
        config = json.load(config_file)
        app.config['SECRET_KEY'] = config.get('SECRET_KEY')
    
    from .routes.user_manager import user_bp 
    app.register_blueprint(user_bp)
    from .routes.polis_manager import polis_bp
    app.register_blueprint(polis_bp)
    
    app.errorhandler(404)
    def not_found(e):
        formatted_date = datetime.now().strftime("%d/%b/%Y")
        logging.warning(f' [{formatted_date}] 404 - Not Found')
        return jsonify({"result": "Not Found"}), 404
    
    return app