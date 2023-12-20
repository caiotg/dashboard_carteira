# Dashboar para carteira de investimentos

Esse projeto foi feito para acompanhar a rentabilidade acumulada de uma carteira de investimentos. O dashboard tem um gráfico de candlestick com os últimos 30 dias de negociaçãos das ações presentes na carteira, uma tabela com os ativos da carteira e o preço de compra e um gráfico com a rentabilidade acumulada da carteira comparada ao ibov e cdi.

* obs: o projeto foi pensado para ser usado no Windows, para usar no Linux é preciso trocar as \ por / nos nomes dos arquivos para funcionar.

  ## Carteiras
  Na pasta carteiras é onde fica armazenado o csv com as carteiras mensais, para criar mais de uma carteira basta apenas mudar o paramentro nomeCarteira na classe Carteira.

  ## Dados
  Os dados utilizados são retirados da API da FINTZ, os parquets usados para fazer backtest e criar as carteiras mensais são aproveitados para fazer esse dashboard. A forma como os parquets são baixados está disponível no arquivo load_data.py.

  ## Dashboard
  Para rodar o dashboard é preciso criar um objeto chamdo carteira usando a classe Carteira. Nesse construtor é preciso passar 3 parâmetros: dataCompra, carteiraVigente e nomeCarteira. Os gráficos de candlestick e retorno acumulado são criados a partir das funções grafico_candlestick e grafico_retorno_modelo. O gráfico de candlestick é feito atráves de um callback, assim ao mudar o ativo no dropdown o gráfico é atualizado. A tebela com os ativos da carteira é feita a partir da carteira vigente e da funçõa cotacoes_atulizadas presentes na Carteira.

  Na classe Carteira é onde o csv com a carteira mensal é atualizada ou criada. Além disso, também é calculada a rentabilidade do modelo e feita a leitura dos dados baixados.

  Para que tudo funcione mude o caminho dos arquivos para o local onde os dados estão sendo baixados e as carteiras armazenadas.
