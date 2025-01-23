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
import config_inicial
from utils import dividir_em_grupos, cor_predominante, limpar_dados_resultado
from estrategias import get_catg_mhi_padrao, get_catg_mhi_reverso
import config_inicial

init(autoreset=True)
green = Fore.GREEN
yellow = Fore.YELLOW
red = Fore.RED
white = Fore.WHITE
greenf = Back.GREEN
yellowf = Back.YELLOW
redf = Back.RED
blue = Fore.BLUE

iqoption = login_iq_option()
pares_abertos = ativos_binarios(iqoption)
tamanho_grupo = 5

def inicia_catalogacao(funcao):
    if locals()['funcao'].__name__ == 'get_catg_mhi_padrao':
        print('\nEstratégia: MHI padrão')
    elif locals()['funcao'].__name__ == 'get_catg_mhi_reverso':
        print('\nEstratégia: MHI reverso')

    print(f"\n{'Ativo':<10} {'WINS':<7} {'LOSS':<7} {'Doji':<7} {'Percentual Win':<10}")
    limpar_dados_resultado(pares_abertos)
    for j, ativo in enumerate(pares_abertos['velas_ativas']):
        ativos_ordenados = funcao(ativo, j, pares_abertos)
        
    for resumo_ativo in ativos_ordenados:
        ativo_label = resumo_ativo['Ativo']
        print(f"{ativo_label:<10} {resumo_ativo['Win']:<7} {resumo_ativo['Loss']:<7} {resumo_ativo['Doji']:<7} {resumo_ativo['Taxa_Win']:<7}")
    resultado_operacao = []
inicia_catalogacao(get_catg_mhi_padrao)
resultado_operacao = []     
inicia_catalogacao(get_catg_mhi_reverso)