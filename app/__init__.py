from flask import Flask, render_template
from .config import Config
from .extensions import db, bcrypt, mail
from .controllers.controller_pg import pg_bp
from .controllers.controller_user import user_bp

def create_app(config_class=Config):
    """
    Factory function untuk membuat instance aplikasi Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inisialisasi ekstensi
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # Registrasi blueprint
    register_blueprints(app)

    # Registrasi error handler
    register_error_handlers(app)

    return app

def register_blueprints(app):
    """
    Registrasi blueprint aplikasi.
    """
    app.register_blueprint(pg_bp, url_prefix='/')  # Blueprint untuk halaman utama
    app.register_blueprint(user_bp, url_prefix='/user')  # Blueprint untuk pengguna

def register_error_handlers(app):
    """
    Registrasi error handler global.
    """
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Server Error: {error}")
        return render_template("errors/500.html"), 500
