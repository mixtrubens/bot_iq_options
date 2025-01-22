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

def login_iq_option():
    config = ConfigObj('config.txt')
    email = config['LOGIN']['email']
    password = config['LOGIN']['senha']

    print('Iniciando Conexão com a IQOption')
    API = IQ_Option(email, password)

    iqoption = IQ_Option(email, password)
    check, reason = iqoption.connect()
    if check:
        print("Conectado com sucesso!")
    else:
        print(f"Erro ao conectar: {reason}")
    return iqoption
