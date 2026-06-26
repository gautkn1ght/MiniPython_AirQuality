import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
CLEANED_DIR = os.path.join(DATA_DIR, "cleaned")

# Fichier sources
CSV_MESURES = os.path.join(RAW_DIR, "gamedata_mesures.csv")
CSV_STATIONS = os.path.join(RAW_DIR, "stations_referentiel.csv")
DB_PATH = os.path.join(CLEANED_DIR, "db.sqlite")

# Dashboard
MAP_STYLE = "open-street-map"
DEFAULT_CENTER = {"lat": 46.603354, "lon": 1.888334} # Centre de la France