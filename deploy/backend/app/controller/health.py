from flask_restx import Namespace, Resource

# Create a new namespace for health
health_ns = Namespace("health", description="Health check endpoints")

@health_ns.route("/")
class HealthCheck(Resource):
    def get(self):
        """
        Basic health check.
        Returns:
            JSON object with status OK.
        """
        return {"status": "ok"}, 200
