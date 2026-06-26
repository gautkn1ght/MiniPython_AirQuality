import sqlite3
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from config import DB_PATH, MAP_STYLE, DEFAULT_CENTER
from src.dashboard.app import app

@app.callback(
    [Output("carte-pollution", "figure"), 
     Output("histogramme-pollution", "figure")],
    [Input("polluant-dropdown", "value")],
)

def update_graphs(polluant_selectionne):
    if not polluant_selectionne:
        return {}, {}

    connexion = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM cleaned WHERE polluant = ?"
    database = pd.read_sql_query(query, connexion, params=(polluant_selectionne,))
    connexion.close()

    if database.empty:
        return {}, {}
    
    database["taille_carte"] = database["valeur"].clip(lower=0) + 2

    fig_map = px.scatter_map(
        database,
        lat="latitude",
        lon="longitude",
        hover_name="nom_site",
        hover_data=["valeur", "unite"],
        color="valeur",
        color_continuous_scale="Reds",
        size="taille_carte",
        size_max=15,
        zoom=5,
        center=DEFAULT_CENTER,  # Centre sur la France
    )
    fig_map.update_layout(
        mapbox_style=MAP_STYLE, margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    fig_hist = px.histogram(
        database,
        x="valeur",
        nbins=30,
        labels={
            "valeur": f"Concentration ({database['unite'].iloc[0] if not database.empty else ''})"
        },
        color_discrete_sequence=["#3498db"],
    )
    fig_hist.update_layout(
        bargap=0.1,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin={"t": 20},
    )

    return fig_map, fig_hist