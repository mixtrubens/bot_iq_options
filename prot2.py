from iqoptionapi.stable_api import IQ_Option
import time
from configobj import ConfigObj
import json, sys
from datetime import datetime, timedelta
from tabulate import tabulate
from colorama import init, Fore, Back
from iqoptionapi.constants import ACTIVES
from collections import Counter
from itertools import groupby

init(autoreset=True)
green = Fore.GREEN
yellow = Fore.YELLOW
red = Fore.RED
white = Fore.WHITE
greenf = Back.GREEN
yellowf = Back.YELLOW
redf = Back.RED
blue = Fore.BLUE


email = "rubinho132@hotmail.com"
password = "Ax206487"

def login_iq_option(email, password):
    email = "rubinho132@hotmail.com"
    password = "Ax206487"
    iqoption = IQ_Option(email, password)
    check, reason = iqoption.connect()
    if check:
        print("Conectado com sucesso!")
    else:
        print(f"Erro ao conectar: {reason}")
    return iqoption

iqoption = login_iq_option(email, password)

def maior_sequencia(candles):
    # Use groupby para agrupar elementos consecutivos iguais
    grouped = [(key, sum(1 for _ in group)) for key, group in groupby(candles)]
    
    # Encontre o grupo com a maior sequência
    max_key, max_count = max(grouped, key=lambda x: x[1])
    
    return max_key, max_count

def get_last_candles(iqoption, symbol, interval, count, time_adjustment):
    current_time = time.time() + time_adjustment
    candle = iqoption.get_candles(symbol, interval, count, current_time)
    return candle[0]



def make_trade(iqoption, symbol, amount, action, duration):
    if action == 'verde':
        direction = 'call'
    else:
        direction = 'put'
    
    check, order_id = iqoption.buy(amount, symbol, direction, duration)
    if check:
        print(f"Compra realizada: {direction} com {amount} em {symbol} por {duration} minutos")
    else:
        print("Erro ao realizar a compra")

def analyze_candles(candle):

    open_price = candle['open']
    close_price = candle['close']
    if close_price > open_price:
        color = 'Verde'
    else:
        color ='Vermelho'
    return color


print(yellow + '***************************************************************************************\n\n')
print(yellow+'Iniciando Conexão com a IQOption')

### Função para Selecionar demo ou real ###
while True:
    escolha = input(green+'\n>>'+ white +' Selecione a conta em que deseja conectar:\n'+
                            green+'>>'+ white +' 1 - Demo\n'+
                            green+'>>'+ white +' 2 - Real\n'+
                            green+'-->'+ white +' ')
    
    escolha =  int(escolha)

    if escolha == 1:
        conta = 'PRACTICE'
        print('Conta demo selecionada')
        break
    if escolha == 2:
        conta = 'REAL'
        print('Conta real selecionada')
        break
    else:
        print(red+'Escolha incorreta! Digite demo ou real')
        
def horario():
    x = iqoption.get_server_timestamp()
    now = datetime.fromtimestamp(iqoption.get_server_timestamp())
    
    return now


perfil = json.loads(json.dumps(iqoption.get_profile_ansyc()))
cifrao = str(perfil['currency_char'])
nome = str(perfil['name'])

valorconta = float(iqoption.get_balance())
valor_entrada = 10
stop_win = 100
stop_loss = 100
print(yellow+'\n######################################################################')
print('\nOlá, ',nome, '\nSeja bem vindo ao Robô do Canal do Lucas.')
print('\nSeu Saldo na conta ',escolha, 'é de', cifrao,valorconta)
print('\nSeu valor de entrada é de ',cifrao,valor_entrada)
print('\nStop win:',cifrao,stop_win)
print('\nStop loss:',cifrao,'-',stop_loss)
print(yellow+'\n######################################################################\n\n')

print('>> Iniciando Operacoes')

ativo = input(green+ '\n>>'+white+' Digite o ativo que você deseja operar: ').upper()
timeframe = 60
qnt_velas  = 3

iqoption = login_iq_option(email, password)
teste = False

while True:

    array_velas = []
    catalogo = []
    pontos_entrada = []
    amount = 10
    
    velas = iqoption.get_candles(ativo, timeframe,qnt_velas, time.time() + 130)
    for i in range(len(velas)):
            minutos = float(datetime.fromtimestamp(velas[i]['from']).strftime('%M')[1:])    
            if velas[i]['open'] < velas[i]['close']:
                array_velas.append('Verde')
                vela = 'Verde'
            elif velas[i]['open'] > velas[i]['close']:
                vela = 'Vermelho'
                array_velas.append('Vermelho')
            else:
                array_velas.append('Doji')

    cor, contagem = maior_sequencia(array_velas)
    for vela, i in enumerate(array_velas):
        if vela == vela[i+1]:
            sequencia_valida = True if array_velas[-1] == array_velas[-2] else False
    # Inicializa variáveis para rastrear a sequência atual e a sequência mais longa
    if contagem > 1 and contagem < 10 and sequencia_valida and martingale <3:
        array_velas[-1] != array_velas[-2]
        if iqoption:
            if cor == 'Vermelho':
                    action = 'call'
            elif cor == 'Verde':
                action = 'put'
            segundos = datetime.fromtimestamp(iqoption.get_server_timestamp()).strftime('%S')
            print(segundos)
            if int(segundos) < 1:
                make_trade(iqoption, ativo, amount, action, 1)
                martingale = martingale + 1
                print(green + '************************************************************************************')
                print('OPERACAO INICIADA \n')
                print(f"{white}Martingale:{blue}{str(martingale + 1)}")
                print(array_velas)
                print(datetime.fromtimestamp(iqoption.get_server_timestamp()).strftime('%H:%M:%S'))
                print(green + '***************************************************************************************\n\n')
                time.sleep(30)
    elif martingale > 2:
        print('LOSS')
        print(datetime.fromtimestamp(iqoption.get_server_timestamp()).strftime('%H:%M:%S'))
        print(array_velas)
        time.sleep(600)


# import requests
# import pandas as pd
# from datetime import datetime

# def get_last_minute_candle(symbol):
#     base_url = "https://api.binance.com"
#     endpoint = "/api/v3/klines"
#     params = {
#         'symbol': symbol,
#         'interval': '1m',
#         'limit': 1
#     }

#     response = requests.get(base_url + endpoint, params=params)
    
#     if response.status_code == 200:
#         data = response.json()
#         # Formatando o dado recebido
#         columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
#         df = pd.DataFrame(data, columns=columns)
#         df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
#         df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
        
#         # Convertendo valores para o tipo adequado
#         for col in ['open', 'high', 'low', 'close', 'volume']:
#             df[col] = df[col].astype(float)
        
#         # Pegando o último candle
#         last_candle = df.iloc[-1]
        
#         return last_candle
#     else:
#         print(f"Erro na requisição: {response.status_code}")
#         return None

# # Exemplo de uso
# symbol = 'BTCUSDT'
# last_candle = get_last_minute_candle(symbol)
# if last_candle is not None:
#     print(last_candle)    print(yellow + '***************************************************************************************')
