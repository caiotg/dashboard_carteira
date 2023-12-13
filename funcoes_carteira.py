import pandas as pd
import os

def data_compra():

    return '2023-12-11'

def carteira_vigente():

    carteiraVigente = ['CSED3','CSUD3','KEPL3','LAVV3','MDNE3','PFRM3','SOJA3','TGMA3','VLID3','WIZC3']

    return carteiraVigente

def adicionando_carteira_vigente(dados, carteiraVigente, dataCompra, nome = ''):

    if os.path.exists(fr'carteiras\{nome}.xlsx'):

        carteiras = pd.read_excel(fr'carteiras\{nome}.xlsx')
        ultimaData = str(carteiras.iloc[-1,0])[0:10]

        if ultimaData != dataCompra:

            dadosCarteiraVigente = dados[dados['ticker'].isin(carteiraVigente)]
            dadosCarteiraVigente = dadosCarteiraVigente[dadosCarteiraVigente['data'] == dataCompra]

            carteiraAtualizada = pd.concat([carteiras, dadosCarteiraVigente], ignore_index= True)

            carteiraAtualizada.to_excel(fr'carteiras\{nome}.xlsx', index= False)
        
    else:

        dadosCarteiraVigente = dados[dados['ticker'].isin(carteiraVigente)]
        dadosCarteiraVigente = dadosCarteiraVigente[dadosCarteiraVigente['data'] == dataCompra]

        carteiraAtualizada = dadosCarteiraVigente.reset_index(drop=True)

        carteiraAtualizada.to_excel(fr'carteiras\{nome}.xlsx', index= False)

def calculando_rentabilidade(dados, carteiras):

    listaDatas = carteiras['data'].unique()

    listaDfs = []

    for i, data in enumerate(listaDatas):

        carteira = carteiras[carteiras['data'] == data]
        
        if i < (len(listaDatas) - 1):

            cotacoesCarteira = dados[(dados['data'] >= data) & (dados['data'] <= listaDatas[i+1])]
            cotacoesCarteira = cotacoesCarteira[cotacoesCarteira['ticker'].isin(carteira['ticker'])]
            cotacoesCarteira['peso'] = 1/(len(carteira))

            listaDfs.append(cotacoesCarteira)

        else:

            cotacoesCarteira = dados[(dados['data'] >= listaDatas[-1])]
            cotacoesCarteira = cotacoesCarteira[cotacoesCarteira['ticker'].isin(carteira['ticker'])]
            cotacoesCarteira['peso'] = 1/(len(carteira))

            listaDfs.append(cotacoesCarteira)
        
    dfCotacoes = listaDfs[0]

    for df in listaDfs[1:]:

        dfCotacoes = pd.concat([dfCotacoes, df], ignore_index= True)


    dfCotacoes['retorno'] = dfCotacoes.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
    dfCotacoes.loc[dfCotacoes['retorno'].isna(), 'retorno'] = 0
    dfCotacoes['retorno_por_acao'] = dfCotacoes['retorno'] * dfCotacoes['peso']
    
    retornoCarteira = dfCotacoes.groupby('data')['retorno_por_acao'].sum()
    retornoCarteira = retornoCarteira.to_frame()
    retornoCarteira['retorno_acum'] = (1 + retornoCarteira['retorno_por_acao']).cumprod() - 1
    retornoCarteira = retornoCarteira.drop('retorno_por_acao', axis=1)
    retornoCarteira = retornoCarteira.reset_index()

    return retornoCarteira

if __name__ == "__main__":

    dados = pd.read_parquet(r'dados\cotacoes.parquet')
    dados = dados[['data', 'ticker', 'preco_fechamento_ajustado']]

    ibov = pd.read_parquet(r'dados\ibov.parquet')
    cdi = pd.read_parquet(r'dados\cdi.parquet')

    adicionando_carteira_vigente(dados, carteira_vigente, data_compra, nome='carteira1')