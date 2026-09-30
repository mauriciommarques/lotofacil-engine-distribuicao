import json
import boto3
import random

from datetime import datetime
from zoneinfo import ZoneInfo


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

REGION = "ap-east-1"

TABLE_RESULTADO = "resultado_lotofacil"

TABLE_JOGOS = "jogos_lotofacil"

ENGINE = "DESDOBRAMENTO-6"

ENGINE_VERSION = "1.0"

TIMEZONE = ZoneInfo(
    "America/Sao_Paulo"
)


# ==========================================================
# DYNAMODB
# ==========================================================

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION
)

resultado_table = dynamodb.Table(
    TABLE_RESULTADO
)

jogos_table = dynamodb.Table(
    TABLE_JOGOS
)


# ==========================================================
# BUSCAR ÚLTIMO RESULTADO
# ==========================================================

def buscar_resultado_concurso_anterior():

    response = resultado_table.get_item(
        Key={
            "pk": "LOTOFACIL",
            "sk": "ULTIMO"
        }
    )

    item = response.get(
        "Item"
    )

    if not item:

        raise Exception(
            "Resultado da Lotofácil não encontrado."
        )

    return item


# ==========================================================
# LIMPAR TABELA DE JOGOS
# ==========================================================

def limpar_tabela_jogos():

    itens_removidos = 0

    # ------------------------------------------------------
    # BUSCAR SOMENTE AS CHAVES
    # ------------------------------------------------------

    response = jogos_table.scan(
        ProjectionExpression="pk, sk"
    )

    while True:

        itens = response.get(
            "Items",
            []
        )

        # --------------------------------------------------
        # REMOVER EM BATCH
        # --------------------------------------------------

        if itens:

            with jogos_table.batch_writer() as batch:

                for item in itens:

                    batch.delete_item(
                        Key={
                            "pk": item["pk"],
                            "sk": item["sk"]
                        }
                    )

                    itens_removidos += 1

        # --------------------------------------------------
        # VERIFICAR PAGINAÇÃO
        # --------------------------------------------------

        if "LastEvaluatedKey" not in response:

            break

        response = jogos_table.scan(
            ProjectionExpression="pk, sk",
            ExclusiveStartKey=response[
                "LastEvaluatedKey"
            ]
        )

    return itens_removidos


# ==========================================================
# SALVAR JOGO
# ==========================================================

def salvar_jogo(
    concurso,
    jogo,
    tipo_combinacao
):

    agora = datetime.now(
        TIMEZONE
    )

    data = agora.strftime(
        "%Y-%m-%d"
    )

    sk = (
        f"{concurso}"
        f"#{ENGINE}"
        f"#{tipo_combinacao}"
    )


    # ------------------------------------------------------
    # IMPORTANTE:
    #
    # O jogo é salvo EXATAMENTE na ordem recebida.
    #
    # NÃO ORDENAR.
    # ------------------------------------------------------

    item = {
        "pk":
            "JOGO",

        "sk":
            sk,

        "data":
            data,

        "concurso":
            concurso,

        "engine":
            ENGINE,

        "engine_version":
            ENGINE_VERSION,

        "tipo_combinacao":
            tipo_combinacao,

        "jogo":
            jogo
    }

    jogos_table.put_item(
        Item=item
    )


# ==========================================================
# MONTAR OS 6 JOGOS
# ==========================================================

def montar_jogos():

    resultado_anterior = (
        buscar_resultado_concurso_anterior()
    )

    concurso_anterior = int(
        resultado_anterior["concurso"]
    )

    proximo_concurso = (
        concurso_anterior + 1
    )


    # ======================================================
    # 15 DEZENAS DO CONCURSO ANTERIOR
    #
    # NÃO ORDENAR.
    # ======================================================

    dezenas_anteriores = [
        int(numero)
        for numero
        in resultado_anterior["listaDezenas"]
    ]

    if len(dezenas_anteriores) != 15:

        raise Exception(
            "O concurso anterior deve possuir "
            "exatamente 15 dezenas."
        )

    if len(set(dezenas_anteriores)) != 15:

        raise Exception(
            "O concurso anterior possui "
            "dezenas repetidas."
        )


    # ======================================================
    # 10 DEZENAS NÃO SORTEADAS
    #
    # NÃO ADICIONAR ORDENAÇÃO.
    # ======================================================

    nao_sorteadas = [
        numero
        for numero in range(1, 26)
        if numero not in dezenas_anteriores
    ]

    if len(nao_sorteadas) != 10:

        raise Exception(
            "Devem existir exatamente "
            "10 dezenas não sorteadas."
        )


    # ======================================================
    # GERADOR ALEATÓRIO
    #
    # Mesmo concurso = mesma projeção.
    #
    # IMPORTANTE:
    # usar o MESMO gerador durante todo o processo.
    # ======================================================

    gerador = random.Random(
        concurso_anterior
    )


    # ======================================================
    # EMBARALHAR AS 15 DEZENAS ANTERIORES
    #
    # NÃO ORDENAR.
    # ======================================================

    dezenas_embaralhadas = (
        dezenas_anteriores.copy()
    )

    gerador.shuffle(
        dezenas_embaralhadas
    )


    # ======================================================
    # 3 FIXAS
    # ======================================================

    fixas = (
        dezenas_embaralhadas[0:3]
    )


    # ======================================================
    # 5 DEZENAS PRÓPRIAS DO CONJ1
    # ======================================================

    dezenas_conj1 = (
        dezenas_embaralhadas[3:8]
    )


    # ======================================================
    # 5 DEZENAS PRÓPRIAS DO CONJ2
    # ======================================================

    dezenas_conj2 = (
        dezenas_embaralhadas[8:13]
    )


    # ======================================================
    # CONJ1
    #
    # 3 fixas + 5 dezenas = 8
    # ======================================================

    conj1 = (
        fixas +
        dezenas_conj1
    )


    # ======================================================
    # CONJ2
    #
    # mesmas 3 fixas + outras 5 dezenas = 8
    # ======================================================

    conj2 = (
        fixas +
        dezenas_conj2
    )


    # ======================================================
    # VALIDAR CONJ1 / CONJ2
    # ======================================================

    if len(conj1) != 8:

        raise Exception(
            "CONJ1 deve possuir exatamente 8 dezenas."
        )

    if len(set(conj1)) != 8:

        raise Exception(
            "CONJ1 possui dezenas repetidas."
        )

    if len(conj2) != 8:

        raise Exception(
            "CONJ2 deve possuir exatamente 8 dezenas."
        )

    if len(set(conj2)) != 8:

        raise Exception(
            "CONJ2 possui dezenas repetidas."
        )

    if (
        set(conj1).intersection(
            set(conj2)
        )
        !=
        set(fixas)
    ):

        raise Exception(
            "CONJ1 e CONJ2 devem compartilhar "
            "exatamente as 3 dezenas fixas."
        )


    # ======================================================
    # CONJ_NS
    #
    # 10 dezenas não sorteadas.
    #
    # NÃO ORDENAR.
    # ======================================================

    conj_ns = (
        nao_sorteadas.copy()
    )


    # ======================================================
    # EMBARALHAR CONJ_NS
    #
    # CONTINUA USANDO O MESMO GERADOR.
    #
    # NÃO RECRIAR O GERADOR.
    # NÃO ORDENAR.
    # ======================================================

    gerador.shuffle(
        conj_ns
    )


    # ======================================================
    # FIXA_NS
    # ======================================================

    fixa_ns = (
        conj_ns[0]
    )


    # ======================================================
    # NS_1
    # ======================================================

    ns_1 = (
        conj_ns[1:4]
    )


    # ======================================================
    # NS_2
    # ======================================================

    ns_2 = (
        conj_ns[4:7]
    )


    # ======================================================
    # NS_3
    # ======================================================

    ns_3 = (
        conj_ns[7:10]
    )


    # ======================================================
    # VALIDAR NS
    # ======================================================

    if len(conj_ns) != 10:

        raise Exception(
            "CONJ_NS deve possuir exatamente 10 dezenas."
        )

    if len(set(conj_ns)) != 10:

        raise Exception(
            "CONJ_NS possui dezenas repetidas."
        )

    if fixa_ns in conj1 or fixa_ns in conj2:

        raise Exception(
            "FIXA_NS não pode pertencer "
            "ao CONJ1 nem ao CONJ2."
        )

    if len(ns_1) != 3:

        raise Exception(
            "NS_1 deve possuir exatamente 3 dezenas."
        )

    if len(ns_2) != 3:

        raise Exception(
            "NS_2 deve possuir exatamente 3 dezenas."
        )

    if len(ns_3) != 3:

        raise Exception(
            "NS_3 deve possuir exatamente 3 dezenas."
        )


    # ======================================================
    # SEP_1
    #
    # fixa_ns + ns_1 + ns_2
    # ======================================================

    sep_1 = (
        [fixa_ns] +
        ns_1 +
        ns_2
    )


    # ======================================================
    # SEP_2
    #
    # fixa_ns + ns_1 + ns_3
    # ======================================================

    sep_2 = (
        [fixa_ns] +
        ns_1 +
        ns_3
    )


    # ======================================================
    # SEP_3
    #
    # fixa_ns + ns_2 + ns_3
    # ======================================================

    sep_3 = (
        [fixa_ns] +
        ns_2 +
        ns_3
    )


    # ======================================================
    # VALIDAR SEP
    # ======================================================

    separacoes = [
        sep_1,
        sep_2,
        sep_3
    ]

    for indice, separacao in enumerate(
        separacoes,
        start=1
    ):

        if len(separacao) != 7:

            raise Exception(
                f"SEP_{indice} deve possuir "
                "exatamente 7 dezenas."
            )

        if len(set(separacao)) != 7:

            raise Exception(
                f"SEP_{indice} possui "
                "dezenas repetidas."
            )


    # ======================================================
    # MONTAR OS 6 JOGOS
    #
    # NÃO ORDENAR.
    # ======================================================

    jogo_1 = (
        conj1 +
        sep_1
    )

    jogo_2 = (
        conj1 +
        sep_2
    )

    jogo_3 = (
        conj1 +
        sep_3
    )

    jogo_4 = (
        conj2 +
        sep_1
    )

    jogo_5 = (
        conj2 +
        sep_2
    )

    jogo_6 = (
        conj2 +
        sep_3
    )


    # ======================================================
    # ESTRUTURA DOS 6 JOGOS
    # ======================================================

    jogos = [
        {
            "tipo_combinacao":
                "CONJ1-SEP1",

            "jogo":
                jogo_1
        },

        {
            "tipo_combinacao":
                "CONJ1-SEP2",

            "jogo":
                jogo_2
        },

        {
            "tipo_combinacao":
                "CONJ1-SEP3",

            "jogo":
                jogo_3
        },

        {
            "tipo_combinacao":
                "CONJ2-SEP1",

            "jogo":
                jogo_4
        },

        {
            "tipo_combinacao":
                "CONJ2-SEP2",

            "jogo":
                jogo_5
        },

        {
            "tipo_combinacao":
                "CONJ2-SEP3",

            "jogo":
                jogo_6
        }
    ]


    # ======================================================
    # VALIDAR OS 6 JOGOS
    #
    # IMPORTANTE:
    # A TABELA AINDA NÃO FOI LIMPA.
    # ======================================================

    for indice, item in enumerate(
        jogos,
        start=1
    ):

        jogo = item["jogo"]

        if len(jogo) != 15:

            raise Exception(
                f"Jogo {indice} deve possuir "
                "exatamente 15 dezenas."
            )

        if len(set(jogo)) != 15:

            raise Exception(
                f"Jogo {indice} possui "
                "dezenas repetidas."
            )


    # ======================================================
    # SOMENTE AGORA LIMPAR A TABELA
    #
    # Os 6 jogos já foram gerados e validados.
    #
    # Se qualquer validação acima falhar,
    # jogos_lotofacil permanece intacta.
    # ======================================================

    removidos = (
        limpar_tabela_jogos()
    )


    # ======================================================
    # SALVAR OS 6 NOVOS JOGOS
    # ======================================================

    for item in jogos:

        salvar_jogo(
            concurso=proximo_concurso,
            jogo=item["jogo"],
            tipo_combinacao=item[
                "tipo_combinacao"
            ]
        )


    # ======================================================
    # RETORNO
    # ======================================================

    return {
        "concurso_anterior":
            concurso_anterior,

        "concurso":
            proximo_concurso,

        "jogo_1":
            jogo_1,

        "jogo_2":
            jogo_2,

        "jogo_3":
            jogo_3,

        "jogo_4":
            jogo_4,

        "jogo_5":
            jogo_5,

        "jogo_6":
            jogo_6,

        "removidos":
            removidos,

        "salvos":
            6
    }


# ==========================================================
# HANDLER
# ==========================================================

def lambda_handler(
    event,
    context
):

    try:

        resultado = (
            montar_jogos()
        )


        # ==================================================
        # PRINT FINAL
        # ==================================================

        print()
        print("========================================")
        print(" 6 JOGOS FINAIS - 15 DEZENAS")
        print("========================================")

        print(
            "JOGO 1:",
            resultado["jogo_1"]
        )

        print(
            "JOGO 2:",
            resultado["jogo_2"]
        )

        print(
            "JOGO 3:",
            resultado["jogo_3"]
        )

        print(
            "JOGO 4:",
            resultado["jogo_4"]
        )

        print(
            "JOGO 5:",
            resultado["jogo_5"]
        )

        print(
            "JOGO 6:",
            resultado["jogo_6"]
        )

        print("========================================")

        print(
            "Jogos antigos removidos:",
            resultado["removidos"]
        )

        print(
            "Jogos novos salvos:",
            resultado["salvos"]
        )

        print("========================================")


        # ==================================================
        # RETORNO
        # ==================================================

        return {
            "statusCode": 200,

            "body": json.dumps({
                "concurso":
                    resultado["concurso"],

                "jogo_1":
                    resultado["jogo_1"],

                "jogo_2":
                    resultado["jogo_2"],

                "jogo_3":
                    resultado["jogo_3"],

                "jogo_4":
                    resultado["jogo_4"],

                "jogo_5":
                    resultado["jogo_5"],

                "jogo_6":
                    resultado["jogo_6"],

                "removidos":
                    resultado["removidos"],

                "salvos":
                    resultado["salvos"],

                "engine":
                    ENGINE
            })
        }


    except Exception as erro:

        print(
            "Erro:",
            str(erro)
        )

        return {
            "statusCode": 500,

            "body": json.dumps({
                "erro":
                    str(erro)
            })
        }


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    resposta = lambda_handler(
        {},
        None
    )

    print()
    print(
        "Status:",
        resposta["statusCode"]
    )

    print(
        "Resposta:",
        resposta["body"]
    )