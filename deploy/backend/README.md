```bash
mkdir db
cd db
sqlite3 db.sqlite3 < ../../sql/simulazioni.sql
sqlite3 db.sqlite3 < ../../sql/linee.sql
sqlite3 db.sqlite3 < ../../sql/parcheggi.sql
```
