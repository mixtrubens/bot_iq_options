from utils import dividir_em_grupos, cor_predominante
tamanho_grupo = 5
resultado_operacao_parcial = []
def get_catg_mhi_padrao(ativo, j):
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
    return ativos_ordenados