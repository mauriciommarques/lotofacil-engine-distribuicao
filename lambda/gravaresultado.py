# ==========================================================
# IMPORTS
# ==========================================================

import json
import boto3
import requests

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

    if resultado_banco:

        if (
            resultado_banco["concurso"]
            ==
            resultado_online["concurso"]
        ):

            return {

                "atualizado": False,

                "resultado": resultado_banco

            }

    SalvarResultadoBanco(
        resultado_online
    )

    return {

        "atualizado": True,

        "resultado": resultado_online

    }        

# ==========================================================
# LAMBDA
# ==========================================================

def lambda_handler(event, context):

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
