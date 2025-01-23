class Utils:
    def dividir_em_grupos(self, lista, tamanho_grupo):
        grupos = [
            lista[i:i + tamanho_grupo] 
            for i in range(0, len(lista), tamanho_grupo) 
            if len(lista[i:i + tamanho_grupo]) == tamanho_grupo
        ]
        return grupos

    def cor_predominante(self, pares_abertos):
        contagem = {'Vermelho': 0, 'Verde': 0}
        for item in pares_abertos:
            cor = item['cor']
            if cor in contagem:
                contagem[cor] += 1

        if contagem['Vermelho'] > contagem['Verde']:
            return 'Vermelho'
        elif contagem['Verde'] > contagem['Vermelho']:
            return 'Verde'
        return 'Doji'

    def limpar_dados_resultado(self, pares_abertos):
        for par in pares_abertos['velas_ativas']:
            par[next(iter(par))]['resultado_total'] = []
            par[next(iter(par))]['resultado_parcial'] = []
        return pares_abertos
