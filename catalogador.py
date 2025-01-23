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

    def inicia_catalogacao(self, estrategia):
        if estrategia.__name__ == 'mhi_padrao':
            print('\nEstratégia: MHI padrão')
        elif estrategia.__name__ == 'mhi_reverso':
            print('\nEstratégia: MHI reverso')

        print(f"\n{'#':<3} {'Ativo':<10} {'WINS':<7} {'LOSS':<7} {'Doji':<7} {'Percentual Win':<10}")
        self.utils.limpar_dados_resultado(self.pares_abertos)

        index = 1  # Inicializar o índice global
        for j, ativo in enumerate(self.pares_abertos['velas_ativas']):
            try:
                ativos_ordenados = estrategia(ativo, j, self.pares_abertos)
            except Exception as e:
                print(f"Erro ao processar {ativo}: {e}")
                continue

            # Ordenar por número de Wins e, em seguida, por % de Wins
            ativos_ordenados = sorted(
                ativos_ordenados,
                key=lambda x: (x['Win'], float(x['Taxa_Win'].strip('%'))),
                reverse=True
            )

            # Numerar os ativos ordenados e imprimir
            for resumo_ativo in ativos_ordenados:
                ativo_label = resumo_ativo['Ativo']
                print(
                    f"{index:<3} {ativo_label:<10} {resumo_ativo['Win']:<7} "
                    f"{resumo_ativo['Loss']:<7} {resumo_ativo['Doji']:<7} "
                    f"{resumo_ativo['Taxa_Win']:<10}"
                )
                index += 1  # Incrementar o índice global

    def menu_interativo(self):
        while True:
            print("\nEscolha a estratégia para catalogação:")
            print("1 - MHI padrão")
            print("2 - MHI inverso")
            print("3 - Todas")
            print("0 - Sair")

            opcao = input("Digite a opção desejada: ")

            if opcao == '1':
                self.inicia_catalogacao(self.estrategias.mhi_padrao)
            elif opcao == '2':
                self.inicia_catalogacao(self.estrategias.mhi_reverso)
            elif opcao == '3':
                self.inicia_catalogacao(self.estrategias.mhi_padrao)
                self.inicia_catalogacao(self.estrategias.mhi_reverso)
            elif opcao == '0':
                print("Encerrando o programa...")
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    catalogador = Catalogador()
    catalogador.menu_interativo()
