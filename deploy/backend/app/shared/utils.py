import sqlite3
import json
import requests
import time

def safe_json_loads(value):
    """Versione robusta di json.loads usata in molte parti del backend."""
    try:
        return json.loads(value) if value else []
    except Exception:
        return []

UTENTI = "db/utenti.db"
PARCHEGGI = "db/parcheggi.db"
LINEE = "db/linee.db"
SIMULAZIONI = "db/simulazioni.db"

def get_db_connectionUtenti():
    conn = sqlite3.connect(UTENTI)
    conn.row_factory = sqlite3.Row  # permette di accedere ai campi per nome
    return conn

def get_db_connectionParcheggi():
    conn = sqlite3.connect(PARCHEGGI)
    conn.row_factory = sqlite3.Row
    return conn

def get_db_connectionLinee():
    conn = sqlite3.connect(LINEE)
    conn.row_factory = sqlite3.Row
    return conn

def get_db_connectionSimulazioni():
    conn = sqlite3.connect(SIMULAZIONI)
    conn.row_factory = sqlite3.Row
    return conn

def load_parcheggi():
    conn = get_db_connectionParcheggi()
    rows = conn.execute("SELECT * FROM parcheggi").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def load_linee():
    conn = get_db_connectionLinee()
    rows = conn.execute("SELECT * FROM linee").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def load_simulazione(sim_id):
    """
    Carica una simulazione dal DB e ritorna un dict Python pulito.
    """
    conn = get_db_connectionSimulazioni()
    cur = conn.cursor()
    cur.execute("SELECT * FROM simulazioni WHERE id = ?", (sim_id,))
    row = cur.fetchone()
    columns = [desc[0] for desc in cur.description]
    conn.close()

    if not row:
        return None

    sim = dict(zip(columns, row))

    # parse dei JSON salvati come stringhe
    for key in [
        "risultato",
        "parcheggi_usati",
        "linee_usate",
        "parcheggi_esclusi",
        "linee_escluse"
    ]:
        sim[key] = safe_json_loads(sim.get(key))

    return sim

def call_mobility_api(url, payload, retries=3, delay=2, timeout=5):
    """
    Chiama mobility_api con retry automatici, timeout e gestione errori solida.

    :param url: URL completo (es. "http://mobility_api:8080/predict")
    :param payload: oggetto JSON da inviare
    :param retries: numero di tentativi
    :param delay: attesa tra un tentativo e l’altro
    :param timeout: timeout della richiesta in secondi
    :return: dict con "success", "data" oppure "error"
    """
    for attempt in range(1, retries + 1):
        try:
            res = requests.post(url, json=payload, timeout=timeout)

            if res.status_code == 200:
                return {"success": True, "data": res.json()}

            # errore HTTP (404, 500…)
            return {
                "success": False,
                "error": f"Mobility API ha risposto con HTTP {res.status_code}",
                "details": res.text,
            }

        except requests.exceptions.RequestException as e:
            # ultimo tentativo → errore finale
            if attempt == retries:
                return {"success": False, "error": str(e)}

            # attendo e ritento
            time.sleep(delay)

    # fallback (non dovrebbe mai arrivare qui)
    return {"success": False, "error": "Errore sconosciuto nella chiamata a mobility_api"}
