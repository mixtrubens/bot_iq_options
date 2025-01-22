
from datetime import datetime
from iqoptionapi.stable_api import IQ_Option
import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
# Credenciais da IQ Option
email = "rubinho132@hotmail.com"
password = "Ax206487"
iqoption = IQ_Option(email, password)
check, reason = iqoption.connect()


if not check:
    print(f"Erro ao conectar: {reason}")
    exit()

# Configurações iniciais
paridade = "EURUSD-OTC"
tipo = "binary"  # ou "digital"
valor_investimento = 1  # valor em dólares
direcao = None
wins = 0

# Função para obter as últimas 500 velas
def obter_velas(paridade, num_velas):
    velas = iqoption.get_candles(paridade, 100, num_velas, time.time() + 125)
    df = pd.DataFrame(velas)
    df['datetime'] = pd.to_datetime(df['from'], unit='s')
    df['open_close_diff'] = df['open'] - df['close']
    df['high_low_diff'] = df['max'] - df['min']
    df['target'] = df['close'].shift(-1) > df['close']
    df['target'] = df['target'].astype(int)
    return df[:-1]  # Remover a última linha, pois não há próxima vela para comparar

# Função para prever a próxima vela
def prever_proxima_vela(model, df):
    X_new = df[['open_close_diff', 'high_low_diff']].tail(1)
    prediction = model.predict(X_new)
    return "call" if prediction[0] == 1 else "put"

# Função para treinar o modelo com Grid Search
def treinar_modelo_com_ajustes(df):
    X = df[['open_close_diff', 'high_low_diff']]
    y = df['target']

    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Definir o modelo e os parâmetros para Grid Search
    model = LogisticRegression()
    parametros = {
        'C': [0.01, 0.1, 1, 10, 100],
        'max_iter': [100, 200, 300, 400, 500],
        'solver': ['lbfgs', 'liblinear']
    }

    # Usar Grid Search para encontrar os melhores parâmetros
    grid_search = GridSearchCV(model, parametros, cv=5)
    grid_search.fit(X_train, y_train)

    # Melhor modelo encontrado
    melhor_modelo = grid_search.best_estimator_
    y_pred = melhor_modelo.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Melhor acurácia: {accuracy * 100:.2f}%")
    print(f"Melhores parâmetros: {grid_search.best_params_}")

    return melhor_modelo, accuracy

# Função para executar a ordem na IQ Option
def executar_ordem(paridade, valor_investimento, direcao):
    _, id = iqoption.buy(valor_investimento, paridade, direcao, 1)
    return id

# Loop principal do programa
while True:
    # Obter os dados das últimas 500 velas
    segundos = datetime.fromtimestamp(iqoption.get_server_timestamp()).strftime('%S')

    if segundos == '50':
        df = obter_velas(paridade, 60)

        # Treinar o modelo de Machine Learning
        model, accuracy = treinar_modelo_com_ajustes(df)

        # Só prever e executar a ordem se a acurácia for maior que 80%
        if accuracy >= 0.8:
            # Prever a direção da próxima vela
            direcao = prever_proxima_vela(model, df)
            print(f"Acurácia é {accuracy * 100:.2f}%, Ordem será executada: {direcao.upper()}")
        else:
            direcao = prever_proxima_vela(model, df)
            print(f"Acurácia de {accuracy * 100:.2f}% é menor que 80%. Ordem não será executada. Ordem: {direcao}")

    if segundos == '00':
        horario = datetime.fromtimestamp(iqoption.get_server_timestamp()).strftime('%H:%M:%S')
        time.sleep(1)
        print(horario)
        if  accuracy >= 0.8:
            id = executar_ordem(paridade, valor_investimento, direcao)
            print(f"Ordem executada: {direcao.upper()} com ID: {id}")
            time.sleep(40)