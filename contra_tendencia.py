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
from colorama import Fore, Style, init


init()

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


def select_color(color, i, array_velas):
    if color == "Vermelho":
        if i == len(array_velas) - 1:
            color = f"{red}{color}"
        else:
            color = f"{red}{color}{white}, "
    elif color == "Verde":
        if i == len(array_velas) - 1:
            color = f"{green}{color}"
        else:
            color = f"{green}{color}{white}, "
    return color

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
        print('\n**************************        OPERACAO INICIADA        **************************\n')
        print(f"Compra realizada: {direction} com {amount} em {symbol} por {duration} minutos")
    else:
        print("Erro ao realizar a compra")
    return order_id
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
qnt_velas  = 4 # Quantidade de velas que ira ser usado na base
martingale = -1
iqoption = login_iq_option(email, password)
teste = False
em_compra = False
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
    array_velas.pop()
    cor, contagem = maior_sequencia(array_velas)
    hora = datetime.fromtimestamp(iqoption.get_server_timestamp()).strftime('%H:%M:%S')
    k = ""
    if hora.split(':')[2] == '10':
        print(yellow + '***************************************************************************************\n')
        print(f"{white}Horario: {hora}")
        if em_compra:
            print(f"{white}Status:{green} Em Operação")
            print(f"{white}Martingale atual: {blue}{martingale}")
            time.sleep(1)
        elif not em_compra:
            print(f"{white}Status:{yellow} Analisando Operação")
            print(f"{white}Sequencia atual: {blue}{contagem}")
            time.sleep(1)
        for x, i in enumerate(array_velas):
            color = select_color(i, x, array_velas)
            k += color
        
        print(f"{white}Array Velas: {k}")
        print(yellow + '***************************************************************************************\n')
        time.sleep(1)
    if em_compra:
        if array_velas[-1] != array_velas[-2]:
           print(green + '######################## WIN ########################')
           martingale = -1
           em_compra = False     
           time.sleep(5)
        
            
    sequencia_valida = True if array_velas[-1] == array_velas[-2] else False
    # Inicializa variáveis para rastrear a sequência atual e a sequência mais longa
    if contagem > 1 and contagem < 3 and sequencia_valida and martingale <3:
        array_velas[-1] != array_velas[-2]
        if iqoption:
            if cor == 'Vermelho':
                    action = 'call'
            elif cor == 'Verde': 
                action = 'put'
            segundos = datetime.fromtimestamp(iqoption.get_server_timestamp()).strftime('%S')
            if int(segundos) <= 1:
                make_trade(iqoption, ativo, amount, action, 1)
                martingale = martingale + 1
                em_compra = True
                time.sleep(5)
    elif martingale > 3:
        print(red + '######################## LOSS ########################')
        print(datetime.fromtimestamp(iqoption.get_server_timestamp()).strftime('%H:%M:%S'))
        print(array_velas)
        martingale = -1 
        time.sleep(600)


