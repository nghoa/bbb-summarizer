from flask import Flask
from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix

# host='localhost', port=8132, debug=True
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = b'_5#y2L"FxX2u4Q8z\n\xec]/'
    app.config.from_pyfile('dev.cfg')
    # Fix Reverse Proxy in Flask -> lookup in dev.cfg ['REVERSE_PROXY_PATH']
    # documentation @https://pypi.org/project/flask-reverse-proxy-fix/
    ReverseProxyPrefixFix(app)          
    initialize_extensions(app)
    register_blueprints(app)

    return app

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    pass

def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from app.lectures import lectures_blueprint
    from app.summarization import summarization_blueprint
 
    app.register_blueprint(lectures_blueprint)
    app.register_blueprint(summarization_blueprint)
