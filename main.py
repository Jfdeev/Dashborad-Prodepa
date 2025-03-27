import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
server = app.server

app.layout = html.Div([
    dcc.Location(id="url", refresh=True),
    dcc.Store(id="login-status", storage_type="session"),
    dash.page_container
])


# Callback para verificar o login e redirecionar, se necessário
@app.callback(
    Output("url", "pathname"),
    Input("login-status", "data"),
    prevent_initial_call=True
)
def redirect_login(login_status):
    if not login_status:
        return "/login"
    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
