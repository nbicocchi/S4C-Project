import csv
from datetime import datetime
import zipfile
import re
from sqlalchemy import MetaData

def clean_data(engine, items, folder_path, file_type):
    connection = engine.connect()
    metadata = MetaData()
    metadata.reflect(bind=engine)

    for zip_file in items:
        zip_path = folder_path+"/"+zip_file
        print(zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for internal_file in zf.namelist():
                with zf.open(internal_file) as csv_file:
                    reader = csv.reader((line.decode("utf-8").strip() for line in csv_file), delimiter=';')
                    match = re.search(r'\d{8}', internal_file)
                    data_str = match.group(0)
                    data = datetime.strptime(data_str, "%Y%m%d").date()
                    for row in reader:
                        if file_type=="PRESENZE":
                            print("Inseriamo oggetti nella tabella presenze...")
                            presences_table = metadata.tables["presences"]
                            list_key = ["istataa", "classe", "mcc_ace_residenza", "ace_notte_precedente", "ace_notte_successiva", "n_presenze"]
                            row_dict = {}
                            for i in range(len(list_key)):
                                row_dict[list_key[i]] = row[i]
                            row_dict["n_presenze"] = int(float(row_dict["n_presenze"]))
                            row_dict["data_analisi"] = data
                            print(row_dict)
                            if all(row_dict.values()):
                                try:
                                    connection.execute(presences_table.insert(), row_dict)
                                    connection.commit()
                                    print("Riga inserita!")
                                except Exception as e:
                                    print(f"Errore durante l'inserimento: {e}")
                                    connection.rollback()
                            else:
                                print("Riga scartata in quanto incompleta")
                        else:
                            print("Inseriamo oggetti nella tabella spostamenti...")
                            movements_table = metadata.tables["movements"]
                            list_key = ["classe", "i", "id_zonai", "id_zonaj", "spost_zonai_zonaj"]
                            row_dict = {}
                            for i in range(len(list_key)):
                                row_dict[list_key[i]] = row[i]
                            row_dict["i"] = int(row_dict["i"])
                            row_dict["spost_zonai_zonaj"] = int(float(row_dict["spost_zonai_zonaj"]))
                            row_dict["data_analisi"] = data
                            try:
                                connection.execute(movements_table.insert(), row_dict)
                                connection.commit()
                                print("Riga inserita!")
                            except Exception as e:
                                print(f"Errore durante l'inserimento: {e}")
                                connection.rollback()
    connection.close()
    print("Funzione completata")