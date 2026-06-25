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

app = dash.Dash(__name__, title="Analyse Qualité de l'Air")

df = load_data()
polluants_disponibles = df['parameter'].unique()

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#f4f6f9'}, children=[
    
    # En-tête / Titre
    html.Div(style={'textAlign': 'center', 'marginBottom': '30px', 'padding': '10px', 'backgroundColor': '#1e3d59', 'color': 'white', 'borderRadius': '8px'}, children=[
        html.H1("Baromètre Temporel de la Qualité de l'Air"),
        html.H3(f"Analyse Nationale")
    ]),
    
    # Panneau de contrôle (Filtres)
    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'marginBottom': '20px'}, children=[
        html.Label("Sélectionnez le polluant atmosphérique :", style={'fontWeight': 'bold', 'fontSize': '16px', 'color': '#1e3d59'}),
        dcc.Dropdown(
            id='polluant-dropdown',
            options=[{'label': str(p).upper(), 'value': p} for p in polluants_disponibles],
            value=polluants_disponibles[0],
            clearable=False,
            style={'marginTop': '10px', 'width': '50%'}
        )
    ]),
    
    # Zone des Graphiques (Carte à gauche, Histogramme à droite)
    html.Div(style={'display': 'flex', 'gap': '20px'}, children=[
        
        # Bloc Carte Géo
        html.Div(style={'flex': '1', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
            html.H4("Cartographie des stations", style={'color': '#1e3d59', 'textAlign': 'center'}),
            dcc.Graph(id='carte-geoloc')
        ]),
        
        # Bloc Histogramme
        html.Div(style={'flex': '1', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
            html.H4("Distribution des concentrations", style={'color': '#1e3d59', 'textAlign': 'center'}),
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
    df_current = load_data()

    df_filtre = df_current[df_current['parameter'] == polluant_selectionne]
    unite = df_filtre['unit'].iloc[0] if not df_filtre.empty else "µg/m³"
    
    # Carte Géo
    df_map = df_filtre.groupby(['station_name', 'latitude', 'longitude'], as_index=False)['value'].mean()

    df_map['marker_size'] = df_map['value'].apply(lambda x: max(2, (x + 5) * 3))
    
    fig_carte = px.scatter_map(
        df_map,
        lat="latitude",
        lon="longitude",
        color="value",
        size="marker_size",
        hover_name="station_name",
        hover_data={"value": True, "marker_size": False},
        color_continuous_scale=px.colors.sequential.Reds,
        zoom=5.5,
        height=400
    )
    fig_carte.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    
    # Histogramme
    fig_histo = px.histogram(
        df_filtre,
        x="value",
        nbins=25,
        labels={"value": f"Concentration ({unite})", "count": "Nombre de relevés"},
        color_discrete_sequence=['#4f92ff']
    )
    fig_histo.update_layout(
        margin={"r":20,"t":20,"l":20,"b":40},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#e1e5eb'),
        yaxis=dict(showgrid=True, gridcolor='#e1e5eb')
    )
    
    return fig_carte, fig_histo

if __name__ == '__main__':
    app.run(debug=True, port=8050)