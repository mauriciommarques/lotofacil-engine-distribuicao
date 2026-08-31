# ==========================================================
# IMPORTS
# ==========================================================

import json
import boto3
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# ==========================================================
# CONFIG
# ==========================================================

REGION = "ap-east-1"

TABLE_NAME = "resultado_lotofacil"

TABLE_ESTATISTICA = "estatistica_concurso"

URL = (
    "https://apiloterias.com.br/app/v2/resultado?loteria=lotofacil&token=qjkzMRqoKP1nXUd"
)

lambda_client = boto3.client(
    "lambda",
    region_name=REGION
)

PK = "LOTOFACIL"
SK = "ULTIMO"


def DataUltimoResultadoEsperado():

    agora = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    )

    hoje = agora.date()

    # Segunda-feira
    # Último sorteio foi sábado
    if hoje.weekday() == 0:

        return hoje - timedelta(days=2)

    # Domingo
    # Último sorteio também foi sábado
    if hoje.weekday() == 6:

        return hoje - timedelta(days=1)

    # Terça a sábado
    # Último sorteio foi ontem
    return hoje - timedelta(days=1)

# ==========================================================
# ATUALIZAR ESTATÍSTICA
# ==========================================================

def ChamarAtualizaEstatistica():

    print()
    print("=" * 60)
    print("CHAMANDO ATUALIZA-ESTATISTICA")
    print("=" * 60)

    response = lambda_client.invoke(

        FunctionName="Atualiza-Estatistica",

        InvocationType="RequestResponse",

        Payload=b"{}"

    )

    print(
        "[LOTOFACIL] >>> ATUALIZA-ESTATISTICA EXECUTADA <<<"
    )

    return response


def maior_sequencia(jogo):

    jogo = sorted(jogo)

    maior = 1
    atual = 1

    for i in range(1, len(jogo)):

        if jogo[i] == jogo[i - 1] + 1:

            atual += 1

            maior = max(
                maior,
                atual
            )

        else:

            atual = 1

    return maior


def contar_sequencias(jogo):

    jogo = sorted(jogo)

    sequencias = {}

    atual = 1

    for i in range(1, len(jogo)):

        if jogo[i] == jogo[i - 1] + 1:

            atual += 1

        else:

            if atual >= 2:

                for tamanho in range(
                    2,
                    atual + 1
                ):

                    sequencias[tamanho] = (
                        sequencias.get(
                            tamanho,
                            0
                        ) + 1
                    )

            atual = 1

    # ======================================================
    # ÚLTIMO BLOCO
    # ======================================================

    if atual >= 2:

        for tamanho in range(
            2,
            atual + 1
        ):

            sequencias[tamanho] = (
                sequencias.get(
                    tamanho,
                    0
                ) + 1
            )

    return sequencias


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

estatistica_table = dynamodb.Table(
    TABLE_ESTATISTICA
)


# ==========================================================
# RESULTADO ONLINE
# ==========================================================

def BuscarResultadoLotoFacilOnline():

    response = requests.get(
        URL,
        timeout=15
    )

    response.raise_for_status()

    dados = response.json()

    return {

        "pk": PK,

        "sk": SK,

        "concurso": int(
            dados["numero_concurso"]
        ),

        "dataApuracao": (
            dados["data_concurso"]
        ),

        "listaDezenas": [

            int(n)

            for n in dados["dezenas"]

        ]

    }

# ==========================================================
# PERSISTÊNCIA
# ==========================================================

def SalvarResultadoBanco(
    resultado
):

    table.put_item(

        Item=resultado

    )


def BuscarResultadoBanco():

    response = table.get_item(

        Key={

            "pk": PK,

            "sk": SK

        }

    )

    item = response.get(
        "Item"
    )

    return item


# ==========================================================
# ESTATÍSTICA DO CONCURSO
# ==========================================================

def SalvarEstatisticaConcurso(resultado):

    jogo = resultado["listaDezenas"]

    pares = {
        2, 4, 6, 8, 10, 12,
        14, 16, 18, 20, 22, 24
    }

    impares = {
        1, 3, 5, 7, 9, 11,
        13, 15, 17, 19, 21, 23, 25
    }

    primos = {
        2, 3, 5, 7, 11,
        13, 17, 19, 23
    }

    fibonacci = {
        1, 2, 3, 5, 8, 13, 21
    }

    multiplos3 = {
        3, 6, 9, 12,
        15, 18, 21, 24
    }

    moldura = {
        1, 2, 3, 4, 5, 6,
        10, 11, 15, 16,
        20, 21, 22, 23, 24, 25
    }

    centro = {
        12, 13, 14,
        17, 18, 19
    }

    # ======================================================
    # ORDENAÇÃO
    # ======================================================

    jogo_ordenado = sorted(jogo)

    # ======================================================
    # SEQUÊNCIAS
    # ======================================================

    quantidade_sequencias = contar_sequencias(
        jogo_ordenado
    )

    maior_seq = maior_sequencia(
        jogo_ordenado
    )

    # ======================================================
    # ESTATÍSTICA
    # ======================================================

    estatistica = {

        "pk": "LOTOFACIL",

        "sk": f"CONCURSO#{resultado['concurso']}",

        "concurso": int(
            resultado["concurso"]
        ),

        "dataApuracao": (
            resultado["dataApuracao"]
        ),

        # ==================================================
        # PARES / ÍMPARES
        # ==================================================

        "quantidade_pares": len([

            n for n in jogo

            if n in pares

        ]),

        "quantidade_impares": len([

            n for n in jogo

            if n in impares

        ]),

        # ==================================================
        # PRIMOS
        # ==================================================

        "quantidade_primos": len([

            n for n in jogo

            if n in primos

        ]),

        # ==================================================
        # FIBONACCI
        # ==================================================

        "quantidade_fibonacci": len([

            n for n in jogo

            if n in fibonacci

        ]),

        # ==================================================
        # MÚLTIPLOS DE 3
        # ==================================================

        "quantidade_multiplos3": len([

            n for n in jogo

            if n in multiplos3

        ]),

        # ==================================================
        # MOLDURA
        # ==================================================

        "quantidade_moldura": len([

            n for n in jogo

            if n in moldura

        ]),

        # ==================================================
        # CENTRO
        # ==================================================

        "quantidade_centro": len([

            n for n in jogo

            if n in centro

        ]),

        # ==================================================
        # SEQUÊNCIAS
        # ==================================================

        "quantidade_sequencias_2": (
            quantidade_sequencias.get(
                2,
                0
            )
        ),

        "quantidade_sequencias_3": (
            quantidade_sequencias.get(
                3,
                0
            )
        ),

        "quantidade_sequencias_4": (
            quantidade_sequencias.get(
                4,
                0
            )
        ),

        "quantidade_sequencias_5": (
            quantidade_sequencias.get(
                5,
                0
            )
        ),

        "quantidade_sequencias_6": (
            quantidade_sequencias.get(
                6,
                0
            )
        ),

        "quantidade_sequencias_7": (
            quantidade_sequencias.get(
                7,
                0
            )
        ),

        "quantidade_sequencias_8": (
            quantidade_sequencias.get(
                8,
                0
            )
        ),

        "quantidade_sequencias_9": (
            quantidade_sequencias.get(
                9,
                0
            )
        ),

        # ==================================================
        # MAIOR SEQUÊNCIA
        # ==================================================

        "maior_sequencia": (
            maior_seq
        )
    }

    # ======================================================
    # SALVA NO DYNAMODB
    # ======================================================

    estatistica_table.put_item(
        Item=estatistica
    )

    print(
        "[LOTOFACIL] >>> ESTATÍSTICA DO CONCURSO SALVA <<<"
    )

# ==========================================================
# ATUALIZAÇÃO
# ==========================================================

def AtualizarResultado():

    resultado_online = (
        BuscarResultadoLotoFacilOnline()
    )

    resultado_banco = (
        BuscarResultadoBanco()
    )

    print(
        f"[LOTOFACIL] Concurso API: "
        f"{resultado_online['concurso']}"
    )

    print(
        f"[LOTOFACIL] Data resultado API: "
        f"{resultado_online['dataApuracao']}"
    )

    # ======================================================
    # VERIFICA SE JÁ EXISTE RESULTADO NO BANCO
    # ======================================================

    if resultado_banco:

        concurso_banco = int(
            resultado_banco["concurso"]
        )

        concurso_online = int(
            resultado_online["concurso"]
        )

        print(
            f"[LOTOFACIL] Concurso banco: "
            f"{concurso_banco}"
        )

        # ==================================================
        # RESULTADO JÁ ATUALIZADO OU API ATRASADA
        # ==================================================

        if concurso_online <= concurso_banco:

            print(
                "[LOTOFACIL] >>> RESULTADO "
                "JÁ ESTÁ ATUALIZADO <<<"
            )

            return {

                "atualizado": False,

                "resultado": resultado_banco

            }

    # ======================================================
    # SALVA NOVO RESULTADO
    # ======================================================

    SalvarResultadoBanco(
        resultado_online
    )

    SalvarEstatisticaConcurso(
        resultado_online
    )

    ChamarAtualizaEstatistica()

    print(
        "[LOTOFACIL] >>> NOVO RESULTADO SALVO <<<"
    )

    return {

        "atualizado": True,

        "resultado": resultado_online

    }


    # ======================================================
    # SALVA NOVO RESULTADO
    # ======================================================

    SalvarResultadoBanco(
        resultado_online
    )

    SalvarEstatisticaConcurso(
        resultado_online
    )

    ChamarAtualizaEstatistica()

    print(
        "[LOTOFACIL] >>> NOVO RESULTADO SALVO <<<"
    )

    return {

        "atualizado": True,

        "resultado": resultado_online

    }


# ==========================================================
# LAMBDA
# ==========================================================

def lambda_handler(event, context):

    data_esperada = (
        DataUltimoResultadoEsperado()
    )

    print(
        f"[LOTOFACIL] Data/hora São Paulo: "
        f"{datetime.now(ZoneInfo('America/Sao_Paulo'))}"
    )

    print(
        f"[LOTOFACIL] Último resultado esperado: "
        f"{data_esperada}"
    )

    try:

        atualizacao = (
            AtualizarResultado()
        )

        if atualizacao["atualizado"]:

            mensagem = (
                "Resultado atualizado."
            )

        else:

            mensagem = (
                "Resultado já atualizado."
            )

        return {

            "statusCode": 200,

            "body": json.dumps({

                "mensagem": mensagem,

                "concurso": int(
                    atualizacao["resultado"]["concurso"]
                ),

                "dataApuracao": (
                    atualizacao["resultado"]["dataApuracao"]
                )

            }, ensure_ascii=False)

        }

    except Exception as erro:

        return {

            "statusCode": 500,

            "body": json.dumps({

                "erro": str(erro)

            }, ensure_ascii=False)

        }
     