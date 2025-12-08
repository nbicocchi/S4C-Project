import uuid
from datetime import datetime
import json
from geopy.distance import geodesic
from schemas.schemas import Simulazione
from utils.geoutils import are_close, to_float
from repositories import parcheggi_repo, linee_repo  # adjust import paths
from schemas.schemas import Parcheggio, Linea

def run_simulazione(db, data, n_turisti, parcheggi_esclusi_ids=None, linee_escluse_ids=None):
    # Load all parcheggi and linee
    parcheggi = [
        Parcheggio.model_validate(p).model_dump()
        for p in parcheggi_repo.get_all(db, skip=0, limit=1000)
    ]

    linee = [
        Linea.model_validate(l).model_dump()
        for l in linee_repo.get_all(db, skip=0, limit=1000)
    ]

    # Filtra esclusi
    parcheggi_esclusi = [p for p in parcheggi if str(p["id"]) in parcheggi_esclusi_ids]
    linee_escluse = [l for l in linee if str(l["id"]) in linee_escluse_ids]
    parcheggi = [p for p in parcheggi if str(p["id"]) not in parcheggi_esclusi_ids]
    linee = [l for l in linee if str(l["id"]) not in linee_escluse_ids]

    # Esegui ottimizzazione
    output = ottimizza_risorse(parcheggi, linee, n_turisti)

    sim_id = uuid.uuid4().hex  # shorter, still unique
    timestamp = datetime.now().isoformat(timespec="seconds")

    sim_obj = Simulazione(
        id=sim_id,
        data=data,
        n_turisti=n_turisti,
        risultato=json.dumps(output["risultato"]),
        parcheggi_usati=json.dumps(output["parcheggi_usati"]),
        linee_usate=json.dumps(output["linee_usate"]),
        parcheggi_esclusi=json.dumps(parcheggi_esclusi_ids),
        linee_escluse=json.dumps(linee_escluse_ids),
        timestamp=timestamp
    )

    return sim_obj


def ottimizza_risorse(parcheggi, linee, n_turisti):
    DOZZA_COORDS = (44.3511, 11.6519)
    risultato = {}
    assegnati = 0
    parcheggi_usati = []
    linee_usate = set()

    # Mappa: parcheggio_id → linee collegate
    linee_per_parcheggio = {}
    for p in parcheggi:
        lat_p, lng_p = to_float(p['latitudine']), to_float(p['longitudine'])
        for linea in linee:
            lat_l, lng_l = to_float(linea['partenza_lat']), to_float(linea['partenza_lng'])
            if are_close(lat_p, lng_p, lat_l, lng_l, soglia_m=1000):
                linee_per_parcheggio.setdefault(p['id'], []).append(linea)

    # Distanze da Dozza
    parcheggi_distanze = [
        (p, geodesic(
            (to_float(p['latitudine']), to_float(p['longitudine'])),
            DOZZA_COORDS
        ).meters)
        for p in parcheggi
    ]
    parcheggi_distanze.sort(key=lambda x: x[1])

    for parcheggio, distanza in parcheggi_distanze:
        if assegnati >= n_turisti:
            break

        capienza_p = parcheggio.get('capienza', 0)
        if capienza_p <= 0:
            continue

        turisti_restanti = n_turisti - assegnati
        turisti_assegnati_parcheggio = 0
        linee_usate_parcheggio = []

        linee_assoc = sorted(
            linee_per_parcheggio.get(parcheggio['id'], []),
            key=lambda l: geodesic(
                (to_float(l['arrivo_lat']), to_float(l['arrivo_lng'])),
                DOZZA_COORDS
            ).meters
        )

        for linea in linee_assoc:
            capienza_linea = linea.get('capienza', 0)
            viaggi = int(float(str(linea.get('frequenza_giornaliera', 1)).replace(',', '.')))
            capienza_totale_linea = capienza_linea * viaggi

            turisti_su_linea = min(turisti_restanti, capienza_p, capienza_totale_linea)
            if turisti_su_linea > 0:
                linee_usate.add(linea['id'])
                linee_usate_parcheggio.append({'linea_id': linea['id'], 'turisti': turisti_su_linea})
                turisti_assegnati_parcheggio += turisti_su_linea
                assegnati += turisti_su_linea
                capienza_p -= turisti_su_linea
                turisti_restanti = n_turisti - assegnati

            if assegnati >= n_turisti or capienza_p <= 0:
                break

        if not linee_assoc and capienza_p > 0 and turisti_restanti > 0:
            turisti_da_inviare = min(turisti_restanti, capienza_p)
            turisti_assegnati_parcheggio += turisti_da_inviare
            assegnati += turisti_da_inviare

        if turisti_assegnati_parcheggio > 0:
            risultato[parcheggio['nome']] = turisti_assegnati_parcheggio
            p_copy = parcheggio.copy()
            p_copy['linee_usate'] = linee_usate_parcheggio
            parcheggi_usati.append(p_copy)

    linee_utilizzate = [l for l in linee if l['id'] in linee_usate]

    return {
        "risultato": risultato,
        "parcheggi_usati": parcheggi_usati,
        "linee_usate": linee_utilizzate
    }
