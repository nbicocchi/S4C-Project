import logging
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from flask_restx import Namespace, Resource, fields
from flask import request
from ..db.db import get_db_connection_utenti

# -------------------------
# Logging setup
# -------------------------
logger = logging.getLogger("auth")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
logger.addHandler(handler)

# -------------------------
# Namespace
# -------------------------
auth_ns = Namespace("auth", description="Authentication endpoints")

# -------------------------
# Swagger Models
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
        "ruolo": fields.String(description="User role"),
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
        row = conn.execute("SELECT * FROM utenti WHERE id=?", (user_id,)).fetchone()
        conn.close()
        if row:
            return User(id=row["id"], email=row["email"], ruolo=row["ruolo"])
        return None

# -------------------------
# LOGIN ENDPOINT
# -------------------------
@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(user_model, code=200)
    def post(self):
        """Authenticate user and return user info"""
        data = request.json
        email = data.get("email")
        password = data.get("password")

        logger.info(f"Login attempt: {email}")

        # Lookup user
        conn = get_db_connection_utenti()
        row = conn.execute("SELECT * FROM utenti WHERE email=?", (email,)).fetchone()
        conn.close()

        # Validate credentials (cleartext password)
        if not row or row["password"] != password:
            logger.warning(f"Invalid credentials for: {email}")
            auth_ns.abort(401, "Invalid email or password")

        user_obj = User(id=row["id"], email=row["email"], ruolo=row["ruolo"])
        login_user(user_obj)

        logger.info(f"Login OK: {email}")
        return user_obj

# -------------------------
# USER INFO (PROTECTED)
# -------------------------
@auth_ns.route("/userinfo")
class UserInfo(Resource):
    method_decorators = [login_required]

    @auth_ns.marshal_with(user_model)
    def get(self):
        """Return current logged-in user info"""
        logger.info(f"User info requested: {current_user.email}")
        return current_user

# -------------------------
# LOGOUT (PROTECTED)
# -------------------------
@auth_ns.route("/logout")
class Logout(Resource):
    method_decorators = [login_required]

    def post(self):
        """Logout current user"""
        logger.info(f"Logout: {current_user.email}")
        logout_user()
        return {"success": True}
