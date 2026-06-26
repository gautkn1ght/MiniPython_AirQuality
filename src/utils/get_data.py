import os
import sqlite3
import pandas as pd
from config import DB_PATH, CSV_MESURES, CSV_STATIONS

def raw_data():

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    connexion = sqlite3.connect(DB_PATH)

    print(f"INFO : Insertion de {CSV_MESURES} dans la table 'raw'")
    database_mesures = pd.read_csv(CSV_MESURES, sep=";", low_memory=False)
    database_mesures.to_sql("raw", connexion, if_exists="replace", index=False)

    print(f"INFO : Insertion de {CSV_STATIONS} dans la table 'stations'")
    database_stations = pd.read_csv(CSV_STATIONS, sep=";", low_memory=False)
    database_stations.to_sql("stations", connexion, if_exists="replace", index=False)

    connexion.close()
    print("SUCCESS : terminée avec succès !")

if __name__ == "__main__":
    raw_data()