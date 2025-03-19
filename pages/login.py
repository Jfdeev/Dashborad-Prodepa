import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State

dash.register_page(__name__, path="/login", name="Login", title="Login")

layout = dbc.Container([
    html.H2("Login", className="text-center"),
    dbc.Input(id="username", placeholder="Usuário", type="text", className="mb-2"),
    dbc.Input(id="password", placeholder="Senha", type="password", className="mb-2"),
    dbc.Button("Entrar", id="login-btn", color="primary", className="mb-2"),
    html.Div(id="login-output", className="mt-2"),
    dcc.Location(id="login-redirect", refresh=True)
])

@dash.callback(
    Output("login-output", "children"),
    Output("login-status", "data"),
    Output("login-redirect", "pathname"),
    Input("login-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def verify_login(n_clicks, username, password):
    # Validação simples; ajuste conforme necessário
    if username == "admin" and password == "1234":
        return "Login bem-sucedido!", True, "/"
    return "Usuário ou senha incorretos.", dash.no_update, dash.no_update
