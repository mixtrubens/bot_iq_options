from iqoptionapi.stable_api import IQ_Option
import time
from configobj import ConfigObj
import sys
from tabulate import tabulate
from ativos_validos import ativos_binarios
from login_iq import login_iq_option
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
from ativos_validos import ativos_binarios

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

config = ConfigObj('config.txt')
iqoption = login_iq_option()
pares_abertos = ativos_binarios(iqoption)
timeframe = config['AJUSTES']['timeframe']
qnt_velas = config['AJUSTES']['quantidade_velas']
pares_inativos = []
resultado = []
resultado_operacao = []
resultado_operacao_parcial = []
tamanho_grupo = 5

def obter_velas(par):
    velas = iqoption.get_candles(par[0], timeframe, qnt_velas, time.time())
    return velas

def dividir_em_grupos(lista, tamanho_grupo):
    grupos = [
        lista[i:i + tamanho_grupo] 
        for i in range(0, len(lista), tamanho_grupo) 
        if len(lista[i:i + tamanho_grupo]) == tamanho_grupo
    ]
    return grupos

def cor_predominante(pares_abertos):
    # Contar as ocorrências de cada cor
    contagem = {'Vermelho': 0, 'Verde': 0}

    for item in pares_abertos:
        cor = item['cor']
        if cor in contagem:
            contagem[cor] += 1

    # Determinar o resultado com base na predominância
    if contagem['Vermelho'] > contagem['Verde']:
        resultado = 'Vermelho'
    elif contagem['Verde'] > contagem['Vermelho']:
        resultado = 'Verde'
    else:
        resultado = 'Doji'  # Caso as quantidades de Verde e Vermelho sejam iguais
    return resultado

print(f"\n{'Ativo':<10} {'WINS':<7} {'LOSS':<7} {'Doji':<7} {'Percentual Win':<10}")
for j, ativo in enumerate(pares_abertos['velas_ativas']):
    resultado_operacao = []
    win = 0
    loss = 0
    doji = 0
    operacoes = 0
    key = list(ativo.keys())[0]
    velas_ativo = (ativo[key]['velas']) 
    partes = 5
    velas_agrupadas = dividir_em_grupos(velas_ativo, tamanho_grupo)
    for i, velas in enumerate(velas_agrupadas):
        cor_predominante_grupo = cor_predominante(velas_agrupadas[i])
        try:
            if velas_agrupadas[i+1][0]['cor'] == 'Doji' or cor_predominante_grupo == 'Doji': 
                doji += 1
                sinal = 'Doji'
            elif cor_predominante_grupo == velas_agrupadas[i+1][0]['cor']:
                operacoes += 1
                win += 1
                sinal = 'Win' 
            else:
                operacoes += 1
                loss += 1
                sinal = 'Loss'

            resultado_operacao.append({'operacao': {sinal},
                                       'horario_resultado': velas_agrupadas[i][0]['horario_candle'],
                                       'sinal': velas_agrupadas[i+1][0]['cor']
                                        })
        except IndexError:
            break
    ativo[key]['resultado_total'].append(resultado_operacao)
    
    resultado_operacao_parcial.append({'Ativo': next(iter(ativo)),
                                       'Win': win,
                                       'Loss': loss,
                                       'Doji': doji,
                                       'Taxa_Win': f"{win * 100 / operacoes:.2f}%"})

    pares_abertos['velas_ativas'][j][key]['resultado_parcial'].append({'Ativo': next(iter(ativo)),
                                       'Win': win,
                                       'Loss': loss,
                                       'Doji': doji,
                                       'Taxa_Win': f"{win * 100 / operacoes:.2f}%"})

    ativos_ordenados = sorted(resultado_operacao_parcial, key=lambda x: x['Win'], reverse=True)

for resumo_ativo in ativos_ordenados:
    ativo_label = resumo_ativo['Ativo']
    print(f"{ativo_label:<10} {resumo_ativo['Win']:<7} {resumo_ativo['Loss']:<7} {resumo_ativo['Doji']:<7} {resumo_ativo['Win'] * 100 / operacoes:.2f}%")
    
print('\n>> Iniciando catalogacao análise da estratégia MHI')

tuplas = pares_abertos['tupla']
pares_abertos
