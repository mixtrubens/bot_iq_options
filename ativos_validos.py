
from velas import ativos_online

def ativos_binarios(iq):
    # Obter payouts
    payouts = iq.get_all_profit()

    # Filtrar apenas ativos binários com payout acima de 82% e retira labels que terminam com -op
    ativos_binarios_payout_alto = []
    for ativo, valores in payouts.items():
        if isinstance(valores, dict) and 'binary' in valores:  # Verifica a chave 'binary'
            payout_binary = valores['binary']
            if isinstance(payout_binary, (float, int)) and payout_binary * 100 > 82:
                if ativo[-3:] != '-op':
                    ativos_binarios_payout_alto.append((ativo, payout_binary * 100))

    #filtra os ativos que realmente estao disponiveis e monta o dicionario
    ativos_binarios_payout_alto_validos = ativos_online(ativos_binarios_payout_alto)
    return ativos_binarios_payout_alto_validos

def ativos_binarios_padrao(iq):
    # Obter payouts
    payouts = iq.get_all_profit()
    open_time = iq.get_all_open_time()
    ativos_abertos = []
    labels_ativos = []

    # Iterar apenas sobre os ativos da categoria "binary"
    for ativo, dados in open_time["binary"].items():
        if ativo[-3:] =='-op':
            if dados["open"]:  # Verifica se o ativo está aberto
                labels_ativos.append(ativo[:-3])

    print("Ativos binários abertos:", ativos_abertos)

    # Filtrar apenas ativos binários com payout acima de 82% e retira labels que terminam com -op
    ativos_binarios_payout_alto = []
    for ativo, valores in payouts.items():
        if ativo in labels_ativos:
            if isinstance(valores, dict) and 'binary' in valores:  # Verifica a chave 'binary'
                payout_binary = valores['binary']
                if isinstance(payout_binary, (float, int)) and payout_binary * 100 > 82:
                    if ativo[-3:] != '-op':
                        ativos_binarios_payout_alto.append((ativo, payout_binary * 100))

    #filtra os ativos que realmente estao disponiveis e monta o dicionario
    ativos_binarios_payout_alto_validos = ativos_online(ativos_binarios_payout_alto)
    return ativos_binarios_payout_alto_validos