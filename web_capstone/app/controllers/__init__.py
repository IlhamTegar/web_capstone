from flask import Blueprint
from .controller_pg import pg_bp
from .controller_user import user_bp

def register_blueprints(app):
    """
    Registrasi semua blueprint.
    """
    app.register_blueprint(pg_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/user')
