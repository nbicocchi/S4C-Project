# 🧩 Backend – Flask Microservice
Micro-servizio che gestisce:
- Autenticazione degli utenti che vogliono usufruire del servizio
- CRUD parcheggi
- CRUD linee bus
- CRUD simulazioni
- Integrazione con **Mobility API**
- Previsioni per mese dei turisti presenti a Dozza
- Sessioni sicure con Flask-Login
---
#### Requisiti
- Python ≥ 3.9
- SQLite (solo per usarlo fuori da Docker)
---
## Avvio locale (senza Docker)

1. Crea e attiva la *venv*:
```bash
python3 -m venv venv source venv/bin/activate
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. Imposta le variabili d’ambiente:
```bash
cp ../.env.example .env
```
(cambia la SECRET_KEY seguendo le istruzioni all'interno del file appena creato)
4. Avvia il server:
```bash
python app/main.py
```
Il back-end diventa disponibile su:
```bash
http://localhost:8080
```
---
##  Avvio in Docker
```bash
docker build -t backend .
docker run -p 8080:8080 --env-file ../.env backend
```
(Oppure gestito dal docker-compose root)

---
## API principali
### 🔐 Autenticazione
- `POST /api/login`
- `POST /api/admin/login`
- `POST /api/logout`
- `GET /api/userinfo`
### 🚗 Parcheggi
- `GET /api/parcheggi`
- `GET /api/parcheggi/<id>`
- `POST /api/parcheggi`
- `PUT /api/parcheggi/<id>`
- `DELETE /api/parcheggi/<id>`
### 🚌 Linee bus
- `GET /api/linee`
### 🧠 Simulazioni
- `POST /api/sim`
- `GET /api/simulazioni`
- `GET /api/simulazioni/<id>`
- `POST /api/simulazioni/esporta`
- `DELETE /api/simulazioni/<id>`
### 📈 Previsioni
- `POST /api/predizioni`  
    (una previsione al giorno → mobility_api)
---
# 🛠️ Struttura interna
```
backend/
│── app/
│   ├── main.py          ← server Flask
│   ├── api.py           ← blueprint API
│   └── shared/
│        ├── utils.py    ← DB, helper, requests
│        ├── sim.py      ← logica simulazioni
│        ├── geoutils.py ← distanze, parse numerico
│        └── __init__.py
│
├── db/                  ← vuoto, riempito dall’utente
├── sql/                 ← schema SQL
├── requirements.txt
└── Dockerfile

```
