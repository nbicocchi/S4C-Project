import sqlite3
import json

# Database file paths
DB_UTENTI = "db/utenti.db"
DB_PARCHEGGI = "db/parcheggi.db"
DB_LINEE = "db/linee.db"
DB_SIMULAZIONI = "db/simulazioni.db"


def get_connection(db_file):
    """Create a SQLite connection with row factory for dict-like access."""
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn


def get_db_connection_utenti():
    return get_connection(DB_UTENTI)


def get_db_connection_parcheggi():
    return get_connection(DB_PARCHEGGI)


def get_db_connection_linee():
    return get_connection(DB_LINEE)


def get_db_connection_simulazioni():
    return get_connection(DB_SIMULAZIONI)


def safe_json_loads(value):
    """Robust JSON loader: returns empty list if invalid or None."""
    try:
        return json.loads(value) if value else []
    except Exception:
        return []


# -------------------------
# DATA ACCESS FUNCTIONS
# -------------------------
def load_parcheggi():
    conn = get_db_connection_parcheggi()
    rows = conn.execute("SELECT * FROM parcheggi").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def load_linee():
    conn = get_db_connection_linee()
    rows = conn.execute("SELECT * FROM linee").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def load_simulazione(sim_id):
    """Load a simulation by ID and parse JSON fields."""
    conn = get_db_connection_simulazioni()
    cur = conn.cursor()
    cur.execute("SELECT * FROM simulazioni WHERE id = ?", (sim_id,))
    row = cur.fetchone()
    columns = [desc[0] for desc in cur.description]
    conn.close()

    if not row:
        return None

    sim = dict(zip(columns, row))

    # Parse JSON fields
    for key in [
        "risultato",
        "parcheggi_usati",
        "linee_usate",
        "parcheggi_esclusi",
        "linee_escluse"
    ]:
        sim[key] = safe_json_loads(sim.get(key))

    return sim
