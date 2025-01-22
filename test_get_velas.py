from iqoptionapi.stable_api import IQ_Option
import time
from configobj import ConfigObj
import websocket
import json
import time

# Insira suas credenciais
config = ConfigObj('config.txt')
email = config['LOGIN']['email']
password = config['LOGIN']['senha']


# Conecte-se à API da IQ Option
api = IQ_Option(email, password)
status, reason = api.connect()

if not status:
    print(f"Erro ao conectar: {reason}")
    exit()

print("Conexão bem-sucedida!")

# Configurações para o ativo e timeframe
ativo = "EURUSD"  # Substitua pelo ativo desejado
timeframe = 1     # Timeframe em minutos (exemplo: 1 para 1 minuto)
num_velas = 5     # Quantidade de velas a buscar

# Obtenha as velas
velas = api.get_candles(ativo, timeframe * 60, num_velas, time.time())

# Exiba as velas
for i, vela in enumerate(velas):
    open_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(vela['from']))
    print(f"Vela {i+1}:")
    print(f"  Início: {open_time}")
    print(f"  Abertura: {vela['open']}")
    print(f"  Fechamento: {vela['close']}")
    print(f"  Mínimo: {vela['min']}")
    print(f"  Máximo: {vela['max']}")
    print(f"  Volume: {vela['volume']}\n")