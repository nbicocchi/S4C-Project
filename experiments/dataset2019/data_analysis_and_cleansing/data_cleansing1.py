from Funz import clean_data
import os
from sqlalchemy import create_engine

#Inserire variabili per connettersi a SQL
db_user = " "
db_password = " "
db_host = " "
db_port = " "
db_name = " "
#Inserire path dei file da caricare nel database
folder_path = " "

connection = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(connection)

items = os.listdir(folder_path)
clean_data(engine, items, folder_path)