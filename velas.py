import threading
import datetime
from iqoptionapi.stable_api import IQ_Option
import locale
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
from datetime import datetime   
import pytz     
from datetime import datetime, timezone, timedelta
from configobj import ConfigObj
import time

config = ConfigObj('config.txt')
email = config['LOGIN']['email']
senha = config['LOGIN']['senha']
ativo =  config['AJUSTES']['pair']
timeframe = config['AJUSTES']['timeframe']
quantidade = config['AJUSTES']['quantidade_velas']
# Conexão à API
iq = IQ_Option(email, senha)
check, reason = iq.connect()

if not check:
    print(f"Erro ao conectar: {reason}")
    exit()

# Lista de ativos e configurações 
tempo = 1  # Período da vela em minutos (M1)
quantidade = 20  # Quantidade de velas para buscar

# Função para obter velas com timeout usando threading
class FunctionWithTimeout:
    def __init__(self, func, *args, **kwargs):
        self.result = None
        self.exception = None
        self.thread = threading.Thread(target=self.run, args=(func,) + args, kwargs=kwargs)
    
    def run(self, func, *args, **kwargs):
        try:
            self.result = func(*args, **kwargs)
        except Exception as e:
            self.exception = e

    def execute(self, timeout):
        self.thread.start()
        self.thread.join(timeout)
        if self.thread.is_alive():
            return None  # Timeout ocorreu
        if self.exception:
            raise self.exception  # Levanta qualquer exceção gerada pela função
        return self.result

def definir_cores_velas(vela):
    if vela['open'] < vela['close']:
        cor_vela = 'Verde'
    elif vela['open'] > vela['close']:
        cor_vela = 'Vermelho'
    else:
        cor_vela = 'Doji'
    return cor_vela

def ajustar_horario_catalogacao():
    # Obter a data e horário atuais
    data_horario = datetime.now()
    # fuso_horario = pytz.timezone('America/Sao_Paulo')
    # data_local = data_horario.astimezone(fuso_horario)
    # Obter o último dígito dos minutos
    ultimo_digito = data_horario.minute % 10

    # Substituir os minutos de acordo com as condições
    # data_horario = data_local.replace(minute=(data_horario.minute // 10) * 10) 
    if ultimo_digito in {0, 1, 2, 3, 4}:
        data_str = datetime.strftime(data_horario, '%Y-%m-%d %H:%M:%S')
        if data_horario.minute < 5:
            data_horario = data_horario.replace(minute=(data_horario.minute // 10) * 10)
        else:
            data_horario = data_horario.replace(minute=((data_horario.minute // 10) * 10) - 1 )
    elif ultimo_digito in {5, 6, 7, 8, 9}:
        data_str = datetime.strftime(data_horario, '%Y-%m-%d %H:%M:%S')
        data_horario = data_horario.replace(minute=((data_horario.minute // 10) * 10) + 4)
    data_horario = data_horario.replace(second=0)
    return data_horario


def get_velas(iq, ativo, timeframe, tempo):
    # Obtenha as velas
    timeframe = 1     # Timeframe em minutos (exemplo: 1 para 1 minuto)
    num_velas = 120    # Quantidade de velas a busca
    tempo_timestamp = tempo.timestamp()

    # Exiba as velas
    
    try:
        # Captura as velas de hoje (últimas 10)
        candles = iq.get_candles(ativo, timeframe * 60, num_velas, tempo_timestamp)
        # Formata os dados das velas
    except Exception as e:
        # print(f"Erro ao obter as velas: {e}")
        return None
    else:
        # open_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(candles['from']))
        formatted_candles = [
            {   "cor": definir_cores_velas(candle),
                "horario_candle": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(candle['from'])),
                "close": candle["close"]}
        for candle in candles
    ]
    
    return formatted_candles
def ativos_online(ativos):
# Processar cada ativo com timeout
    ativos_disponiveis = []
    ativos_disponiveis_anomalos = []
    
    list_tupla = list(ativos)
    tempo = ajustar_horario_catalogacao()

    for index, ativo in enumerate(ativos):
        velas_ativas = []
        # print(f"({index}/{len(ativos)}) Processando ativo: {ativo}")
        try:
            velas = get_velas(iq, ativo[0], timeframe, tempo)
            if velas is None:
                list_tupla.remove(ativo)
                continue
        except Exception as e:
            pass
            # print(f"Erro ao processar {ativo}\n")
        else:
            if velas[-1]['horario_candle'][0:13] == tempo.strftime('%Y-%m-%d %H:%M:%S')[0:13]:
                print(f">>> ({index}/{len(ativos)}) Ativo [{ativo}] processado com sucesso!")
                ativos_disponiveis.append({ativo[0] : {'payout': ativo[1],
                                                        'velas': velas,
                                                        'resultado_total': [],
                                                        'resultado_parcial': []}})
    return {'velas_ativas': ativos_disponiveis}


                 
    