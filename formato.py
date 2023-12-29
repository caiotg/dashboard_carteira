import dash_bootstrap_components as dbc
from app import *
from components import layout_dashboard

app.layout = dbc.Container(

    dbc.Row(

        dbc.Col([

            dbc.Row([
                dbc.Col(html.H2(children= 'Gráfico Ação', className='titulo-dash'), style= {'display': 'flex', 'justify-content': 'center'}),
                dbc.Col(html.H2(children= 'Ativos na Carteira', className='titulo-dash'), style= {'display': 'flex', 'justify-content': 'center'})
            ]),

            layout_dashboard.layout_acoes,

            dbc.Row([
                dbc.Col(),
                dbc.Col(html.H2(children= 'Retorno Acumulado', className='titulo-dash'), style= {'display': 'flex', 'justify-content': 'center'}),
                dbc.Col()
            ]),
            
            layout_dashboard.layout_retorno_modelo,
        ])
    ), fluid= True, style= {'height': '100vh', 'width': '100%', 'padding': '25px 25px 0px 25px', 'background-color': '#131516'}
)

if __name__ == '__main__':

    app.run_server(debug= True, port= 8051)














