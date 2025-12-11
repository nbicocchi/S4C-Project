import os
import csv
import zipfile
import re
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, Date, MetaData, create_engine

def create_tables(engine):
    metadata = MetaData()

    # PRESENCES table
    presences_table = Table(
        "presences",
        metadata,
        Column("istataa", String, nullable=False),
        Column("classe", String, nullable=False),
        Column("mcc_ace_residenza", String, nullable=False),
        Column("ace_notte_precedente", String, nullable=True),
        Column("ace_notte_successiva", String, nullable=True),
        Column("n_presenze", Integer, nullable=False),
        Column("data_analisi", Date, nullable=False)
    )

    # MOVEMENTS table
    movements_table = Table(
        "movements",
        metadata,
        Column("classe", String, nullable=False),
        Column("i", Integer, nullable=False),
        Column("id_zonai", String, nullable=False),
        Column("id_zonaj", String, nullable=False),
        Column("spost_zonai_zonaj", Integer, nullable=False),
        Column("data_analisi", Date, nullable=False)
    )

    # Create tables in the database
    metadata.create_all(engine)
    print("Tables created (if not existing)!")

# -----------------------------
# Funzione per caricare presenze
# -----------------------------
def load_presences(engine, items, folder_path):
    connection = engine.connect()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    presences_table = metadata.tables["presences"]

    rows_ok = 0
    rows_failed = 0

    for zip_file in items:
        zip_path = os.path.join(folder_path, zip_file)
        print(f"Elaborazione file: {zip_path}")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for internal_file in zf.namelist():
                with zf.open(internal_file) as csv_file:
                    reader = csv.reader((line.decode("utf-8").strip() for line in csv_file), delimiter=';')
                    match = re.search(r'\d{8}', internal_file)
                    data = datetime.strptime(match.group(0), "%Y%m%d").date()
                    for row in reader:
                        try:
                            row_dict = {
                                "istataa": row[0] or "UNKNOWN",
                                "classe": row[1] or "UNKNOWN",
                                "mcc_ace_residenza": row[2] or "UNKNOWN",
                                "ace_notte_precedente": row[3] or "UNKNOWN",
                                "ace_notte_successiva": row[4] or "UNKNOWN",
                                "n_presenze": int(float(row[5])) if row[5] else 0,
                                "data_analisi": data
                            }
                            connection.execute(presences_table.insert(), row_dict)
                            connection.commit()
                            rows_ok += 1
                        except Exception as e:
                            print(f"Errore durante l'inserimento: {e}")
                            connection.rollback()
                            rows_failed += 1

    connection.close()
    print(f"Presenze inserite: {rows_ok}, inserimenti falliti: {rows_failed}")

# -----------------------------
# Funzione per caricare movimenti
# -----------------------------
def load_movements(engine, items, folder_path):
    connection = engine.connect()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    movements_table = metadata.tables["movements"]

    for zip_file in items:
        zip_path = os.path.join(folder_path, zip_file)
        print(zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for internal_file in zf.namelist():
                with zf.open(internal_file) as csv_file:
                    reader = csv.reader((line.decode("utf-8").strip() for line in csv_file), delimiter=';')
                    match = re.search(r'\d{8}', internal_file)
                    data = datetime.strptime(match.group(0), "%Y%m%d").date()
                    for row in reader:
                        row_dict = {
                            "classe": row[0],
                            "i": int(row[1]),
                            "id_zonai": row[2],
                            "id_zonaj": row[3],
                            "spost_zonai_zonaj": int(float(row[4])),
                            "data_analisi": data
                        }
                        try:
                            connection.execute(movements_table.insert(), row_dict)
                            connection.commit()
                            print("Riga inserita!")
                        except Exception as e:
                            print(f"Errore durante l'inserimento: {e}")
                            connection.rollback()
    connection.close()
    print("Movimenti caricati!")

# -----------------------------
# Esempio di utilizzo
# -----------------------------
engine = create_engine("postgresql://admin:admin123@localhost:5432/DozzaDB")

# Create tables if missing
create_tables(engine)

folder_path_presences = "../AIRI/dozza_presenze"
items_presences = os.listdir(folder_path_presences)
load_presences(engine, items_presences, folder_path_presences)

#folder_path_movements = "../AIRI/dozza_spostamenti"
#items_movements = os.listdir(folder_path_movements)
#load_movements(engine, items_movements, folder_path_movements)