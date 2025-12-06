# 🏛️ S4C – Microservices Architecture

## Prerequisites

```
cd backend/db

sqlite3 utenti.db < ../../sql/utenti.sql
sqlite3 parcheggi.db < ../../sql/parcheggi.sql
sqlite3 linee.db < ../../sql/linee.sql
sqlite3 simulazioni.db < ../../sql/simulazioni.sql
```

## Start

```
docker compose up --build --detach
```

## Services

| Servizio            | Host port | Descrizione                   |
|---------------------| --------- | ----------------------------- |
| Backend             | 8080      | API principale                |
| Mobility Prediction | 8081      | API per previsioni turistiche |
| Frontend            | 3000      | Interfaccia web               |

## Mobility Prediction

```text
curl -X POST http://localhost:8081/predict \
  -H "Content-Type: application/json" \
  -d '{
"date": "2025-06-01",
"layerid": "08|037|025|000|000"
}'
```