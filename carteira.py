import pandas as pd
import os
from funcoes_graficos import grafico_retorno_modelo


class Carteira():

    def __init__(self, dataCompra, carteiraVigente, nomeCarteira):
        

        dados = pd.read_parquet(r'dados\cotacoes.parquet')
        dados = dados[['data', 'ticker', 'preco_fechamento_ajustado']]
        
        ibov = pd.read_parquet(r'dados\ibov.parquet')
        cdi = pd.read_parquet(r'dados\cdi.parquet')

        self.dados = dados
        
        self.dataCompra = dataCompra
        self.carteiraVigente = carteiraVigente
     
        self.nomeCarteira = nomeCarteira
    
        self.atualizando_carteira()
        self.calculando_rentabilidade()
        self.cotacoes_atualizadas()
        
        self.figRetornoModelo = grafico_retorno_modelo(self.retornoCarteira, ibov, cdi)


    def atualizando_carteira(self):

        dados = self.dados

        if os.path.exists(fr'carteiras\{self.nomeCarteira}.csv'):

            carteiras = pd.read_csv(fr'carteiras\{self.nomeCarteira}.csv')
            ultimaData = str(carteiras.iloc[-1,0])[0:10]

            if ultimaData != self.dataCompra:

                dadosCarteiraVigente = dados[dados['ticker'].isin(self.carteiraVigente)]
                dadosCarteiraVigente = dadosCarteiraVigente[dadosCarteiraVigente['data'] == self.dataCompra]

                carteiraAtualizada = pd.concat([carteiras, dadosCarteiraVigente], ignore_index= True)

                carteiraAtualizada.to_csv(fr'carteiras\{self.nomeCarteira}.csv', index= False)
            
        else:

            dadosCarteiraVigente = dados[dados['ticker'].isin(carteiraVigente)]
            dadosCarteiraVigente = dadosCarteiraVigente[dadosCarteiraVigente['data'] == self.dataCompra]

            carteiraAtualizada = dadosCarteiraVigente.reset_index(drop=True)

            carteiraAtualizada.to_csv(fr'carteiras\{self.nomeCarteira}.csv', index= False)


        self.carteiras = pd.read_csv(fr'carteiras\{self.nomeCarteira}.csv')

    def calculando_rentabilidade(self):

        dados = self.dados
        carteiras = self.carteiras

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

        self.retornoCarteira = retornoCarteira
    
    def cotacoes_atualizadas(self):

        dados = self.dados
        carteiras = self.carteiras

        dataAtual = dados['data'].unique()
        dataAtual = dataAtual[-1]

        carteiraVigente = self.carteiraVigente

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

        self.cotacoesAtualizadas = carteira


if __name__ == "__main__":

 
    dataCompra = '2023-12-11'
    
    carteiraVigente = ['CSED3','CSUD3','KEPL3','LAVV3','MDNE3','PFRM3','SOJA3','TGMA3','VLID3','WIZC3']
    
    nomeCarteira = 'carteira1'

    carteira = Carteira(dataCompra, carteiraVigente, nomeCarteira)
    # carteira.atualizando_carteira()
    # carteira.calculando_rentabilidade()