from __future__ import annotations

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config

from .auth.routes import auth_bp
from .extensions import db, login_manager, migrate
from .main.routes import main_bp


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    register_shell_context(app)
    initialize_database(app)
    return app


def initialize_database(app: Flask) -> None:
    if not app.config.get('AUTO_CREATE_TABLES', True):
        return

    from .models import Branch, StrategicPriority, User
    from .seed import seed_demo_data

    with app.app_context():
        db.create_all()
        if app.config.get('AUTO_SEED_DATA', True):
            should_seed = (
                User.query.count() == 0
                or Branch.query.count() == 0
                or StrategicPriority.query.count() == 0
            )
            if should_seed:
                seed_demo_data(force=False)


def register_shell_context(app: Flask) -> None:
    from . import models

    @app.shell_context_processor
    def shell_context():
        return {'db': db, 'models': models}

app = create_app()
