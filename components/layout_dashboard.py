from app import *
import pandas as pd
from funcoes_graficos import grafico_candlestick
from dash_bootstrap_templates import load_figure_template
from carteira import Carteira

load_figure_template('slate')

carteira = Carteira(dataCompra= '2023-12-11', carteiraVigente= ['CSED3','CSUD3','KEPL3','LAVV3','MDNE3','PFRM3','SOJA3','TGMA3','VLID3','WIZC3'], nomeCarteira= 'carteira1')

layout_acoes = dbc.Row([
    
    dbc.Col([
        dcc.Dropdown(carteira.carteiraVigente, carteira.carteiraVigente[0], id='dropdown_escolher_acao', style={'border-radius':'8px', 'width': '200px', 'background-color': '#7a7a7a', 'color': 'white'}),
        dcc.Graph(id='grafico_acao_callback', style= {'height': '294px', 'background-color': '#272B30','border-radius': '8px'})
    ]),
    dbc.Col(
        dash_table.DataTable(carteira.cotacoesAtualizadas.to_dict('records'), 
                            style_header= {'backgroundColor': '#7a7a7a','fontWeight': 'bold','border': '0px','font-size': "15px",'color': 'black',"borderRadius": "8px"}, 
                            style_cell={'textAlign': 'center','padding': '4px 4px','backgroundColor': '#d3d3d3',"borderRadius": "8px",'color': 'black'}, 
                            style_data={ 'border': '0px','font-size': "15px"},
                            style_table={ 'borderRadius': '8px', 'overflow': 'hidden'},id= 'tabela_teste')
    )
])

layout_retorno_modelo = dbc.Row(
    
    dbc.Col(dcc.Graph(figure= carteira.figRetornoModelo, style={'height': "470px", 'background-color': '#272B30', 'border-radius': '8px'}))

)

@app.callback(
    Output('grafico_acao_callback', 'figure'),
    Input('dropdown_escolher_acao', 'value')
)

def update_grafico_acao(valor_dropdown):

    dados = pd.read_parquet(r'C:\Users\Caio\Documents\dev\github\dashboard_carteira\dados\cotacoes.parquet')

    fig = grafico_candlestick(valor_dropdown, dados)


    return fig
