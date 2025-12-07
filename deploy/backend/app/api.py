import os
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, send_file, current_app

# === Shared utilities ===
from .shared.geoutils import to_float
from .shared.sim import run_simulazione
from .shared.utils import *

api = Blueprint('api', __name__)

# ======================= Helpers =======================
def safe_int(val, default=0):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def safe_float(val, default=0.0):
    try:
        return to_float(val)
    except (ValueError, TypeError):
        return default

def jsonify_row(row):
    return jsonify(dict(row)) if row else ({"error": "Not found"}, 404)

def commit_and_close(conn):
    conn.commit()
    conn.close()


# ======================= Logging =======================
@api.before_app_request
def log_request_info():
    print(f"[API CALL] {request.method} {request.path}")


# ======================= Health =======================
@api.get("/health")
def api_health():
    return {"status": "ok"}, 200


# ======================= MAPPA =======================
@api.get("/api/mappa/dati")
def api_mappa_dati():
    try:
        parcheggi = [p for p in load_parcheggi() if p.get("attivo") == 1]
        linee = [l for l in load_linee() if l.get("attiva") == 1]

        for p in parcheggi:
            p["latitudine"] = safe_float(p["latitudine"])
            p["longitudine"] = safe_float(p["longitudine"])

        for l in linee:
            for campo in ["partenza_lat", "partenza_lng", "arrivo_lat", "arrivo_lng"]:
                l[campo] = safe_float(l[campo])

        return jsonify({"parcheggi": parcheggi, "linee_trasporto": linee})

    except Exception as e:
        print("Errore mappa:", e)
        return jsonify({"error": str(e)}), 500


# ======================= PARCHEGGI =======================
@api.get("/api/parcheggi")
def api_get_parcheggi():
    return jsonify(load_parcheggi())

@api.get("/api/parcheggi/<id>")
def api_get_parcheggio(id):
    conn = get_db_connectionParcheggi()
    row = conn.execute("SELECT * FROM parcheggi WHERE id=?", (id,)).fetchone()
    conn.close()
    return jsonify_row(row)

@api.post("/api/parcheggi")
def api_add_parcheggio():
    data = request.json
    try:
        conn = get_db_connectionParcheggi()
        conn.execute(
            """
            INSERT INTO parcheggi (nome, comune, capienza, attivo, latitudine, longitudine)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(data.get("nome", "")),
                str(data.get("comune", "")),
                safe_int(data.get("capienza")),
                1 if data.get("attivo") else 0,
                safe_float(data.get("latitudine")),
                safe_float(data.get("longitudine"))
            )
        )
        commit_and_close(conn)
        return jsonify({"success": True}), 201
    except Exception as e:
        print("Errore add parcheggio:", e)
        return jsonify({"error": str(e)}), 400

@api.put("/api/parcheggi/<id>")
def api_update_parcheggio(id):
    data = request.json
    try:
        conn = get_db_connectionParcheggi()
        conn.execute(
            """
            UPDATE parcheggi
            SET nome=?, comune=?, capienza=?, attivo=?, latitudine=?, longitudine=?
            WHERE id=?
            """,
            (
                str(data.get("nome", "")),
                str(data.get("comune", "")),
                safe_int(data.get("capienza")),
                1 if data.get("attivo") else 0,
                safe_float(data.get("latitudine")),
                safe_float(data.get("longitudine")),
                safe_int(id)
            )
        )
        commit_and_close(conn)
        return jsonify({"success": True})
    except Exception as e:
        print("Errore update parcheggio:", e)
        return jsonify({"error": str(e)}), 400

@api.delete("/api/parcheggi/<id>")
def api_delete_parcheggio(id):
    conn = get_db_connectionParcheggi()
    conn.execute("DELETE FROM parcheggi WHERE id=?", (id,))
    commit_and_close(conn)
    return jsonify({"success": True})


# ======================= LINEE BUS =======================
@api.get("/api/linee")
def api_get_linee():
    return jsonify(load_linee())

@api.get("/api/linee/<id>")
def api_get_linea(id):
    conn = get_db_connectionLinee()
    row = conn.execute("SELECT * FROM linee WHERE id=?", (id,)).fetchone()
    conn.close()
    return jsonify_row(row)

@api.post("/api/linee")
def api_add_linea():
    data = request.json
    try:
        conn = get_db_connectionLinee()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO linee (
                nome, comune_partenza, partenza_lat, partenza_lng,
                comune_arrivo, arrivo_lat, arrivo_lng,
                capienza, attiva, sabato, domenica, frequenza_giornaliera
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(data.get("nome", "")),
                str(data.get("comune_partenza", "")),
                safe_float(data.get("partenza_lat")),
                safe_float(data.get("partenza_lng")),
                str(data.get("comune_arrivo", "")),
                safe_float(data.get("arrivo_lat")),
                safe_float(data.get("arrivo_lng")),
                safe_int(data.get("capienza")),
                1 if data.get("attiva") else 0,
                1 if data.get("sabato") else 0,
                1 if data.get("domenica") else 0,
                safe_int(data.get("frequenza_giornaliera"))
            )
        )
        commit_and_close(conn)
        return jsonify({"id": cur.lastrowid}), 201
    except Exception as e:
        print("Errore add linea:", e)
        return jsonify({"error": str(e)}), 400

@api.put("/api/linee/<id>")
def api_update_linea(id):
    data = request.json
    try:
        conn = get_db_connectionLinee()
        conn.execute(
            """
            UPDATE linee
            SET nome=?, comune_partenza=?, partenza_lat=?, partenza_lng=?,
                comune_arrivo=?, arrivo_lat=?, arrivo_lng=?, capienza=?,
                attiva=?, sabato=?, domenica=?, frequenza_giornaliera=?
            WHERE id=?
            """,
            (
                str(data.get("nome", "")),
                str(data.get("comune_partenza", "")),
                safe_float(data.get("partenza_lat")),
                safe_float(data.get("partenza_lng")),
                str(data.get("comune_arrivo", "")),
                safe_float(data.get("arrivo_lat")),
                safe_float(data.get("arrivo_lng")),
                safe_int(data.get("capienza")),
                1 if data.get("attiva") else 0,
                1 if data.get("sabato") else 0,
                1 if data.get("domenica") else 0,
                safe_int(data.get("frequenza_giornaliera")),
                safe_int(id)
            )
        )
        commit_and_close(conn)
        return jsonify({"success": True})
    except Exception as e:
        print("Errore update linea:", e)
        return jsonify({"error": str(e)}), 400

@api.delete("/api/linee/<id>")
def api_delete_linea(id):
    conn = get_db_connectionLinee()
    conn.execute("DELETE FROM linee WHERE id=?", (id,))
    commit_and_close(conn)
    return jsonify({"success": True})


# ======================= SIMULAZIONI =======================
@api.get("/api/simulazioni")
def api_get_simulazioni():
    conn = get_db_connectionSimulazioni()
    rows = conn.execute("SELECT * FROM simulazioni ORDER BY timestamp DESC").fetchall()
    conn.close()
    simulazioni = [dict(r) for r in rows]
    return jsonify({
        "simulazioni": simulazioni,
        "parcheggi": load_parcheggi(),
        "linee": load_linee()
    })

@api.get("/api/simulazioni/<sim_id>")
def api_get_simulazione(sim_id):
    sim = load_simulazione(sim_id)
    if sim is None:
        return jsonify({"error": "Simulazione non trovata"}), 404
    return jsonify(sim)

@api.delete("/api/simulazioni/<sim_id>")
def api_delete_simulazione(sim_id):
    if load_simulazione(sim_id) is None:
        return jsonify({"error": "Simulazione non trovata"}), 404
    conn = get_db_connectionSimulazioni()
    conn.execute("DELETE FROM simulazioni WHERE id=?", (sim_id,))
    commit_and_close(conn)
    return jsonify({"success": True})

@api.post("/api/simulazioni/esporta")
def api_simulazione_export():
    data = request.json
    sim_id = data.get("id")
    if not sim_id:
        return jsonify({"error": "ID simulazione mancante"}), 400
    sim = load_simulazione(sim_id)
    if sim is None:
        return jsonify({"error": "Simulazione non trovata"}), 404

    export_dir = os.path.join(current_app.root_path, "exports")
    os.makedirs(export_dir, exist_ok=True)
    filename = f"simulazione_{sim_id}.json"
    export_path = os.path.join(export_dir, filename)

    export_data = {
        "data": sim["data"],
        "n_turisti": sim["n_turisti"],
        "parcheggi_aperti": sim["parcheggi_usati"],
        "parcheggi_esclusi": sim["parcheggi_esclusi"],
        "linee_utilizzate": sim["linee_usate"],
        "linee_escluse": sim["linee_escluse"]
    }

    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=4)

    return send_file(export_path, as_attachment=True, download_name=filename, mimetype="application/json")

@api.post("/api/sim")
def api_run_simulazione():
    data = request.json
    data_sim = data.get("data")
    n_turisti = safe_int(data.get("n_turisti"))
    parcheggi_esclusi = data.get("parcheggi_esclusi", [])
    linee_escluse = data.get("linee_escluse", [])

    sim_id, sim_doc = run_simulazione(data_sim, n_turisti, parcheggi_esclusi, linee_escluse)

    try:
        conn = get_db_connectionSimulazioni()
        conn.execute(
            """
            INSERT INTO simulazioni (id, data, n_turisti, risultato, parcheggi_usati,
            linee_usate, parcheggi_esclusi, linee_escluse, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sim_id, sim_doc["data"], sim_doc["n_turisti"],
                json.dumps(sim_doc["risultato"]),
                json.dumps(sim_doc["parcheggi_usati"]),
                json.dumps(sim_doc["linee_usate"]),
                json.dumps(sim_doc["parcheggi_esclusi"]),
                json.dumps(sim_doc["linee_escluse"]),
                sim_doc["timestamp"]
            )
        )
        commit_and_close(conn)
    except Exception as e:
        print("Errore salvando simulazione:", e)

    return jsonify({"id": sim_id, "simulazione": sim_doc}), 201


# ======================= PREDIZIONI =======================
@api.post("/api/predizioni")
def api_predizioni():
    data = request.json
    anno = safe_int(data.get("anno"))
    mese = safe_int(data.get("mese"))

    start_date = datetime(anno, mese, 1)
    if mese == 12:
        next_month = datetime(anno + 1, 1, 1)
    else:
        next_month = datetime(anno, mese + 1, 1)
    delta = (next_month - start_date).days

    previsioni = []
    for i in range(delta):
        giorno = start_date + timedelta(days=i)
        date_str = giorno.strftime("%Y-%m-%d")
        payload = {"date": date_str, "layerid": "08|037|025|000|000"}
        giorno_result = call_mobility_api(
            url="http://mobility-prediction:8080/predict",
            payload=payload,
            retries=3,
            delay=1,
            timeout=5
        )
        turisti = giorno_result["data"].get("prediction") if giorno_result["success"] else None
        previsioni.append({"data": date_str, "turisti": turisti})

    return jsonify({"anno": anno, "mese": mese, "previsioni": previsioni})
