from utils import Utils

class Estrategias:
    def __init__(self):
        self.tamanho_grupo = 5
        self.utils = Utils()

    def estrategia_mhi(self, velas_agrupadas, cor_predominante_grupo, operacoes, doji, win, loss, i):
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

            resultado_operacao = {'operacao': sinal,
                                  'horario_resultado': velas_agrupadas[i][0]['horario_candle'],
                                  'sinal': velas_agrupadas[i+1][0]['cor']}
            return resultado_operacao, operacoes, doji, win, loss
        except IndexError:
            return None, operacoes, doji, win, loss

    def estrategia_mhi_reverso(self, velas_agrupadas, cor_predominante_grupo, operacoes, doji, win, loss, i):
        try:
            if velas_agrupadas[i+1][0]['cor'] == 'Doji' or cor_predominante_grupo == 'Doji': 
                doji += 1
                sinal = 'Doji'
            elif cor_predominante_grupo != velas_agrupadas[i+1][0]['cor']:
                operacoes += 1
                win += 1
                sinal = 'Win' 
            else:
                operacoes += 1
                loss += 1
                sinal = 'Loss'

            resultado_operacao = {'operacao': sinal,
                                  'horario_resultado': velas_agrupadas[i][0]['horario_candle'],
                                  'sinal': velas_agrupadas[i+1][0]['cor']}
            return resultado_operacao, operacoes, doji, win, loss
        except IndexError:
            return None, operacoes, doji, win, loss

    def mhi_padrao(self, ativo, j, pares_abertos):
        return self._processar_estrategia(ativo, j, pares_abertos, self.estrategia_mhi)

    def mhi_reverso(self, ativo, j, pares_abertos):
        return self._processar_estrategia(ativo, j, pares_abertos, self.estrategia_mhi_reverso)

    def _processar_estrategia(self, ativo, j, pares_abertos, estrategia_func):
        win = 0
        loss = 0
        doji = 0
        operacoes = 0
        resultado_operacao_parcial = []
        resultado_operacao = []

        key = list(ativo.keys())[0]
        velas_ativo = ativo[key]['velas']
        velas_agrupadas = self.utils.dividir_em_grupos(velas_ativo, self.tamanho_grupo)

        for i, velas in enumerate(velas_agrupadas):
            cor_predominante_grupo = self.utils.cor_predominante(velas_agrupadas[i])
            resultado, operacoes, doji, win, loss = estrategia_func(
                velas_agrupadas, cor_predominante_grupo, operacoes, doji, win, loss, i
            )
            if resultado:
                resultado_operacao.append(resultado)

        if operacoes != 0:
            ativo[key]['resultado_total'].append(resultado_operacao)
            resultado_operacao_parcial.append({
                'Ativo': key,
                'Win': win,
                'Loss': loss,
                'Doji': doji,
                'Taxa_Win': f"{win * 100 / operacoes:.2f}%"
            })
            pares_abertos['velas_ativas'][j][key]['resultado_parcial'].append(resultado_operacao_parcial[0])

        return sorted(resultado_operacao_parcial, key=lambda x: x['Win'], reverse=True)
