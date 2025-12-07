from flask_restx import Namespace, Resource
from flask_login import login_required
from ..db.db import load_parcheggi, load_linee, load_simulazioni

# Create a namespace for API endpoints
api_ns = Namespace("api", description="Parking, Bus Lines, and Simulation endpoints")

@api_ns.route("/parcheggi")
class ParcheggiResource(Resource):
    method_decorators = [login_required]   # ← correct way

    @api_ns.doc("list_parcheggi")
    def get(self):
        """
        Retrieve all parking areas.
        Returns a JSON list of all parking areas.
        """
        return load_parcheggi()


@api_ns.route("/linee")
class LineeResource(Resource):
    method_decorators = [login_required]   # ← correct way

    @api_ns.doc("list_linee")
    def get(self):
        """
        Retrieve all bus lines.
        Returns a JSON list of all bus lines.
        """
        return load_linee()


@api_ns.route("/simulazioni")
class SimulazioniResource(Resource):
    method_decorators = [login_required]   # ← correct way

    @api_ns.doc("list_simulazioni")
    def get(self):
        """
        Retrieve all simulations, ordered by most recent first.
        Returns a JSON list of simulation records.
        """
        return load_simulazioni()
