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

URL = (
    "https://loteriascaixa-api.herokuapp.com/"
    "api/lotofacil/latest"
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

        "concurso": dados["concurso"],

        "dataApuracao": dados["data"],

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
# ATUALIZAÇÃO
# ==========================================================

def AtualizarResultado():

    resultado_online = (
        BuscarResultadoLotoFacilOnline()
    )

    resultado_banco = (
        BuscarResultadoBanco()
    )

    data_esperada = (
        DataUltimoResultadoEsperado()
    )

    data_resultado = datetime.strptime(
        resultado_online["dataApuracao"],
        "%d/%m/%Y"
    ).date()

    print(
        f"[LOTOFACIL] Data resultado API: "
        f"{data_resultado}"
    )

    print(
        f"[LOTOFACIL] Data resultado esperada: "
        f"{data_esperada}"
    )

    # =====================================================
    # RESULTADO AINDA NÃO É O ESPERADO
    # =====================================================

    if data_resultado != data_esperada:

        print(
            "[LOTOFACIL] >>> RESULTADO ESPERADO AINDA NÃO DISPONÍVEL <<<"
        )

        return {

            "atualizado": False,

            "resultado": resultado_banco

        }

    # =====================================================
    # RESULTADO ESPERADO JÁ ESTÁ DISPONÍVEL
    # =====================================================

    if resultado_banco:

        if (
            resultado_banco["concurso"]
            ==
            resultado_online["concurso"]
        ):

            print(
                "[LOTOFACIL] >>> RESULTADO JÁ ESTÁ ATUALIZADO <<<"
            )

            return {

                "atualizado": False,

                "resultado": resultado_banco

            }

    # =====================================================
    # SALVA NOVO RESULTADO
    # =====================================================

    SalvarResultadoBanco(
        resultado_online
    )

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

    data_esperada = DataUltimoResultadoEsperado()

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
