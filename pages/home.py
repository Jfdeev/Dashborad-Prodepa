import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from dash_bootstrap_templates import ThemeSwitchAIO
import plotly.express as px
import pandas as pd

# Registra a página com path "/" para ser a tela principal
dash.register_page(__name__, path="/", name="Home", title="Dashboard Prodepa")

# Definição dos temas
theme_light = "lux"
theme_dark = "darkly"

# Certifique-se de que o CSV esteja no diretório raiz do projeto ou ajuste o caminho
df = pd.read_csv("prodepa.pae.csv")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src="../assets/logo.svg", className="img-fluid"), width=12),
    ]),
    dbc.Row([
        dbc.Col(html.H1("Dashboard Prodepa", className="mb-4"), width=8),
        dbc.Col(ThemeSwitchAIO(aio_id="theme-switch", themes=[dbc.themes.LUX, dbc.themes.DARKLY]), width=2),
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Escolha a variável para análise:"),
            dcc.Dropdown(
                id="tipo_grafico",
                options=[
                    {"label": "Andamento", "value": "Andamento"},
                    {"label": "Urgência", "value": "Urgência"},
                    {"label": "Setor Atual", "value": "SETOR ATUAL"},
                    {"label": "Analista", "value": "Analista"},
                    {"label": "Sistema PAE", "value": "SISTEMA PAE"}
                ],
                value="Andamento",
                clearable=False
            )
        ], width=6),
        dbc.Col([
            html.Label("Escolha o tipo de visualização:"),
            dcc.Dropdown(
                id="tipo_visualizacao",
                options=[
                    {"label": "Gráfico de Barras", "value": "bar"},
                    {"label": "Gráfico de Pizza", "value": "pie"},
                    {"label": "Gráfico de Linhas", "value": "line"},
                    {"label": "Gráfico de Dispersão", "value": "scatter"},
                    {"label": "Gráfico de Área", "value": "area"},
                    {"label": "Gráfico de Radar", "value": "radar"},
                    {"label": "Gráfico de Funil", "value": "funnel"}
                ],
                value="bar",
                clearable=False
            )
        ], width=6)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="grafico"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Button("Ir para Análises", id="analises-btn", className="btn btn-primary", n_clicks=0),
            dcc.Location(id="analises-redirect", refresh=True)
        ], width=12)
    ], className="mt-4"),
    dbc.Row([
        dbc.Col(
            html.P("Desenvolvido por Prodepa - 2025", className="text-center"),
            width=12
        )
    ])
])

# Callback para atualizar o gráfico
@dash.callback(
    Output("grafico", "figure"),
    Input("tipo_grafico", "value"),
    Input("tipo_visualizacao", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme-switch"), "value")
)
def update_graph(tipo_grafico, tipo_visualizacao, theme_switch):
    theme = theme_light if theme_switch else theme_dark
    df_counts = df[tipo_grafico].value_counts().reset_index()
    df_counts.columns = [tipo_grafico, "Quantidade"]
    
    if tipo_visualizacao == "bar":
        fig = px.bar(df_counts, x=tipo_grafico, y="Quantidade", title=f"Distribuição de {tipo_grafico}")
    elif tipo_visualizacao == "pie":
        fig = px.pie(df_counts, names=tipo_grafico, values="Quantidade", title=f"Distribuição de {tipo_grafico}")
    elif tipo_visualizacao == "line":
        fig = px.line(df_counts, x=tipo_grafico, y="Quantidade", title=f"Distribuição de {tipo_grafico}")
    elif tipo_visualizacao == "scatter":
        fig = px.scatter(df_counts, x=tipo_grafico, y="Quantidade", title=f"Distribuição de {tipo_grafico}")
    elif tipo_visualizacao == "area":
        fig = px.area(df_counts, x=tipo_grafico, y="Quantidade", title=f"Distribuição de {tipo_grafico}")
    elif tipo_visualizacao == "radar":
        fig = px.line_polar(df_counts, r="Quantidade", theta=tipo_grafico, line_close=True, title=f"Distribuição de {tipo_grafico}")
    elif tipo_visualizacao == "funnel":
        fig = px.funnel(df_counts, x="Quantidade", y=tipo_grafico, title=f"Distribuição de {tipo_grafico}")
    else:
        fig = px.bar(df_counts, x=tipo_grafico, y="Quantidade", title=f"Distribuição de {tipo_grafico}")
    
    fig.update_layout(template=theme)
    return fig

# Callback para navegação: ao clicar no botão, redireciona para a página de análises
@dash.callback(
    Output("analises-redirect", "pathname"),
    Input("analises-btn", "n_clicks"),
    prevent_initial_call=True
)
def navigate_to_analises(n_clicks):
    if n_clicks:
        return "/analises"
    return dash.no_update
