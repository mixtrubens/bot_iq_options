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

def limpar_dados_resultado(pares_abertos):
    for par in pares_abertos['velas_ativas']:
        par[next(iter(par))]['resultado_total'] = []
        par[next(iter(par))]['resultado_parcial'] = []
    return pares_abertos
