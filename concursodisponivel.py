import requests

def conferir_concurso():

    url = "https://api.guidi.dev.br/loteria/lotofacil/ultimo"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    dados = response.json()

    print("=" * 50)
    print("      ÚLTIMO CONCURSO DA LOTOFÁCIL")
    print("=" * 50)
    print(f"Concurso : {dados['numero']}")
    print(f"Data     : {dados['dataApuracao']}")
    print(f"Próximo  : {dados['dataProximoConcurso']}")
    print()
    print("Dezenas sorteadas:")
    print(" ".join(dados["listaDezenas"]))
    print("=" * 50)


if __name__ == "__main__":
    conferir_concurso()