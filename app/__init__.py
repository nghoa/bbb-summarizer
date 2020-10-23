from flask import Flask

# host='localhost', port=8132, debug=True
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # TODO:
    app.config.from_pyfile('dev.cfg')
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
