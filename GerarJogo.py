import io
import importlib
from contextlib import redirect_stdout


def gerar():

    buffer = io.StringIO()

    try:

        with redirect_stdout(buffer):

            import EngineDistribuicao
            importlib.reload(EngineDistribuicao)

    except SystemExit:

        print()
        print("=" * 50)
        print("FALHA AO GERAR O JOGO")
        print("=" * 50)
        print("Execute novamente o gerador (F5).")
        return

    saida = buffer.getvalue()

    linhas = saida.splitlines()

    for i, linha in enumerate(linhas):

        if linha.strip() == "NOVO RESULTADO":

            print("=" * 50)
            print("JOGO GERADO")
            print("=" * 50)

            print(linhas[i + 2])

            return

    print("Resultado não encontrado.")


if __name__ == "__main__":

    gerar()