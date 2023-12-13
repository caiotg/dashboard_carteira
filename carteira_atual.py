import pandas as pd
from funcoes_carteira import carteira_vigente

def cotacoes_carteira_vigente(nome_carteira = ''):

    dados = pd.read_parquet(r'dados\cotacoes.parquet')
    dados = dados[['data', 'ticker', 'preco_fechamento_ajustado']]

    carteiras = pd.read_excel(fr'carteiras\{nome_carteira}.xlsx')

    dataAtual = dados['data'].unique()
    dataAtual = dataAtual[-1]

    carteiraVigente = carteira_vigente()

    precoAtual = dados[(dados['ticker'].isin(carteiraVigente)) & (dados['data'] == dataAtual)]
    precoAtual = precoAtual.sort_values(by= 'ticker')
    precoAtual = precoAtual.reset_index()
    precoAtual = precoAtual['preco_fechamento_ajustado']

    dataCompra = carteiras['data'].unique()
    dataCompra = dataCompra[-1]

    carteira = dados[(dados['ticker'].isin(carteiraVigente)) & (dados['data'] == dataCompra)]
    carteira = carteira.sort_values(by= 'ticker')
    carteira = carteira.reset_index()
    carteira = carteira.assign(preco_atual = precoAtual)
    carteira = carteira[['ticker','preco_fechamento_ajustado', 'preco_atual']]
    carteira.columns = ['Ticker', f'Preco Compra ({str(dataCompra)[0:10]})', f'Preco {str(dataAtual)[0:10]}']

    return carteira
