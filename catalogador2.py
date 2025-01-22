
from iqoptionapi.stable_api import IQ_Option
import time
from configobj import ConfigObj
import sys
from datetime import datetime
from tabulate import tabulate
from iqoptionapi.constants import ACTIVES
from collections import Counter


def catag(API):

    ### CRIANDO ARQUIVO DE CONFIGURAÇÃO ####
    config = ConfigObj('config.txt')
    

    pares_abertos = []

    all_asset = API.get_all_open_time()

    
    # for par in all_asset['turbo']:
    #     if par in ACTIVES:
    #         if all_asset['turbo'][par]['open']:
    #             if par not in pares_abertos:
    #                 turbo = payout(par, API)
    #                 if turbo > 80.0:
    #                     pares_abertos.append(par)
            
            
    timeframe = 60
    # qnt_velas  = 1440 
    qnt_velas  = 100000

    global resultado
    resultado = []

    def mhi():
        global resultado
    gale = 0
    if pares_abertos:
        for par in pares_abertos:
            array_velas = []
            catalogo = []
            pontos_entrada = []
            velas = API.get_candles(par, timeframe,qnt_velas, time.time())
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
            max_verde = max(contar_verde(s) for s in array_velas)
            max_vermelho = max(contar_verde(s) for s in array_velas)
            print(par)
            print(max_verde)
            print(max_vermelho)

# Inicializa variáveis para rastrear a sequência atual e a sequência mais longa
            max_sequencia = 0
            sequencia_atual = 1

            # Percorre o vetor
            for indice, candle_sequencia in  enumerate(array_velas):
                if indice !=0:
                    if array_velas[indice-1] == array_velas[indice]:
                        sequencia_atual += 1
                        # Atualiza o comprimento da sequência mais longa se a atual for maior
                        if sequencia_atual > max_sequencia:
                            max_sequencia = max(max_sequencia, sequencia_atual)
                            h = datetime.fromtimestamp(velas[indice]['from']).strftime('%H:%M')
                        if sequencia_atual == 10:
                            h2= datetime.fromtimestamp(velas[indice]['from']).strftime('%H:%M')  
                            pontos_entrada.append(h2) 
                    else:
                        # Reseta a contagem da sequência atual se encontrar uma palavra diferente
                        sequencia_atual = 0
            

            print("Maior sequencia: " + par + " - " + str(max_sequencia) + " - "+ h)
            print(h)
            print('Fim')
    def mhi_reverso():
        global resultado
    gale = 0
    if pares_abertos:
        for par in pares_abertos:
        #      profit = API.get_all_profit()
        #      all_asset = API.get_all_open_time()
        # try:
        #     if all_asset['turbo'][par]['open']:
        #         if profit[par]['turbo']> 0:
        #             turbo = round(profit[par]['turbo'],2) * 100
        #     else:
        #         turbo  = 0
        # except:
        #     turbo = 0
            # turbo = payout(par, API)
            catalogo = []
            velas = API.get_candles(par, timeframe,qnt_velas, time.time())
            for i in range(len(velas)):
                minutos = float(datetime.fromtimestamp(velas[i]['from']).strftime('%M')[1:])    
                array_velas = []
              
                if minutos == 5 or minutos == 0:
                    try:
                        if i <2:
                            pass
                        else:

                            for j in range(5):
                                if velas[i+j]['open'] < velas[i+j]['close']:
                                    array_velas.append('Verde')
                                elif velas[i+j]['open'] > velas[i+j]['close']:
                                    array_velas.append('Vermelho')
                                else:
                                    array_velas.append('Doji')
                            contagem = Counter(array_velas)
                            velaSignal = contagem.most_common(1)[0][0]
                            # Sinal
                            if velaSignal == 'Verde':
                                entrada = 'Verde'
                            elif velaSignal == 'Vermelho':
                                entrada = 'Vermelho'
                            else:
                                entrada = 'Doji'
                            # Resultado da vela
                            if velas[i+5]['open'] < velas[i+5]['close']:
                                vela_result = 'Verde'
                            elif velas[i+5]['open'] > velas[i+5]['close']:
                                vela_result = 'Vermelho'
                            else:
                                vela_result = 'Doji'
                            # Resultado Win/Lose/Marginale
                            if vela_result == entrada and vela_result != 'Doji':
                                result = 'WIN' + str(gale)
                                i = i+ 5
                                catalogo.append({'WIN': datetime.fromtimestamp(velas[i]['from']).strftime("%Y-%m-%d %H:%M:%S"), 'GALE': gale})
                                gale  = 0
                            elif vela_result != entrada:
                                gale = gale + 1
                                i = i+ 5
                                if gale > 3:
                                    catalogo.append({'LOSS': datetime.fromtimestamp(velas[i]['from']).strftime("%Y-%m-%d %H:%M:%S")})
                                    gale = 0
                                continue
                    except:
                        pass

            contagem_win = sum(map(lambda d: 'WIN' in d, catalogo))
            # Total de dicionários na lista
            total_dicionarios = len(catalogo)
            # Calcula a porcentagem de 'WIN'
            taxa_win = round(contagem_win/(total_dicionarios)*100,2)
            

            resultado.append(['MHI'] + [par]+ [taxa_win]  + [catalogo])
    print('Fim')

    resultado_mhi_reverso = mhi_reverso()
    resultado_mhi = mhi()

    return  resultado_mhi

def payout(par, API):
    profit = API.get_all_profit()
    all_asset = API.get_all_open_time()
    try:
        if all_asset['turbo'][par]['open']:
            if profit[par]['turbo']> 0:
                turbo = round(profit[par]['turbo'],2) * 100
        else:
            turbo  = 0
    except:
        turbo = 0


    return turbo


def contar_verde(s):
    return s.split(',').count('Verde')
def contar_vermelho(s):
    return s.split(',').count('Vermelho')