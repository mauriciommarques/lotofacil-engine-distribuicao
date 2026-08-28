# ==========================================================
# IMPORTS
# ==========================================================

import boto3


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

REGION = "ap-east-1"

TABLE_NAME = "parametrossistema"

PK = "LOTOFACIL"

SK = "PARAMETROS"


# ==========================================================
# PARÂMETROS DO SISTEMA
# ==========================================================
#
# Os valores abaixo são carregados do DynamoDB
# pela função CarregarParametrosSistema().
#
# ----------------------------------------------------------
# INDICADORES DO JOGO
# ----------------------------------------------------------
# QTD_PARES              → quantidade de números pares permitida
# QTD_IMPARES            → quantidade de números ímpares permitida
# QTD_PRIMOS             → quantidade de números primos permitida
# QTD_FIBONACCI          → quantidade de números Fibonacci permitida
# QTD_MULTIPLOS3         → quantidade de múltiplos de 3 permitida
# QTD_MOLDURA            → quantidade de números da moldura permitida
# QTD_CENTRO             → quantidade de números do centro permitida
#

# ----------------------------------------------------------
# REGRAS DE SEQUÊNCIA
# ----------------------------------------------------------
# MAX_SEQUENCIA
# → tamanho máximo de uma sequência.
#   Exemplo: 01-02-03-04-05 = sequência de tamanho 5.
#
# TAMANHO_MINIMO_SEQUENCIA
# → tamanho mínimo para considerar um bloco como sequência.
#   Exemplo: 01-02-03 = sequência.
#   Exemplo: 01-02 = não é considerado sequência.
#
# MAX_QTD_SEQUENCIAS
# → quantidade máxima de blocos de sequência permitidos.
#   Exemplo: 01-02-03 | 07-08-09 | 12-13-14 = 3 blocos.
#   Se MAX_QTD_SEQUENCIAS = 3 → permitido.
#   Com 4 blocos → não permitido.
#
# ----------------------------------------------------------
# REGRAS DOS FIXOS
# ----------------------------------------------------------
# MAX_SEQUENCIA_FIXOS
# → tamanho máximo de uma sequência entre os números fixos.
#   Exemplo: fixos 01-02-03-07-08-10
#   possui uma sequência de tamanho 3 (01-02-03).
#
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
# REMOVER CONFIGURAÇÃO ANTERIOR
# ==========================================================

def LimparParametros():

    print(
        "[LOTOFACIL] >>> REMOVENDO CONFIGURAÇÃO ANTERIOR <<<"
    )

    table.delete_item(

        Key={

            "pk": PK,

            "sk": SK

        }

    )

    print(
        "[LOTOFACIL] >>> CONFIGURAÇÃO ANTERIOR REMOVIDA <<<"
    )


# ==========================================================
# SALVAR NOVA CONFIGURAÇÃO
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
        "[LOTOFACIL] >>> NOVA CONFIGURAÇÃO SALVA <<<"
    )


# ==========================================================
# VALIDAR CONFIGURAÇÃO GRAVADA
# ==========================================================

def ValidarParametros():

    response = table.get_item(

        Key={

            "pk": PK,

            "sk": SK

        }

    )

    item = response.get(
        "Item"
    )

    if not item:

        raise Exception(
            "Configuração não encontrada após gravação."
        )

    print()
    print(
        "=========================================================="
    )
    print(
        "[LOTOFACIL] >>> CONFIGURAÇÃO CONFIRMADA NO DYNAMODB <<<"
    )
    print(
        "=========================================================="
    )

    print(
        f"PK: {item.get('pk')}"
    )

    print(
        f"SK: {item.get('sk')}"
    )

    print()

    for nome, valor_esperado in PARAMETROS.items():

        valor_gravado = item.get(
            nome
        )

        if valor_gravado != valor_esperado:

            raise Exception(
                f"Parâmetro {nome} divergente. "
                f"Esperado: {valor_esperado} | "
                f"Gravado: {valor_gravado}"
            )

        print(
            f"{nome}: {valor_gravado} ✓"
        )

    print()
    print(
        "[LOTOFACIL] >>> TODOS OS PARÂMETROS CONFIRMADOS <<<"
    )
    print(
        "=========================================================="
    )


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":

    try:

        # --------------------------------------------------
        # 1. REMOVE A CONFIGURAÇÃO ANTERIOR
        # --------------------------------------------------

        LimparParametros()

        # --------------------------------------------------
        # 2. GRAVA A NOVA CONFIGURAÇÃO
        # --------------------------------------------------

        SalvarParametros()

        # --------------------------------------------------
        # 3. LÊ NOVAMENTE E CONFIRMA
        # --------------------------------------------------

        ValidarParametros()

        # --------------------------------------------------
        # CONCLUÍDO
        # --------------------------------------------------

        print()
        print(
            "[LOTOFACIL] >>> CONFIGURAÇÃO APLICADA COM SUCESSO <<<"
        )

    except Exception as erro:

        print()
        print(
            f"[LOTOFACIL] >>> ERRO: {erro} <<<"
        )
