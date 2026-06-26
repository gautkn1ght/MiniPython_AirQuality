import sqlite3
import pandas as pd
from config import DB_PATH

def clean_data():

    connexion = sqlite3.connect(DB_PATH)

    query = """
        SELECT 
            r."Date de début" as date_debut,
            r."nom site" as nom_site,
            r."code site" as code_site,
            r."Polluant" as polluant,
            r."valeur" as valeur,
            r."unité de mesure" as unite,
            s.Latitude as latitude,
            s.Longitude as longitude
        FROM raw r
        INNER JOIN stations s ON r."code site" = s.Code
    """

    print("INFO : Fusion des mesures et coordonnées")
    database_cleaned = pd.read_sql_query(query, connexion)

    if database_cleaned.empty:
        print("ERREUR : La table 'raw' est vide.")
        connexion.close()
        return

    database_cleaned = database_cleaned.dropna(subset=["valeur", "latitude", "longitude"])

    database_cleaned["valeur"] = pd.to_numeric(database_cleaned["valeur"], errors="coerce")
    
    database_cleaned["date_debut"] = pd.to_datetime(database_cleaned["date_debut"], errors="coerce")

    database_cleaned = database_cleaned.dropna(subset=["valeur", "date_debut"])

    print("INFO : Sauvegarde dans la table 'cleaned'")
    database_cleaned.to_sql("cleaned", connexion, if_exists="replace", index=False)

    connexion.close()
    print("RÉUSSITE : Nettoyage terminé et base de données mise à jour !")


if __name__ == "__main__":
    clean_data()