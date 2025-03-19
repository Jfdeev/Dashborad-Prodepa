import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

dash.register_page(__name__, path="/analises", name="Análises")

layout = dbc.Container([
    html.H2("Análises Avançadas"),
    html.P("Aqui você pode visualizar gráficos mais detalhados."),
    # Adicione outros componentes e gráficos conforme necessário
])
