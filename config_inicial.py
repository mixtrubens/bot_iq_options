from login_iq import login_iq_option
from configobj import ConfigObj

class AutoExecuta:
    def __init__(self):
        self.executar()

    def executar(self):
        config = ConfigObj('config.txt')
        timeframe = config['AJUSTES']['timeframe']
        qnt_velas = config['AJUSTES']['quantidade_velas']
        pares_inativos = []
        resultado = []
        resultado_operacao = []
        resultado_operacao_parcial = []
        tamanho_grupo = 5