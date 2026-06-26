import dash

app = dash.Dash(__name__, title="Dashboard Pollution Atmosphérique")
app.config.suppress_callback_exceptions = True