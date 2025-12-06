import csv
from datetime import datetime, timedelta
from sqlalchemy import MetaData

def clean_data(engine,items,folder_path):
    connection = engine.connect()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    movements_table = metadata.tables['movements']

    count_file = 0
    # Per tutti i file contenuti nella cartella
    for file in items:
        print("Controllo il file n", count_file)
        with open(folder_path+"/"+file) as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar="'")
            count = 0
            # Per tutte le righe del file csv
            for row in reader:
                # Controlla direttamente i dati ignorando l'header
                if count > 0:
                    datefrom_str = row[1]
                    dateto_str = row[2]
                    datefrom = datetime.strptime(datefrom_str, "%Y-%m-%d %H:%M:%S")
                    dateto = datetime.strptime(dateto_str, "%Y-%m-%d %H:%M:%S")
                    if datefrom < dateto:  # Se la partenza è precedente all'arrivo
                        duration = dateto - datefrom
                        if duration > timedelta(hours=1):
                            print("Il viaggio è durato più di un'ora.")
                        else:  # Controlla che la somma di ogni tipologia di variabile coincida con datavalue, se si lo carica nel database
                            n = float(row[6]) + float(row[7])
                            t = float(row[8]) + float(row[9])
                            g = float(row[10]) + float(row[11])
                            f = float(row[12]) + float(row[13]) + float(row[14]) + float(row[15]) + float(row[16]) + float(row[17])
                            if n == t and t == g and g == f and f == float(row[3]):
                                for i in range(len(row[6:])):
                                    i += 6
                                    data = int(float(row[i]))
                                    row[i] = data
                                list_key = ["layerid","datefrom","dateto","datavalue","toid","toname","ni","ns","tb","tc","gm","gf","f1","f2","f3","f4","f5","f6"]
                                row_dict = {}
                                for e in range(len(list_key)):
                                    row_dict[list_key[e]] = row[e]
                                try:
                                    connection.execute(movements_table.insert(), row_dict)
                                    connection.commit()
                                except Exception as e:
                                    print(f"Errore durante l'inserimento: {e}")
                                    print(f"Non sono riuscito a caricare la riga numero {count} del file {file}")
                                    break
                count += 1  # Passa la riga successiva
        count_file += 1  # Passa il file successivo
    print("Terminato il controllo dei file")
    connection.close()