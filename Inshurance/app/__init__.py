from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, jsonify
from datetime import datetime
import logging
import json
import os


def create_app():
    
    app = Flask(__name__)
    
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'settings.json'))
    
    with open(config_path) as config_file:
        config = json.load(config_file)
        app.config['SECRET_KEY'] = config.get('SECRET_KEY')
        
    SWAGGER_URL = '/swagger'  
    API_URL = '/static/swagger.json'    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={  
            'app_name': "Flask API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    from .routes.user_manager import user_bp 
    app.register_blueprint(user_bp)
    from .routes.polis_manager import polis_bp
    app.register_blueprint(polis_bp)
    from .routes.agent_manager import agent_bp
    app.register_blueprint(agent_bp)
    from .routes.admin_manager import admin_bp
    app.register_blueprint(admin_bp)
    
    @app.errorhandler(404)
    def not_found(e):
        formatted_date = datetime.now().strftime("%d/%b/%Y")
        logging.warning(f' [{formatted_date}] 404 - Not Found')
        return jsonify({"result": "Not Found"}), 404
    
    return app