import os
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from .api import api
from .shared.utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev_only_key_change_me")

app.register_blueprint(api)

# Flask-Login setup - impostiamo la pagina di login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = None

# ------------------CLASSE USER-----------------------
class User(UserMixin):
    def __init__(self, id, email, ruolo):
        self.id = id
        self.email = email
        self.ruolo = ruolo

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connectionUtenti()
        user = conn.execute("SELECT * FROM utenti WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        if user:
            return User(id=user["id"], email=user["email"], ruolo=user["ruolo"])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# ------------------- UTENTE --------------------
@app.post("/api/login")
def api_login():
    """
    Autenticazione utente (API-only).
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connectionUtenti()
    user = conn.execute("SELECT * FROM utenti WHERE email=?", (email,)).fetchone()
    conn.close()

    if not user or user["password"] != password:
        return jsonify({"success": False, "error": "Credenziali non valide"}), 401

    user_obj = User(id=user["id"], email=user["email"], ruolo=user["ruolo"])
    login_user(user_obj)

    return jsonify({"success": True, "email": user["email"], "ruolo": user["ruolo"]})

@app.get("/api/userinfo")
@login_required
def api_userinfo():
    """
    Ritorna informazioni sull'utente loggato.
    Utile al frontend_static per capire se l'utente è admin, ecc.
    """
    return jsonify({
        "id": current_user.id,
        "email": current_user.email,
        "ruolo": current_user.ruolo
    })

@app.post("/api/logout")
@login_required
def api_logout():
    logout_user()
    return jsonify({"success": True})


# ------------------- ADMIN ---------------------
@app.post("/api/admin/login")
def api_admin_login():
    """
    Login specifico per admin
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connectionUtenti()
    admin = conn.execute(
        "SELECT * FROM utenti WHERE email=? AND ruolo='admin'", (email,)
    ).fetchone()
    conn.close()

    if not admin or admin["password"] != password:
        return jsonify({"success": False, "error": "Credenziali amministratore non valide"}), 401

    user_obj = User(id=admin["id"], email=admin["email"], ruolo=admin["ruolo"])
    login_user(user_obj)

    return jsonify({"success": True, "email": admin["email"], "ruolo": "admin"})

@app.get("/api/admin/dashboard")
@login_required
def api_admin_dashboard():
    if current_user.ruolo != "admin":
        return jsonify({"error": "forbidden"}), 403
    return jsonify({"status": "ok"})

@app.get("/api/admin/users")
@login_required
def api_admin_users():
    if current_user.ruolo != "admin":
        return jsonify({"error": "forbidden"}), 403

    conn = get_db_connectionUtenti()
    users = conn.execute("SELECT * FROM utenti").fetchall()
    conn.close()

    return jsonify([dict(u) for u in users])

@app.post("/api/admin/users")
@login_required
def api_admin_add_user():
    if current_user.ruolo != "admin":
        return jsonify({"error": "forbidden"}), 403

    data = request.json
    email = data.get("email")
    password = data.get("password")
    ruolo = data.get("ruolo", "user")

    conn = get_db_connectionUtenti()
    try:
        conn.execute("INSERT INTO utenti (email, password, ruolo) VALUES (?, ?, ?)",
                     (email, password, ruolo))
        conn.commit()
    except:
        return jsonify({"error": "utente già esistente"}), 400
    conn.close()

    return jsonify({"success": True})

@app.delete("/api/admin/users/<int:user_id>")
@login_required
def api_admin_delete_user(user_id):
    if current_user.ruolo != "admin":
        return jsonify({"error": "forbidden"}), 403

    conn = get_db_connectionUtenti()
    conn.execute("DELETE FROM utenti WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

#---------------- PARCHEGGI -----------------

@app.get("/api/parcheggi")
@login_required
def api_parcheggi():
    return jsonify(load_parcheggi())

# ---------------- LINEE BUS -----------------
@app.get("/api/linee")
@login_required
def api_linee():
    return jsonify(load_linee())

# ---------------- APP START -----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)