import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc

dash.register_page(__name__, path="/analises", name="Análises", external_stylesheets=[dbc.themes.CERULEAN])

df = pd.read_csv("prodepa.pae.csv")

layout = dbc.Container([
    # Cabeçalho com logo e botão
    dbc.Row([
        dbc.Col(html.Img(src="../assets/logo.svg", className="img-fluid", style={"height": "60px"}), width=2),
        dbc.Col(html.H2("Painel de Análises Contratuais", className="text-primary mt-2"), width=8),
        dbc.Col(dbc.Button("Voltar à Home", href="/", color="primary", className="mt-2"), width=2)
    ], className="mb-4 border-bottom pb-2"),
    
    # Linha de introdução
    dbc.Row([
        dbc.Col(html.P("Visualização detalhada dos contratos vencidos e em análise", className="lead"), width=12)
    ], className="mb-4"),
    
    # Primeira linha de gráficos
    dbc.Row([
    dbc.Col(dbc.Card([
        dbc.CardHeader("Distribuição de Contratos por PAE em cada setor"),
        dbc.CardBody(
            dcc.Graph(
                figure={
                    'data': [
                        {
                            'x': df[df['SISTEMA PAE'] == pae].groupby('SETOR ATUAL').size().index,
                            'y': df[df['SISTEMA PAE'] == pae].groupby('SETOR ATUAL').size().values,
                            'name':f'{pae}',
                            'type': 'bar'
                        } for pae in df['SISTEMA PAE'].unique()
                    ],
                    'layout': {
                        'title': 'Distribuição de Andamentos por Setor Atual',
                        'barmode': 'group',  
                        'showlegend': True
                    }
                }
            )
        ),
        dbc.CardFooter("Podemos avaliar e prever a distribuição de contratos por setor")
    ]), width=6),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader("Distribuição de Contratos de cada Analista por Setor"),
            dbc.CardBody(
                dcc.Graph(
                    figure={
                    'data': [
                        {
                            'x': df[df['Analista'] == analista].groupby('SETOR ATUAL').size().index,
                            'y': df[df['Analista'] == analista].groupby('SETOR ATUAL').size().values,
                            'name': analista,
                            'type': 'bar'
                        } for analista in df['Analista'].unique()  # Correção aqui!
                    ],
                    'layout': {
                        'title': 'Distribuição de Analistas por Setor',
                        'barmode': 'group',
                        'showlegend': True,
                        'xaxis': {'title': 'Setor'},
                        'yaxis': {'title': 'Quantidade'}
                    }
                }
            )
        ),
    dbc.CardFooter("Distribuição de responsáveis por processo em cada setor")
    ]), width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Distribuição de Andamento de Contratos por Setor"),
            dbc.CardBody(dcc.Graph(figure={
                'data': [{
                    'x': df[df['Andamento'] == andamento].groupby('SETOR ATUAL').size().index,
                    'y': df[df['Andamento'] == andamento].groupby('SETOR ATUAL').size().values,
                    'name': andamento,
                    'type': 'bar'
                } for andamento in df['Andamento'].unique()],
                'layout': {
                    'title': 'Valores Contratuais por Setor',
                    'barmode': 'group',
                    'showlegend': True,
                }
            })),
            dbc.CardFooter("Deste modo é possivel avaliar o tempo de execução de cada contrato")
        ]), width=6),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader("Distribuição de Leis de Licitação por contrato"),
            dbc.CardBody(dcc.Graph(figure={
                'data': [{
                    'x': df['Lei de licitação'].unique(),
                    'y': df['Lei de licitação'].value_counts(),
                    'type': 'bar',
                    'mode': 'lines+markers'
                }],
                'layout': {
                    'title': 'Renovações Contratuais por Ano',
                    'showlegend': False
                }
            })),
            dbc.CardFooter("Todas as leis de licitação utilizadas em contratos")
        ]), width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Contratos Vencidos - Detalhes"),
            dbc.CardBody(
                dcc.Graph(
                    figure={
                        'data': [{
                            'type': 'table',
                            'header': {'values': ['Nº PAE', 'Analista', 'Instrumento Contratual', 'Cliente', 'Valor Global']},
                            'cells': {
                                'values': [
                                    df[df['Status contratual'] == 'vencido']['Nº PAE'].apply(lambda x: '<br>'.join(x.split(','))),
                                    df[df['Status contratual'] == 'vencido']['Analista'].apply(lambda x: '<br>'.join(x.split(','))),
                                    df[df['Status contratual'] == 'vencido']['Instrumento Contratual'],
                                    df[df['Status contratual'] == 'vencido']['CLIENTE'].apply(lambda x: '<br>'.join(x.split(','))),
                                    df[df['Status contratual'] == 'vencido']['VALOR GLOBAL']
                                ],
                                'align': 'left'
                            }
                        }]
                    }
                )
            ),
            dbc.CardFooter("Lista detalhada de contratos com vigência expirada")
        ]), width=12)
    ])
], fluid=True, style={"padding": "20px"})