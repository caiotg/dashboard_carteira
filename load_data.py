import requests
import pandas as pd
import os
import urllib.request
import dotenv

def pegar_cotacoes(headers, dataInicio):

    response = requests.get('https://api.fintz.com.br/bolsa/b3/avista/cotacoes/historico/arquivos?classe=ACOES&preencher=true', headers= headers)

    linkDownload = (response.json())['link']

    urllib.request.urlretrieve(linkDownload, f'cotacoes.parquet')

    df = pd.read_parquet('cotacoes.parquet')

    colunasPraAjustar = ['preco_abertura', 'preco_maximo', 'preco_medio', 'preco_minimo']

    for coluna in colunasPraAjustar:

        df[f'{coluna}_ajustado'] = df[coluna] * df['fator_ajuste']

    df['preco_fechamento_ajustado'] = df.groupby('ticker')['preco_fechamento_ajustado'].transform('ffill')

    df = df.loc[df['data'] >= dataInicio]
    
    df = df.sort_values('data', ascending=True)

    df.to_parquet('cotacoes.parquet', index= False)


def ibov(headers, dataInicio):

    response = requests.get(f'https://api.fintz.com.br/indices/historico?indice=IBOV&dataInicio={dataInicio}', headers=headers)

    df = pd.DataFrame(response.json())
    df = df.sort_values('data', ascending= True)
    df.columns = ['indice', 'data', 'fechamento']
    df = df.drop('indice', axis=1)

    df.to_parquet('ibov.parquet', index= False)


def cdi(headers, dataInicio):

    response = requests.get(f'https://api.fintz.com.br/taxas/historico?codigo=12&dataInicio={dataInicio}&ordem=ASC', headers= headers)

    cdi = pd.DataFrame(response.json())
    cdi = cdi.drop(["dataFim", 'nome'], axis = 1)
    cdi.columns = ['data', 'retorno']
    cdi['retorno'] = cdi['retorno']/100 

    cdi.to_parquet('cdi.parquet', index = False)


if __name__ == "__main__":
    
    dotenv.load_dotenv()

    os.chdir(r'C:\Users\Caio\Documents\dev\github\dashboard_carteira\dados')

    chaveApi = os.getenv('API_FINTZ')
    headers = {'accept': 'application/json',
            'X-API-Key': chaveApi}

    dataInicio = '2023-09-01'

    pegar_cotacoes(headers= headers, dataInicio= dataInicio)
    ibov(headers= headers, dataInicio= dataInicio)
    cdi(headers=headers, dataInicio= dataInicio)