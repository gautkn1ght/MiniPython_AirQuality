import os
import shutil
import sqlite3
import pandas as pd

CSV_SOURCE = "csv/FR_E2_2026-01-01.csv"
DB_PATH = "data/db.sqlite"
RAW_DIR = "data/raw"

def get_raw_data():
    print("INFO : Récupération des données")
    
    if not os.path.exists(CSV_SOURCE):
        print(f"ERREUR : Le fichier {CSV_SOURCE} est introuvable.")
        return

    os.makedirs(RAW_DIR, exist_ok=True)
    raw_dest = os.path.join(RAW_DIR, "raw_concentration-de-polluants-atmosphérique-reglementes.csv")
    shutil.copyfile(CSV_SOURCE, raw_dest)
    print(f"RÉUSSITE : Fichier brut copié dans : {raw_dest}")

    with open(CSV_SOURCE, "r", encoding="utf-8") as f:
        csv_content = f.read()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            json_payload TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("INSERT INTO raw (json_payload) VALUES (?)", (csv_content,))
    conn.commit()
    conn.close()
    print("RÉUSSITE : Données brutes insérées dans la table 'raw'. (db.sqlite)")

if __name__ == "__main__":
    get_raw_data()