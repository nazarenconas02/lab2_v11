import os
from flask import Flask, redirect
from flasgger import Swagger
from flask_restx import Api

from api_v1.routes import api_v1_bp
from api_v2.resources import api_v2_ns

from database import init_db

def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()

    
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  
                "model_filter": lambda tag: True, 
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/"
    }
    
    Swagger(app, config=swagger_config)

    api = Api(
        app, 
        version='1.0', 
        title='Literature API (RestX)', 
        description='Advanced API with validation',
        doc=None 
    )
    
    api.add_namespace(api_v2_ns, path='/api/v2')

    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)