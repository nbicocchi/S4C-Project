# 🏛️ S4C – Microservices Architecture

## Prerequisites

```bash
cd backend/db

sqlite3 utenti.db < ../../sql/utenti.sql
sqlite3 parcheggi.db < ../../sql/parcheggi.sql
sqlite3 linee.db < ../../sql/linee.sql
sqlite3 simulazioni.db < ../../sql/simulazioni.sql
```

## Start

```bash
docker compose up --build --detach
```

## Services & Documentation

| Service             | Host Port | Description            | Swagger Docs                                             |
| ------------------- | --------- |------------------------| -------------------------------------------------------- |
| Backend             | 8080      | Main API               | [http://localhost:8080/docs](http://localhost:8080/docs) |
| Mobility Prediction | 8081      | Tourist prediction API | [http://localhost:8081/docs](http://localhost:8081/docs) |
| Frontend            | 3000      | Web interface          | —                                                        |

## Mobility Prediction

Predicts the number of tourists visiting the Borgo di Dozza, as observed from camera data.
* *date* - The day to predict
* *anomaly* - Specifies whether the day has any events: 0 indicates no events, while 3 represents a major event (including both local events and large events in Bologna or Imola).

```bash
curl -X POST http://localhost:8081/predict \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-06-01",
    "anomaly": "1"
  }'
```


