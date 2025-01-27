from utils import Utils

class Estrategias:
    def __init__(self):
        self.tamanho_grupo = 5
        self.utils = Utils()

    def estrategia_mhi(self, velas_agrupadas, cor_predominante_grupo, operacoes, doji, win, loss, i, martingale):
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
            return resultado_operacao, operacoes, doji, win, loss, martingale
        except IndexError:
            pass
    def estrategia_mhi_reverso(self, velas_agrupadas, cor_predominante_grupo, operacoes, doji, win, loss, i, martingale):
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
            return None

    def mhi_padrao(self, ativo, j, pares_abertos):
        return self._processar_estrategia(ativo, j, pares_abertos, self.estrategia_mhi)

    def mhi_reverso(self, ativo, j, pares_abertos):
        return self._processar_estrategia(ativo, j, pares_abertos, self.estrategia_mhi_reverso)

    def _processar_estrategia(self, ativo, j, pares_abertos, estrategia_func):
        win = 0
        loss = 0
        doji = 0
        operacoes = 0
        martingale = 0
        resultado_operacao_parcial = []
        resultado_operacao = []

        key = list(ativo.keys())[0]
        velas_ativo = ativo[key]['velas']
        velas_agrupadas = self.utils.dividir_em_grupos(velas_ativo, self.tamanho_grupo)

        for i, velas in enumerate(velas_agrupadas):
            if i == len(velas_agrupadas) -1:
                break
            cor_predominante_grupo = self.utils.cor_predominante(velas_agrupadas[i])
            resultado, operacoes, doji, win, loss , martingale = estrategia_func(
                velas_agrupadas, cor_predominante_grupo, operacoes, doji, win, loss, i, martingale
            )
            if resultado:
                if resultado['operacao'] == 'Loss':
                    martingale += 1
                resultado['martingale'] = str(martingale)

                if resultado['operacao'] == 'Win':
                    loss = loss - (martingale - 1)
                    resultado_operacao.append(resultado)
                    martingale = 0
                elif int(martingale) == 3:
                   martingale = 0
                   resultado_operacao.append(resultado)
                else:
                   continue


        if operacoes != 0:
            ativo[key]['resultado_total'].append(resultado_operacao)
            resultado_operacao_parcial.append({
                'Ativo': key,
                'Win': win,
                'Loss': sum(1 for item in resultado_operacao if item['operacao'] == 'Loss'),
                'Doji': doji,
                'Taxa_Win': f"{win * 100 / len(ativo[key]['resultado_total'][0]):.2f}%"
            })
            pares_abertos['velas_ativas'][j][key]['resultado_parcial'].append(resultado_operacao_parcial[0])

        return sorted(resultado_operacao_parcial, key=lambda x: x['Win'], reverse=True)
