import requests


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

URL_LAMBDA = "https://qw5pcedi3rtuhgdhvx6ntd6eea0ggafc.lambda-url.ap-east-1.on.aws/"


# ==========================================================
# CHAMAR LAMBDA
# ==========================================================

def chamar_lambda():

    try:

        response = requests.get(
            URL_LAMBDA,
            timeout=30
        )

        print("Status:", response.status_code)
        print("Resposta:", response.text)

        response.raise_for_status()

        return response

    except Exception as erro:

        print("ERRO AO CHAMAR LAMBDA:")
        print(erro)

        return None


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":

    chamar_lambda()