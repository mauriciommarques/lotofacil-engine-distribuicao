import io
import ast
import time
import importlib
from contextlib import redirect_stdout

from playwright.sync_api import sync_playwright


# ==========================================================
# GERA O JOGO
# ==========================================================

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

        return None

    saida = buffer.getvalue()

    linhas = saida.splitlines()

    for i, linha in enumerate(linhas):

        if linha.strip() == "NOVO RESULTADO":

            jogo = ast.literal_eval(linhas[i + 2])

            print()
            print("=" * 50)
            print("JOGO GERADO")
            print("=" * 50)
            print(jogo)

            return jogo

    print("Resultado não encontrado.")
    return None


# ==========================================================
# AUTOMAÇÃO
# ==========================================================

def apostar(dezenas):

    with sync_playwright() as p:

        context = p.chromium.launch_persistent_context(
            user_data_dir=r"C:\Users\Mauricio\.playwright\lotofacil",
            channel="chrome",
            headless=False
        )

        page = context.new_page()

        print("Abrindo Sorte Online...")

        page.goto(
            "https://www.sorteonline.com.br/catalogo?lotofacil=true&sort=price:desc"
        )

        time.sleep(2)

        print("Entrando na Lotofácil...")

        page.get_by_role(
            "link",
            name="Lotofácil",
            exact=True
        ).click()

        time.sleep(2)

        print("Abrindo volante...")

        page.get_by_role(
            "button",
            name="Apostar Agora",
            exact=True
        ).click()

        time.sleep(2)

        print()
        print("=" * 50)
        print("MARCANDO DEZENAS")
        print("=" * 50)

        for numero in dezenas:

            texto = f"{numero:02d}"

            print("Marcando", texto)

            page.get_by_test_id(
                f"number-button-{numero}"
            ).click()

            time.sleep(1)

        print()
        print("=" * 50)
        print("JOGO PREENCHIDO")
        print("=" * 50)

        input("Confira o volante e pressione ENTER para fechar...")

        context.close()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    jogo = gerar()

    if jogo:

        apostar(jogo)