import sqlite3
import pandas as pd
import io
import os

DB_PATH = "data/db.sqlite"
CLEANED_DIR = "data/cleaned"

COORDINATES_MAP = {
    "Metz-Centre": (49.1193, 6.1757),
    "Baume-les-Dames": (47.3509, 6.3614),
    "Besançon": (47.2378, 6.0244),
    "Dijon": (47.3220, 5.0415),
    "Nancy": (48.6921, 6.1844),
    "Strasbourg": (48.5734, 7.7521),
    "Besançon-Châteaufarine": (47.2255, 5.9433),
    "Dijon-Champmaillot": (47.3262, 5.0645),
    "Metz-Borny": (49.1147, 6.2201),
    "Strasbourg-Clemenceau": (48.5912, 7.7478),
    "Nancy-Centre": (48.6900, 6.1800)
}

def clean_and_store_data():
    print("INFO : Nettoyage et structuration des données CSV...")

    os.makedirs(CLEANED_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT json_payload FROM raw ORDER BY fetched_at DESC LIMIT 1")
        csv_data = cursor.fetchone()[0]
    except sqlite3.OperationalError:
        print("ERREUR : La table 'raw' n'existe pas. Éxecuter get_data.py.")
        conn.close()
        return

    if not csv_data:
        print("ERREUR : Aucun enregistrement trouvé.")
        conn.close()
        return

    # Convertir le texte brut CSV en DataFrame Pandas
    df = pd.read_csv(io.StringIO(csv_data), sep=";")
    
    # Sélection des colonnes
    df_cleaned = df[[
        'nom site', 'Polluant', 'valeur brute', 'unité de mesure', 'Date de début', 'Date de fin' ]].dropna()
    
    # Renommer les colonnes
    df_cleaned = df_cleaned.rename(columns={
        'nom site': 'station_name',
        'Polluant': 'parameter',
        'valeur brute' : 'value',
        'unité de mesure' : 'unit',
        'Date de début' : 'dateDébut',
        'Date de fin': 'dateFin'
    })
    
    df_cleaned['latitude'] = df_cleaned['station_name'].apply(lambda x: COORDINATES_MAP.get(x, (47.0, 6.0))[0])
    df_cleaned['longitude'] = df_cleaned['station_name'].apply(lambda x: COORDINATES_MAP.get(x, (47.0, 6.0))[1])

    df_cleaned['station_id'] = df_cleaned['station_name'].astype('category').cat.codes

    df_cleaned.to_sql("cleaned", conn, if_exists="replace", index=False)
    conn.close()
    print("RÉUSSITE : Données insérées dans la table 'cleaned'. (SQLite)")
    
    csv_cleaned_path = os.path.join(CLEANED_DIR, "cleaned_concentration-de-polluants-atmosphérique-reglementes.csv")
    df_cleaned.to_csv(csv_cleaned_path, index=False)
    print(f"RÉUSSITE : Copie CSV propre sauvegardée dans : {csv_cleaned_path}")

if __name__ == "__main__":
    clean_and_store_data()