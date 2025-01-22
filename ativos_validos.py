
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