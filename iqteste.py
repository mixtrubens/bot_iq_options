
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta

def get_10_candles_today(username, password):
    try:
        # Conecta na conta da IQ Option
        iq = IQ_Option(username, password)
        check, reason = iq.connect()
        
        if not check:
            print(f"Erro ao conectar: {reason}")
            return None

        # Define o par de moedas e o período de 1 minuto para as velas
        pair = "EURUSD"
        timeframe = 60  # 60 segundos = 1 minuto

        # Define o horário de início e final (meia-noite de hoje)
        now = datetime.now()
        midnight = datetime(now.year, now.month, now.day)

        # Captura as velas de hoje (últimas 10)
        candles = iq.get_candles(pair, timeframe, 10, now.timestamp())

        # Formata os dados das velas
        formatted_candles = [
            {
                "from": datetime.fromtimestamp(candle["from"]),
                "open": candle["open"],
                "close": candle["close"],
                "min": candle["min"],
                "max": candle["max"],
                "volume": candle["volume"]
            }
            for candle in candles
        ]

        return formatted_candles

    except Exception as e:
        print(f"Erro ao obter as velas: {e}")
        return None

# Exemplo de uso:
config = ConfigObj('config.txt')
email = config['LOGIN']['email']
senha = config['LOGIN']['senha']
candles = get_10_candles_today(username, password)

if candles:
    for idx, candle in enumerate(candles, start=1):
        print(f"Vela {idx}: {candle}")
