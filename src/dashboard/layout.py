import sqlite3
from dash import dcc, html
from config import DB_PATH

def get_pollutants_list():
    connexion = sqlite3.connect(DB_PATH)
    cursor = connexion.cursor()
    cursor.execute("SELECT DISTINCT polluant FROM cleaned")
    type_polluants = [row[0] for row in cursor.fetchall()]
    connexion.close()
    return type_polluants

liste_type_polluants = get_pollutants_list()

layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "padding": "20px",
        "backgroundColor": "#f4f6f9",
    },
    children=[
        html.H1(
            "Visualisation en Temps Réel de la Pollution Atmosphérique",
            style={"textAlign": "center", "color": "#2c3e50"},
        ),
        html.Hr(),
        # Barre de sélection
        html.Div(
            [
                html.Label(
                    "Sélectionnez un polluant réglementé :",
                    style={"fontWeight": "bold", "marginBottom": "5px"},
                ),
                dcc.Dropdown(
                    id="polluant-dropdown",
                    options=[{"label": p, "value": p} for p in liste_type_polluants],
                    value=(
                        liste_type_polluants[0] if liste_type_polluants else None
                    ),  # Valeur par défaut
                    clearable=False,
                    style={"width": "300px"},
                ),
            ],
            style={"marginBottom": "30px"},
        ),
        # Zone des graphiques (côte à côte)
        html.Div(
            style={"display": "flex", "flexWrap": "wrap", "gap": "20px"},
            children=[
                # Carte Géographique
                html.Div(
                    [
                        html.H3(
                            "Localisation des stations de mesure",
                            style={"color": "#34495e"},
                        ),
                        dcc.Graph(id="carte-pollution"),
                    ],
                    style={"flex": "1", "minWidth": "450px"},
                ),
                # Histogramme
                html.Div(
                    [
                        html.H3(
                            "Distribution des concentrations",
                            style={"color": "#34495e"},
                        ),
                        dcc.Graph(id="histogramme-pollution"),
                    ],
                    style={"flex": "1", "minWidth": "450px"},
                ),
            ],
        ),
    ],
)