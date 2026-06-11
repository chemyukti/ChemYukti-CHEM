from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()
ckeditor = CKEditor()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    ckeditor.init_app(app)

    from app.blueprints.main import main_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.mentors import mentors_bp
    from app.blueprints.research import research_bp
    from app.blueprints.community import community_bp
    from app.blueprints.solutions import solutions_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(mentors_bp, url_prefix='/mentors')
    app.register_blueprint(research_bp, url_prefix='/research')
    app.register_blueprint(community_bp, url_prefix='/community')
    app.register_blueprint(solutions_bp, url_prefix='/solutions')

    return app
