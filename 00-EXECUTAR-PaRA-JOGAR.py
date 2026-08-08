import io
import ast
import time
import importlib
from contextlib import redirect_stdout
from datetime import datetime
import random

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
        print("NENHUMA COMBINAÇÃO VÁLIDA ENCONTRADA")
        print("=" * 50)
        print("Aguardando nova tentativa...")

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
        print("Feche o navegador quando terminar a aposta.")
        page.wait_for_event("close", timeout=0)
        
# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    tentativa = 1

    while True:

        horario = datetime.now().strftime("%H:%M:%S")

        print("\n" * 3)
        print("=" * 60)
        print(f"TENTATIVA {tentativa:05d} | {horario}")
        print("=" * 60)

        jogo = gerar()

        if jogo:

            print()
            print("=" * 60)
            print("COMBINAÇÃO ENCONTRADA")
            print("=" * 60)

            apostar(jogo)
            break

        horario = datetime.now().strftime("%H:%M:%S")

        print()
        print("=" * 60)
        print(f"[{horario}] Combinação não encontrada.")
        print("=" * 60)

        tentativa += 1

        horario = datetime.now().strftime("%H:%M:%S")

        tempo_espera = random.randint(40, 75)

        print()
        print("=" * 60)
        print(f"[{horario}] Nenhum jogo aprovado pelos filtros.")
        print(f"Aguardando {tempo_espera} segundos para nova tentativa...")
        print("=" * 60)

        tentativa += 1

        for restante in range(tempo_espera, 0, -1):

            minutos = restante // 60
            segundos = restante % 60

            print(
                f"\rPróxima tentativa em {minutos:02d}:{segundos:02d}",
                end="",
                flush=True
            )

            time.sleep(1)

        print()
        print()
        print("Iniciando nova tentativa...")
        time.sleep(1)