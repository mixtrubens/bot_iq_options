from iqoptionapi.stable_api import IQ_Option
import time
import pandas as pd
import plotly.graph_objects as go

# Credenciais de autenticação
email = 'rubinho132@hotmail.com'
password = 'Caneta007$'
# Autenticar na IQ Option
iqoption = IQ_Option(email, password)
iqoption.connect()

# Autenticar na IQ Option
iqoption = IQ_Option(email, password)
iqoption.connect()

if iqoption.check_connect():
    print("Autenticado com sucesso")
else:
    print("Erro na autenticação")
    exit()

# Selecionar conta demo
iqoption.change_balance('PRACTICE')

# Definir a moeda (par de moedas) e tempo
currency = "EURUSD"
interval = 1  # Intervalo de 1 minuto
num_candles = 10  # Número de velas

# Obter dados das velas
end_from_time = time.time()
candles = iqoption.get_candles(currency, interval * 60, num_candles, end_from_time)

# Criar um DataFrame com os dados das velas
df = pd.DataFrame(candles)
df['timestamp'] = pd.to_datetime(df['from'], unit='s')
df.set_index('timestamp', inplace=True)

# Selecionar as colunas relevantes e renomeá-las para o formato esperado
df = df[['open', 'max', 'min', 'close']]
df.columns = ['Open', 'High', 'Low', 'Close']

# Criar o gráfico de candle com plotly
fig = go.Figure(data=[go.Candlestick(x=df.index,
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'])])

# Adicionar título e eixos
fig.update_layout(title='Gráfico de Candles',
                  xaxis_title='Tempo',
                  yaxis_title='Preço')

# Exibir o gráfico
fig.show()

# Desconectar
iqoption.close_connect()