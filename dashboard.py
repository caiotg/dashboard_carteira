import dash_bootstrap_components as dbc
import dash
import pandas as pd
from dash import Dash, html, dcc, dash_table, callback
from dash.dependencies import Input, Output
from funcoes_graficos import grafico_candlestick
from carteira import Carteira


carteira = Carteira(dataCompra= '2023-12-11', carteiraVigente= ['CSED3','CSUD3','KEPL3','LAVV3','MDNE3','PFRM3','SOJA3','TGMA3','VLID3','WIZC3'], nomeCarteira= 'carteira1')

app = dash.Dash(
    external_stylesheets=[dbc.themes.SLATE]
)

app.layout = html.Main([

    dbc.Row([

        dbc.Col(html.H2(children= 'Gráfico Ação', className='titulo-dash'), style= {'display': 'flex', 'justify-content': 'center'}),
        dbc.Col(html.H2(children= 'Ativos na Carteira', className='titulo-dash'),style= {'display': 'flex', 'justify-content': 'center'}),

    ]),

    dbc.Row(

        [

            dbc.Col([

                html.Div(dcc.Dropdown(carteira.carteiraVigente, carteira.carteiraVigente[0], id='dropdown_escolher_acao', style={'margin-left': '50px','border-radius':'8px', 'width': '850px'})),
                html.Div(children= dcc.Graph(id='grafico_acao_callback', style= {'margin-left': '100px', 'margin-right': '0px','height': '293px', 'width': '850px', 'border-radius': '8px', 'background-color': 'white'})),
         
        ]),

            dbc.Col(

                dash_table.DataTable(carteira.cotacoesAtualizadas.to_dict('records'), 
                                     style_header= {'backgroundColor': '#d3d3d3','fontWeight': 'bold','border': '0px','font-size': "15px",'color': 'black',"borderRadius": "8px"}, 
                                     style_cell={'textAlign': 'center','padding': '4px 4px','backgroundColor': 'white',"borderRadius": "8px",'color': 'black'}, 
                                     style_data={ 'border': '0px','font-size': "15px"},
                                     style_table={ 'borderRadius': '8px', 'overflow': 'hidden'},id= 'tabela_teste'),
                                     style={'margin-right': '100px',}

            )

        ],

        align="center",

    ),

    dbc.Row(

        dbc.Col(html.H2(children= 'Retorno Acumulado', className='titulo-dash'), style= {'display': 'flex', 'justify-content': 'center'})

    ),
    dbc.Row(

        dbc.Col([
            html.Div(dcc.Graph(figure= carteira.figRetornoModelo, style={'height': "470px",'margin-right':'100px', 'margin-left': '100px', 'margin-bottom': '16px','border-radius':'8px', 'background-color': 'white', 'border': "2px solid #212946"}))
        ])
    )

])

@app.callback(

    Output('grafico_acao_callback', 'figure'),
    Input('dropdown_escolher_acao', 'value')
)

def criando_grafico_acao(valor_dropdown):

    dados = pd.read_parquet(r'dados\cotacoes.parquet')

    fig = grafico_candlestick(valor_dropdown, dados)

    return fig

if __name__ == '__main__': 
    app.run(debug=True)
