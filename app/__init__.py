from flask import Flask
from flask_migrate import Migrate
from htmx_flask import Htmx
import os
from .models import db

migrate = Migrate()
htmx = Htmx()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuration
    app.config.from_mapping(
        SECRET_KEY='dev', # Change this in production
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'world_cup.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    htmx.init_app(app)

    # Register blueprints/routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app
