import os
from src.utils.get_data import raw_data
from src.utils.clean_data import clean_data
from config import DB_PATH

def main():
    if not os.path.exists(DB_PATH):
        print("=== Base de données absente. Initialisation ===")
        raw_data()
        clean_data()
        
    from src.dashboard.app import app
    from src.dashboard.layout import layout
    import src.dashboard.callbacks

    print("=== Lancement du Dashboard ===")
    app.layout = layout
    app.run(debug=True)

if __name__ == "__main__":
    main()