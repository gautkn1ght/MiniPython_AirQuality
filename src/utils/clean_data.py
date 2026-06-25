import sqlite3
import pandas as pd
import io
import os

DB_PATH = "data/db.sqlite"
CLEANED_DIR = "data/cleaned"

def clean_and_store_data():
    print("INFO : Nettoyage et structuration des données CSV...")

    os.makedirs(CLEANED_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT json_payload FROM raw ORDER BY fetched_at DESC LIMIT 1")
        row = cursor.fetchone()
    except sqlite3.OperationalError:
        print("❌ Erreur : La table 'raw' n'existe pas. Lancez get_data.py d'abord.")
        conn.close()
        return

    if not row:
        print("❌ Aucun enregistrement trouvé.")
        conn.close()
        return

    # Convertir le texte brut CSV en DataFrame Pandas
    csv_data = row[0]
    df = pd.read_csv(io.StringIO(csv_data))
    
    # Sélection et renommage des colonnes nécessaires pour notre Dashboard
    # On s'assure de ne garder que les lignes avec des valeurs valides
    df_cleaned = df[[
        'location_id', 'location_name', 'parameter', 
        'value', 'unit', 'datetimeLocal', 'latitude', 'longitude'
    ]].dropna(subset=['value', 'latitude', 'longitude'])
    
    # Renommer pour correspondre à notre structure cible
    df_cleaned = df_cleaned.rename(columns={
        'location_id': 'station_id',
        'location_name': 'station_name',
        'datetimeLocal': 'date'
    })

    # Stockage dans la table 'cleaned'
    df_cleaned.to_sql("cleaned", conn, if_exists="replace", index=False)
    conn.close()
    print("RÉUSSITE : Données insérées avec succès dans la table SQLite 'cleaned'.")
    
    # 2. Sauvegarde d'une copie CSV propre dans data/cleaned/ (Bonne pratique)
    csv_cleaned_path = os.path.join(CLEANED_DIR, "measurements_cleaned.csv")
    df_cleaned.to_csv(csv_cleaned_path, index=False)
    print(f"INFO : Copie CSV propre sauvegardée dans : {csv_cleaned_path}")

if __name__ == "__main__":
    clean_and_store_data()