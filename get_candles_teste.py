from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import pytz
import time

# Configuração de login
email = "rubinho132@hotmail.com"  # Insira seu email de login
senha = "Ax206487"  # Insira sua senha

# # Conectando à IQ Option
# iq = IQ_Option(email, senha)
# check, reason = iq.connect()

# if not check:
#     print(f"Erro ao conectar: {reason}")
#     exit()

# print("Conexão bem-sucedida!")

# # Configuração do ativo e parâmetros
# ativo = "EURUSD"
# timeframe = 1  # Timeframe das velas em minutos
# quantidade_velas = 10  # Quantidade de velas para buscar
# fuso_horario = pytz.timezone('America/Sao_Paulo')

# def obter_velas(iq, ativo, timeframe, quantidade):
#     """Obtém as últimas velas do ativo especificado."""
#     horario_atual = int(time.time())  # Timestamp atual
#     try:
#         velas = iq.get_candles(ativo, timeframe * 60, quantidade, 1738073220)
#         velas_formatadas = [
#             {
#                 "horario": datetime.fromtimestamp(vela['from'], fuso_horario).strftime('%Y-%m-%d %H:%M:%S'),
#                 "open": vela['open'],
#                 "close": vela['close'],
#                 "high": vela['max'],
#                 "low": vela['min'],
#                 "volume": vela['volume'],
#                 "from": vela['from']
#             }
#             for vela in velas
#         ]
#         return velas_formatadas
#     except Exception as e:
#         print(f"Erro ao obter velas: {e}")
#         return None

# # Obter as velas
# velas = obter_velas(iq, ativo, timeframe, quantidade_velas)

# if velas:
#     print("\nÚltimas velas do ativo EURUSD:")
#     for i, vela in enumerate(velas):
#         print(f"Vela {i + 1}: {vela}")
# else:
#     print("Não foi possível obter as velas.")




# Conexão com a IQ Option
iq = IQ_Option(email, senha)
check, reason = iq.connect()

if not check:
    print(f"Erro ao conectar: {reason}")
    exit()

print("Conexão bem-sucedida!")

# Configuração do ativo e parâmetros
ativo = "EURUSD"
timeframe = 1  # Timeframe das velas em minutos
quantidade_velas = 10  # Quantidade de velas para buscar

def obter_velas(iq, ativo, timeframe, quantidade):
    """Obtém as últimas velas do ativo especificado e valida os dados."""
    horario_atual = int(time.time())  # Timestamp atual
    try:
        velas = iq.get_candles(ativo, timeframe * 60, quantidade, time.time() - 60)
        velas_formatadas = [
            {
                "horario": datetime.fromtimestamp(vela['from']).strftime('%Y-%m-%d %H:%M:%S'),
                "open": vela['open'],
                "close": vela['close'],
                "high": vela['max'],
                "low": vela['min'],
                "volume": vela['volume']
            }
            for vela in velas
        ]
        return velas_formatadas
    except Exception as e:
        print(f"Erro ao obter velas: {e}")
        return None

# Obter as velas
velas = obter_velas(iq, ativo, timeframe, quantidade_velas)     

if velas:
    print("\nÚltimas velas do ativo EURUSD:")
    for i, vela in enumerate(velas):
        print(f"Vela {i + 1}: {vela}")
else:
    print("Não foi possível obter as velas.")

# Validando os resultados
print("\nValidando os dados obtidos:")
for i, vela in enumerate(velas):
    print(f"Vela {i + 1}:")
    print(f"  Horário: {vela['horario']}")
    print(f"  Abertura: {vela['open']}")
    print(f"  Fechamento: {vela['close']}")
    print(f"  Máxima: {vela['high']}")
    print(f"  Mínima: {vela['low']}")
    print(f"  Volume: {vela['volume']}")