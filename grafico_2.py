from iqoptionapi.stable_api import IQ_Option
import time
import plotext as plt
import pandas as pd


# Credenciais de autenticação
email = 'rubinho132@hotmail.com'
password = 'Caneta007$'
# Autenticar na IQ Option
iqoption = IQ_Option(email, password)
iqoption.connect()

## Autenticar na IQ Option
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

# Inspecionar as colunas disponíveis no DataFrame
print(df.columns)

# Verificar quais colunas estão presentes e selecionar as colunas corretas
if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
    df = df[['open', 'high', 'low', 'close']]
    df.columns = ['Open', 'High', 'Low', 'Close']
elif all(col in df.columns for col in ['open', 'max', 'min', 'close']):
    df = df[['open', 'max', 'min', 'close']]
    df.columns = ['Open', 'High', 'Low', 'Close']
else:
    print("As colunas esperadas não estão presentes no DataFrame")
    exit()

# Preparar os dados para plotext
dates = df.index.strftime('%Y-%m-%d %H:%M').tolist()
opens = df['Open'].tolist()
highs = df['High'].tolist()
lows = df['Low'].tolist()
closes = df['Close'].tolist()

# Configurar plotext para plotagem de candles
plt.candlestick(dates, opens, highs, lows, closes)

# Adicionar título e eixos
plt.title('Gráfico de Candles')
plt.xlabel('Tempo')
plt.ylabel('Preço')

# Exibir o gráfico no terminal
plt.show()

# Desconectar
iqoption.close_connect()