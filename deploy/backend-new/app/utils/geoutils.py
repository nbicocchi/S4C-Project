from geopy.distance import geodesic

def are_close(lat1, lng1, lat2, lng2, soglia_m=1000):
    """True se la distanza tra due punti è minore della soglia in metri."""
    return geodesic((lat1, lng1), (lat2, lng2)).meters <= soglia_m

def to_float(val):
    if isinstance(val, (float, int)):
        return float(val)
    try:
        return float(str(val).replace(',', '.'))
    except:
        return 0.0