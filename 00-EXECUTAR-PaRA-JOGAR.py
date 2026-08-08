# ==========================================================
# IMPORTS
# ==========================================================

import time

from datetime import datetime

import boto3

from playwright.sync_api import sync_playwright

# ==========================================================
# CONFIG
# ==========================================================

REGION = "ap-east-1"

TABLE_NAME = "jogos_lotofacil"

# ==========================================================
# DYNAMODB
# ==========================================================

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION
)

table = dynamodb.Table(
    TABLE_NAME
)

# ==========================================================
# BUSCAR JOGO
# ==========================================================

def BuscarJogos():

    response = table.scan()

    jogos = response.get(
        "Items",
        []
    )

    hoje = datetime.now().strftime("%Y-%m-%d")

    jogos = [

        jogo

        for jogo in jogos

        if jogo["data"] == hoje

    ]

    if not jogos:

        return None

    jogos.sort(
        key=lambda jogo: jogo["sk"]
    )

    return jogos

# ==========================================================
# AUTOMAÇÃO
# ==========================================================

def apostar(
    page,
    jogo
):

    dezenas = jogo["jogo"]

    print()
    print("=" * 50)
    print("MARCANDO DEZENAS")
    print("=" * 50)

    print("Concurso :", jogo["concurso"])
    print("Data      :", jogo["data"])

    print()

    for numero in dezenas:

        texto = f"{numero:02d}"

        print("Marcando", texto)

        page.get_by_test_id(
            f"number-button-{numero}"
        ).click()

        time.sleep(1)

    print()

    print("Aguardando validação do volante...")

    time.sleep(2)

    botao = page.get_by_role(
        "button",
        name="Incluir aposta",
        exact=True
    )

    botao.wait_for()

    print("Incluindo aposta no carrinho...")

    botao.click()

    page.wait_for_load_state(
        "networkidle"
    )

    time.sleep(1)
        
# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":

    jogos = BuscarJogos()

    if not jogos:

        print("Nenhum jogo disponível.")
        exit()

    print()
    print("=" * 60)
    print(f"{len(jogos)} jogo(s) encontrado(s).")
    print("=" * 60)

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

        page.wait_for_load_state(
            "networkidle"
        )

        time.sleep(1)

        print("Entrando na Lotofácil...")

        page.get_by_role(
            "link",
            name="Lotofácil",
            exact=True
        ).click()

        time.sleep(2)

        print("Abrindo volante...")

        botao = page.get_by_role(
            "button",
            name="Apostar Agora",
            exact=True
        )

        botao.wait_for()

        botao.click()

        time.sleep(2)

        for indice, jogo in enumerate(jogos, start=1):

            print()
            print("=" * 60)
            print(f"JOGO {indice}")
            print("=" * 60)

            apostar(
                page,
                jogo
            )

        print()
        print("=" * 60)
        print("TODOS OS JOGOS FORAM ADICIONADOS AO CARRINHO")
        print("=" * 60)
        print("Revise os jogos.")
        print("Remova os que não desejar.")
        print("Finalize a compra.")
        print("Depois feche o navegador.")
        print("=" * 60)

        page.wait_for_event(
            "close",
            timeout=0
        )
