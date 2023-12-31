import datetime
import pandas as pd
import plotly.graph_objects as go

def grafico_candlestick(valor_dropdown, dados):

    dados['data'] = pd.to_datetime(dados['data']).dt.date
    dados = dados[['data','ticker','preco_abertura_ajustado','preco_maximo_ajustado','preco_minimo_ajustado','preco_fechamento_ajustado']]

    ultimoDia = dados['data'].unique()

    hoje = datetime.datetime.date(datetime.datetime.today())
    cincoDiasAtras = hoje - datetime.timedelta(days=30)


    cotacoes = dados[dados['ticker'] == valor_dropdown]
    cotacoes = cotacoes[(cotacoes['data'] <= ultimoDia[-1]) & (cotacoes['data'] >= cincoDiasAtras)]

    layout = go.Layout(yaxis= dict(tickfont=dict(color="#D3D6DF"), showline = False), xaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False), template= 'slate')

    graficoCandleStick = go.Figure(data= [go.Candlestick(
        x= cotacoes['data'],
        open= cotacoes['preco_abertura_ajustado'],
        high= cotacoes['preco_maximo_ajustado'],
        low= cotacoes['preco_minimo_ajustado'],
        close= cotacoes['preco_fechamento_ajustado'])
        ], layout= layout)

    graficoCandleStick.update_layout(xaxis_rangeslider_visible=False)
    graficoCandleStick.update_xaxes(rangebreaks=[dict(bounds=['sat','mon'])])
    graficoCandleStick.update_layout(margin= dict(l=16, r=16, t=16, b=16))
    graficoCandleStick.update_layout(paper_bgcolor='rgba(0,0,0,0)')

    return graficoCandleStick

def grafico_retorno_modelo(retornoModelo, ibov, cdi):

    dfRetornoModelo = retornoModelo
    dfRetornoModelo['data'] = pd.to_datetime(dfRetornoModelo['data'])
    dfRetornoModelo = dfRetornoModelo.set_index('data')

    ibov = ibov
    ibov['data'] = pd.to_datetime(ibov['data'])
    ibov = ibov.set_index('data')

    ibov = ibov[ibov.index.isin(dfRetornoModelo.index)]
    ibov['retorno'] = ibov['fechamento'].pct_change()
    ibov.iloc[0,1] = 0
    ibov['retorno_acum'] = (1 + ibov['retorno']).cumprod() - 1

    cdi = cdi
    cdi['data'] = pd.to_datetime(cdi['data'])
    cdi = cdi.set_index('data')
    
    cdi = cdi[cdi.index.isin(dfRetornoModelo.index)]
    cdi['retorno_acum'] = (1 + cdi['retorno']).cumprod() - 1


    layout = go.Layout(template= 'slate')

    graficoRetornoModelo = go.Figure(
        data = [go.Scatter(x= dfRetornoModelo.index, y= ibov['retorno_acum'], name='IBOV',line_shape='spline'), go.Scatter(x= dfRetornoModelo.index, y= dfRetornoModelo['retorno_acum'], name='Carteira',line_shape='spline'), go.Scatter(x= dfRetornoModelo.index, y= cdi['retorno_acum'], name='CDI',)], layout= layout
    )
    
    graficoRetornoModelo.update_layout(template= 'slate')
    graficoRetornoModelo.update_xaxes(showgrid= False)
    graficoRetornoModelo.update_yaxes(showgrid= False)
    graficoRetornoModelo.update_layout(margin= dict(l=16, r= 16, t=16, b= 16))
    graficoRetornoModelo.update_layout(paper_bgcolor='rgba(0,0,0,0)')

    graficoRetornoModelo.update_layout(yaxis= dict(tickformat='.1%', tickfont= dict(color= '#d3d3d3')), xaxis= dict(tickfont= dict(color= '#d3d3d3')))
    graficoRetornoModelo.add_vline(dfRetornoModelo.index[0], line_color= '#d3d3d3')
    graficoRetornoModelo.add_hline(dfRetornoModelo['retorno_acum'].min() - 0.01, line_color= '#d3d3d3')

    return graficoRetornoModelo