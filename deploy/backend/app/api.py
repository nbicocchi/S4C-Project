from flask_login import login_required
from flask_restx import Namespace, Resource
from .shared.db import load_parcheggi, load_linee, get_db_connection_simulazioni, load_simulazione

# Create a namespace for API endpoints
api_ns = Namespace("api", description="Parking, Bus Lines, and Simulation endpoints")

# ------------------------
# PARKING ENDPOINTS
# ------------------------
@api_ns.route("/parcheggi")
class ParcheggiResource(Resource):
    @login_required
    @api_ns.doc("list_parcheggi")
    def get(self):
        """
        Retrieve all parking areas.
        Returns a JSON list of all parking areas.
        """
        return load_parcheggi()


# ------------------------
# BUS LINES ENDPOINTS
# ------------------------
@api_ns.route("/linee")
class LineeResource(Resource):
    @login_required
    @api_ns.doc("list_linee")
    def get(self):
        """
        Retrieve all bus lines.
        Returns a JSON list of all bus lines.
        """
        return load_linee()


# ------------------------
# SIMULATIONS ENDPOINTS
# ------------------------
@api_ns.route("/simulazioni")
class SimulazioniResource(Resource):
    @login_required
    @api_ns.doc("list_simulazioni")
    def get(self):
        """
        Retrieve all simulations, ordered by most recent first.
        Returns a JSON list of simulation records.
        """
        conn = get_db_connection_simulazioni()
        rows = conn.execute("SELECT * FROM simulazioni ORDER BY timestamp DESC").fetchall()
        conn.close()

        return [dict(r) for r in rows]
