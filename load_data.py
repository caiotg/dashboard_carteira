import requests
import pandas as pd
import os
import urllib.request
import dotenv

def pegar_cotacoes(headers):

    response = requests.get(f'https://api.fintz.com.br/bolsa/b3/avista/cotacoes/historico/arquivos?classe=ACOES&preencher=true', headers= headers)

    linkDownload = (response.json())['link']

    urllib.request.urlretrieve(linkDownload, f'cotacoes.parquet')

    df = pd.read_parquet('cotacoes.parquet')

    colunasPraAjustar = ['preco_abertura', 'preco_maximo', 'preco_medio', 'preco_minimo']

    for coluna in colunasPraAjustar:

        df[f'{coluna}_ajustado'] = df[coluna] * df['fator_ajuste']

    df['preco_fechamento_ajustado'] = df.groupby('ticker')['preco_fechamento_ajustado'].transform('ffill')

    df = df.sort_values('data', ascending=True)

    df.to_parquet('cotacoes.parquet', index= False)


def ibov(headers):

    response = requests.get('https://api.fintz.com.br/indices/historico?indice=IBOV&dataInicio=2000-01-01', headers=headers)

    df = pd.DataFrame(response.json())
    df = df.sort_values('data', ascending= True)
    df.columns = ['indice', 'data', 'fechamento']
    df = df.drop('indice', axis=1)

    df.to_parquet('ibov.parquet', index= False)


def cdi(headers):

    response = requests.get('https://api.fintz.com.br/taxas/historico?codigo=12&dataInicio=2000-01-01&ordem=ASC', headers= headers)

    cdi = pd.DataFrame(response.json())
    cdi = cdi.drop(["dataFim", 'nome'], axis = 1)
    cdi.columns = ['data', 'retorno']
    cdi['retorno'] = cdi['retorno']/100 

    cdi.to_parquet('cdi.parquet', index = False)


if __name__ == "__main__":
    
    dotenv.load_dotenv()

    os.chdir(r'C:\Users\Caio\Documents\dev\github\rentabilidade_carteira\dados')

    chaveApi = os.getenv('API_FINTZ')
    headers = {'accept': 'application/json',
            'X-API-Key': chaveApi}

    pegar_cotacoes(headers= headers)
    ibov(headers= headers)
    cdi(headers=headers)