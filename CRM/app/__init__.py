from flask import Flask
# We will create this db object in models.py next
from app.models import db 

def create_app():
    # Initialize Flask application
    app = Flask(__name__)
    
    # Load settings from config.py
    app.config.from_object('config.Config')
    
    # Connect database to the app
    db.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)
    
    # Create all database tables automatically
    with app.app_context():
        db.create_all()
        
    return app