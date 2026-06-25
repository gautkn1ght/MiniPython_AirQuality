import sqlite3
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

DB_PATH = "data/db.sqlite"

def load_data():
    """Charge les données nettoyées depuis SQLite."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM cleaned", conn)
    conn.close()
    return df

# Initialisation de l'application Dash
app = dash.Dash(__name__, title="Analyse Qualité de l'Air - ESIEE")

# 1. Chargement initial des données
df = load_data()

# Extraction de la liste unique des polluants pour le filtre (dropdown)
polluants_disponibles = df['parameter'].unique()

# 2. Structure HTML / Layout de la page Web
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#f4f6f9'}, children=[
    
    # En-tête / Titre
    html.Div(style={'textAlign': 'center', 'marginBottom': '30px', 'padding': '10px', 'backgroundColor': '#1e3d59', 'color': 'white', 'borderRadius': '8px'}, children=[
        html.H1("Baromètre Temporel de la Qualité de l'Air"),
        html.H3(f"Station analysée : {df['station_name'].iloc[0]} (ID: {df['station_id'].iloc[0]})")
    ]),
    
    # Panneau de contrôle (Filtres)
    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'marginBottom': '20px'}, children=[
        html.Label("Sélectionnez le polluant à analyser :", style={'fontWeight': 'bold', 'fontSize': '16px', 'color': '#1e3d59'}),
        dcc.Dropdown(
            id='polluant-dropdown',
            options=[{'label': p.upper(), 'value': p} for p in polluants_disponibles],
            value=polluants_disponibles[0], # Valeur par défaut
            clearable=False,
            style={'marginTop': '10px', 'width': '50%'}
        )
    ]),
    
    # Zone des Graphiques (Carte à gauche, Histogramme à droite)
    html.Div(className='row', style={'display': 'flex', 'gap': '20px'}, children=[
        
        # Bloc Carte Géo
        html.Div(style={'flex': '1', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
            html.H4("Localisation de la station de mesure", style={'color': '#1e3d59', 'textAlign': 'center'}),
            dcc.Graph(id='carte-geoloc')
        ]),
        
        # Bloc Histogramme
        html.Div(style={'flex': '1', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
            html.H4("Distribution des concentrations mesurées", style={'color': '#1e3d59', 'textAlign': 'center'}),
            dcc.Graph(id='histogramme-pollution')
        ])
    ])
])

# 3. Callbacks pour rendre le Dashboard DYNAMIQUE
@app.callback(
    [Output('carte-geoloc', 'figure'),
     Output('histogramme-pollution', 'figure')],
    [Input('polluant-dropdown', 'value')]
)
def update_graphs(polluant_selectionne):
    # Recharger les données pour refléter d'éventuels changements récents dans la base
    df_current = load_data()
    
    # Filtrer le DataFrame selon le polluant choisi
    df_filtre = df_current[df_current['parameter'] == polluant_selectionne]
    
    # Récupérer l'unité correspondante (ex: µg/m³)
    unite = df_filtre['unit'].iloc[0] if not df_filtre.empty else ""
    
    # A. Création de la Carte Géo (Sur un fond de carte gratuit OpenStreetMap)
    # On prend la moyenne ou la dernière ligne connue pour positionner le point unique
    df_station_unique = df_filtre.drop_duplicates(subset=['station_id'])
    
    fig_carte = px.scatter_map(
        df_station_unique,
        lat="latitude",
        lon="longitude",
        hover_name="station_name",
        hover_data={"value": True, "unit": True},
        zoom=13,
        height=400
    )
    fig_carte.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    
    # B. Création de l'Histogramme de distribution
    fig_histo = px.histogram(
        df_filtre,
        x="value",
        nbins=20,
        labels={"value": f"Concentration ({unite})", "count": "Nombre de mesures"},
        color_discrete_sequence=['#ff6f61']
    )
    fig_histo.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin={"r":20,"t":20,"l":20,"b":40},
        xaxis=dict(showgrid=True, gridcolor='#e1e5eb'),
        yaxis=dict(showgrid=True, gridcolor='#e1e5eb')
    )
    
    return fig_carte, fig_histo

if __name__ == '__main__':
    # Lancement du serveur Web local sur le port 8050
    app.run(debug=True, port=8050)