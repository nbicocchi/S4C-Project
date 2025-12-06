import logging
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from flask_restx import Namespace, Resource, fields
from flask import request
from .shared.db import get_db_connection_utenti

# -------------------------
# Setup logging
# -------------------------
logger = logging.getLogger("auth")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# -------------------------
# Create namespace for authentication
# -------------------------
auth_ns = Namespace("auth", description="Authentication endpoints")

# -------------------------
# User Model for Swagger
# -------------------------
login_model = auth_ns.model(
    "Login",
    {
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
    }
)

user_model = auth_ns.model(
    "User",
    {
        "id": fields.Integer(description="User ID"),
        "email": fields.String(description="User email"),
        "ruolo": fields.String(description="User role")
    }
)

# -------------------------
# User class for Flask-Login
# -------------------------
class User(UserMixin):
    def __init__(self, id, email, ruolo):
        self.id = id
        self.email = email
        self.ruolo = ruolo

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection_utenti()
        user = conn.execute("SELECT * FROM utenti WHERE id=?", (user_id,)).fetchone()
        conn.close()
        if user:
            logger.info(f"Loaded user by id: {user_id}")
            return User(id=user["id"], email=user["email"], ruolo=user["ruolo"])
        logger.warning(f"User id {user_id} not found")
        return None

# -------------------------
# Authentication Endpoints
# -------------------------
@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(user_model, code=200, skip_none=True)
    def post(self):
        """Authenticate user and return user info"""
        data = request.json
        email = data.get("email")
        password = data.get("password")
        logger.info(f"Login attempt for email: {email}")

        conn = get_db_connection_utenti()
        user = conn.execute("SELECT * FROM utenti WHERE email=?", (email,)).fetchone()
        conn.close()

        if not user or user["password"] != password:
            logger.warning(f"Failed login attempt for email: {email}")
            auth_ns.abort(401, "Invalid credentials")

        user_obj = User(id=user["id"], email=user["email"], ruolo=user["ruolo"])
        login_user(user_obj)
        logger.info(f"User logged in: {email}")
        return {"id": user_obj.id, "email": user_obj.email, "ruolo": user_obj.ruolo}


@auth_ns.route("/userinfo")
class UserInfo(Resource):
    @login_required
    @auth_ns.marshal_with(user_model)
    def get(self):
        """Return current logged-in user info"""
        logger.info(f"User info requested for: {current_user.email}")
        return {"id": current_user.id, "email": current_user.email, "ruolo": current_user.ruolo}


@auth_ns.route("/logout")
class Logout(Resource):
    @login_required
    def post(self):
        """Logout current user"""
        logger.info(f"User logged out: {current_user.email}")
        logout_user()
        return {"success": True}
