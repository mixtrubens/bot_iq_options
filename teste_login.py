from iqoptionapi.stable_api import IQ_Option
import time

def main():
    email = 'rubinho132@hotmail.com'
    password = 'Ax206487'

    try:
        iqoption = IQ_Option(email, password)
        iqoption.connect()

        if iqoption.check_connect():
            print("Autenticado com sucesso")
        else:
            print("Erro na autenticação")
            reason = iqoption.api.get_reason_message()
            print(f"Motivo: {reason}")
            return

    except Exception as e:
        print(f"Erro ao conectar à IQ Option: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()