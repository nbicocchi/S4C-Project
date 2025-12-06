from flask import Flask
from flask_login import LoginManager
from flask_restx import Api
from .auth import auth_ns, User   # Import User class for login manager
from .api import api_ns
from .health import health_ns

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "dev_only_key_change_me"

    # -------------------------
    # Setup Flask-Login
    # -------------------------
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = None  # API-only, no redirects

    # -------------------------
    # User loader for Flask-Login
    # -------------------------
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    # -------------------------
    # Setup Flask-RESTX API with Swagger
    # -------------------------
    api = Api(
        app,
        version="1.0",
        title="Parking & Transport API",
        description="API for managing parking, bus lines, simulations, and predictions",
        doc="/docs"
    )

    # -------------------------
    # Register namespaces
    # -------------------------
    api.add_namespace(auth_ns, path="/api/auth")
    api.add_namespace(api_ns, path="/api")
    api.add_namespace(health_ns, path="/health")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)