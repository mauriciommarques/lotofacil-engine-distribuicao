# ==========================================================
# IMPORTS
# ==========================================================

import boto3


# ==========================================================
# CONFIG
# ==========================================================

REGION = "ap-east-1"

TABLE_NAME = "parametrossistema"

PK = "LOTOFACIL"

SK = "PARAMETROS"

# ==========================================================
# PARÂMETROS DO SISTEMA
# ==========================================================

PARAMETROS = {

    "QTD_PARES": 7,

    "QTD_IMPARES": 8,

    "QTD_PRIMOS": 5,

    "QTD_FIBONACCI": 4,

    "QTD_MULTIPLOS3": 5,

    "QTD_MOLDURA": 10,

    "QTD_CENTRO": 4,

    # ------------------------------------------------------
    # SEQUÊNCIAS DO JOGO FINAL
    # ------------------------------------------------------

    "MAX_SEQUENCIA": 5,

    "MAX_QTD_SEQUENCIAS": 3,

    "TAMANHO_MINIMO_SEQUENCIA": 3,

    # ------------------------------------------------------
    # SEQUÊNCIA DOS FIXOS
    # ------------------------------------------------------

    "MAX_SEQUENCIA_FIXOS": 2
}


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
# SALVAR PARÂMETROS
# ==========================================================

def SalvarParametros():

    item = {

        "pk": PK,

        "sk": SK,

        **PARAMETROS

    }

    table.put_item(
        Item=item
    )

    print(
        "[LOTOFACIL] >>> PARÂMETROS DO SISTEMA SALVOS <<<"
    )


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":

    try:

        SalvarParametros()

        print(
            "[LOTOFACIL] >>> CONCLUÍDO <<<"
        )

    except Exception as erro:

        print(
            f"[LOTOFACIL] >>> ERRO: {erro} <<<"
        )

