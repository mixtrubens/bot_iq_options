from estrategias import Estrategias
from utils import Utils
from login_iq import login_iq_option
from ativos_validos import ativos_binarios
from colorama import Fore, Back, init

class Catalogador:
    def __init__(self):
        self.iqoption = login_iq_option()
        self.pares_abertos = ativos_binarios(self.iqoption)
        self.utils = Utils()
        self.estrategias = Estrategias()
        self.tamanho_grupo = 5

    def inicia_catalogacao(self, estrategia, qnt_martingale):
        if estrategia.__name__ == 'mhi_padrao':
            print('\nEstratégia: MHI padrão')
        elif estrategia.__name__ == 'mhi_reverso':
            print('\nEstratégia: MHI reverso')

        print(f"\n{'#':<3} {'Ativo':<10} {'WINS':<7} {'LOSS':<7} {'Doji':<7} {'Percentual Win':<10}")
        self.utils.limpar_dados_resultado(self.pares_abertos)
        ativos_ordenados_lista = []
        dados = []
        index = 1  # Inicializar o índice global
        for j, ativo in enumerate(self.pares_abertos['velas_ativas']):
            try:
                ativos_catalogados = estrategia(ativo, j, self.pares_abertos, qnt_martingale)
            except Exception as e:
                # print(f"Erro ao processar {ativo}: {e}")
                continue
            if ativos_catalogados != []:
                win_loss = int(ativos_catalogados[0]['Win']) +  int(ativos_catalogados[0]['Loss'])
                if int(ativos_catalogados[0]['Doji'] < win_loss):
                    dados.append(ativos_catalogados)
                    # Ordenar por número de Wins e, em seguida, por % de Wins
            dados_ordenados = sorted(
                dados,
                key=lambda x: (float(x[0]['Taxa_Win'].strip('%')), x[0]['Win']),
                reverse=True
            )
            # Numerar os ativos ordenados e imprimir
        for resumo_ativo in dados_ordenados:
            ativo_label = resumo_ativo[0]['Ativo']
            print(
                f"{index:<3} {ativo_label:<10} {resumo_ativo[0]['Win']:<7} "
                f"{resumo_ativo[0]['Loss']:<7} {resumo_ativo[0]['Doji']:<7} "
                f"{resumo_ativo[0]['Taxa_Win']:<10}"
            )
            index += 1  # Incrementar o índice global
        return ativos_ordenados_lista


    def menu_interativo(self):
        while True:
            print("\nEscolha a estratégia para catalogação:")
            print("1 - MHI padrão")
            print("2 - MHI inverso")
            print("3 - Todas")
            print("0 - Sair")

            opcao = input("Digite a opção desejada: ")
            self.qnt_martingale = input("Digite a quantidade de martingales: ")
            if opcao == '1':
                resultado = self.inicia_catalogacao(self.estrategias.mhi_padrao, self.qnt_martingale)
            elif opcao == '2':
                self.inicia_catalogacao(self.estrategias.mhi_reverso, self.qnt_martingale)
            elif opcao == '3':
                self.inicia_catalogacao(self.estrategias.mhi_padrao, self.qnt_martingale)
                self.inicia_catalogacao(self.estrategias.mhi_reverso, self.qnt_martingale)
            elif opcao == '0':
                print("Encerrando o programa...")
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    catalogador = Catalogador()
    catalogador.menu_interativo()
