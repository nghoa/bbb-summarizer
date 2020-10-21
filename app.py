from app import create_app

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/dev.cfg
app = create_app('dev.cfg')