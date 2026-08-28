# ==========================================================
# IMPORTS
# ==========================================================

import json
import boto3


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

REGION = "ap-east-1"

TABLE_ESTATISTICA = "estatistica_concurso"

TABLE_PARAMETROS = "parametrossistema"

PK = "LOTOFACIL"

SK = "PARAMETROS"


# ==========================================================
# ANÁLISE
# ==========================================================

QTD_DIAS = 10


# ==========================================================
# PARÂMETROS FIXOS
# ==========================================================

MAX_QTD_SEQUENCIAS = 3

TAMANHO_MINIMO_SEQUENCIA = 3

MAX_SEQUENCIA_FIXOS = 2


# ==========================================================
# DYNAMODB
# ==========================================================

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION
)

estatistica_table = dynamodb.Table(
    TABLE_ESTATISTICA
)

parametros_table = dynamodb.Table(
    TABLE_PARAMETROS
)


# ==========================================================
# CARREGAR CONCURSOS
# ==========================================================

def CarregarConcursos():

    response = estatistica_table.scan()

    itens = response.get(
        "Items",
        []
    )

    while "LastEvaluatedKey" in response:

        response = estatistica_table.scan(
            ExclusiveStartKey=response[
                "LastEvaluatedKey"
            ]
        )

        itens.extend(
            response.get(
                "Items",
                []
            )
        )

    return itens


# ==========================================================
# MÉDIA
# ==========================================================

def CalcularMedia(
    grupo,
    campo
):

    valores = [

        int(item[campo])

        for item in grupo

        if campo in item

    ]

    if not valores:

        return 0

    return (
        sum(valores)
        /
        len(valores)
    )


# ==========================================================
# ANÁLISE DOS INDICADORES
# ==========================================================

def AnalisarIndicadores(
    concursos
):

    # ------------------------------------------------------
    # MAIS RECENTE → MAIS ANTIGO
    # ------------------------------------------------------

    concursos = sorted(

        concursos,

        key=lambda x: int(
            x["concurso"]
        ),

        reverse=True

    )

    print(
        f"[LOTOFACIL] Concursos carregados: "
        f"{len(concursos)}"
    )


    # ------------------------------------------------------
    # ACUMULADORES
    # ------------------------------------------------------

    soma_pares = 0

    soma_impares = 0

    soma_primos = 0

    soma_fibonacci = 0

    soma_multiplos3 = 0

    soma_moldura = 0

    soma_centro = 0

    soma_quantidade_sequencias = 0

    soma_maior_sequencia = 0

    quantidade_blocos = 0


    # ======================================================
    # BLOCOS
    # ======================================================

    inicio = 0

    while (

        inicio + QTD_DIAS
        <= len(concursos)

    ):

        grupo = concursos[

            inicio:
            inicio + QTD_DIAS

        ]


        # ==================================================
        # INDICADORES BÁSICOS
        # ==================================================

        media_pares = CalcularMedia(

            grupo,

            "quantidade_pares"

        )

        media_impares = CalcularMedia(

            grupo,

            "quantidade_impares"

        )

        media_primos = CalcularMedia(

            grupo,

            "quantidade_primos"

        )

        media_fibonacci = CalcularMedia(

            grupo,

            "quantidade_fibonacci"

        )

        media_multiplos3 = CalcularMedia(

            grupo,

            "quantidade_multiplos3"

        )

        media_moldura = CalcularMedia(

            grupo,

            "quantidade_moldura"

        )

        media_centro = CalcularMedia(

            grupo,

            "quantidade_centro"

        )


        # ==================================================
        # SEQUÊNCIAS
        # ==================================================

        totais_sequencias = []


        for item in grupo:

            total = 0


            for tamanho in range(
                2,
                10
            ):

                campo = (
                    f"quantidade_sequencias_{tamanho}"
                )


                if campo in item:

                    total += int(
                        item[campo]
                    )


            totais_sequencias.append(
                total
            )


        if totais_sequencias:

            media_quantidade_sequencias = (

                sum(
                    totais_sequencias
                )
                /
                len(
                    totais_sequencias
                )

            )

        else:

            media_quantidade_sequencias = 0


        # ==================================================
        # MAIOR SEQUÊNCIA
        # ==================================================

        media_maior_sequencia = CalcularMedia(

            grupo,

            "maior_sequencia"

        )


        # ==================================================
        # ACUMULAR
        # ==================================================

        soma_pares += media_pares

        soma_impares += media_impares

        soma_primos += media_primos

        soma_fibonacci += media_fibonacci

        soma_multiplos3 += media_multiplos3

        soma_moldura += media_moldura

        soma_centro += media_centro

        soma_quantidade_sequencias += (
            media_quantidade_sequencias
        )

        soma_maior_sequencia += (
            media_maior_sequencia
        )

        quantidade_blocos += 1


        inicio += QTD_DIAS


    # ======================================================
    # VALIDAR
    # ======================================================

    if quantidade_blocos == 0:

        raise Exception(
            "Nenhum bloco completo disponível "
            "para análise."
        )


    # ======================================================
    # MÉDIAS GERAIS
    # ======================================================

    media_pares = (

        soma_pares
        /
        quantidade_blocos

    )

    media_impares = (

        soma_impares
        /
        quantidade_blocos

    )

    media_primos = (

        soma_primos
        /
        quantidade_blocos

    )

    media_fibonacci = (

        soma_fibonacci
        /
        quantidade_blocos

    )

    media_multiplos3 = (

        soma_multiplos3
        /
        quantidade_blocos

    )

    media_moldura = (

        soma_moldura
        /
        quantidade_blocos

    )

    media_centro = (

        soma_centro
        /
        quantidade_blocos

    )

    media_quantidade_sequencias = (

        soma_quantidade_sequencias
        /
        quantidade_blocos

    )

    media_maior_sequencia = (

        soma_maior_sequencia
        /
        quantidade_blocos

    )


    # ======================================================
    # PARÂMETROS CALCULADOS
    # ======================================================

    parametros = {

        # ------------------------------------------------------
        # CALCULADOS PELA ANÁLISE
        # ------------------------------------------------------

        "QTD_PARES": round(
            media_pares
        ),

        "QTD_IMPARES": round(
            media_impares
        ),

        "QTD_PRIMOS": round(
            media_primos
        ),

        "QTD_FIBONACCI": round(
            media_fibonacci
        ),

        "QTD_MULTIPLOS3": round(
            media_multiplos3
        ),

        "QTD_MOLDURA": round(
            media_moldura
        ),

        "QTD_CENTRO": round(
            media_centro
        ),

        "MAX_SEQUENCIA": round(
            media_maior_sequencia
        ),

        # ------------------------------------------------------
        # FIXOS
        # ------------------------------------------------------

        "MAX_QTD_SEQUENCIAS":
            MAX_QTD_SEQUENCIAS,

        "TAMANHO_MINIMO_SEQUENCIA":
            TAMANHO_MINIMO_SEQUENCIA,

        "MAX_SEQUENCIA_FIXOS":
            MAX_SEQUENCIA_FIXOS
    }

    # ======================================================
    # RESUMO
    # ======================================================

    print()
    print(
        "=========================================================="
    )
    print(
        "[LOTOFACIL] >>> PARÂMETROS CALCULADOS <<<"
    )
    print(
        "=========================================================="
    )

    for nome, valor in parametros.items():

        print(
            f"{nome}: {valor}"
        )

    print()
    print(
        f"Blocos analisados: {quantidade_blocos}"
    )

    print(
        f"Tamanho dos blocos: {QTD_DIAS}"
    )

    print(
        "=========================================================="
    )


    return parametros


# ==========================================================
# REMOVER CONFIGURAÇÃO ANTERIOR
# ==========================================================

def LimparParametros():

    print()
    print(
        "[LOTOFACIL] >>> REMOVENDO "
        "CONFIGURAÇÃO ANTERIOR <<<"
    )

    parametros_table.delete_item(

        Key={

            "pk": PK,

            "sk": SK

        }

    )

    print(
        "[LOTOFACIL] >>> CONFIGURAÇÃO "
        "ANTERIOR REMOVIDA <<<"
    )


# ==========================================================
# SALVAR NOVA CONFIGURAÇÃO
# ==========================================================

def SalvarParametros(
    parametros
):

    item = {

        "pk": PK,

        "sk": SK,

        **parametros

    }

    parametros_table.put_item(

        Item=item

    )

    print(
        "[LOTOFACIL] >>> NOVA CONFIGURAÇÃO SALVA <<<"
    )


# ==========================================================
# VALIDAR CONFIGURAÇÃO GRAVADA
# ==========================================================

def ValidarParametros(
    parametros
):

    response = parametros_table.get_item(

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
            "Configuração não encontrada "
            "após gravação."
        )


    print()
    print(
        "=========================================================="
    )
    print(
        "[LOTOFACIL] >>> CONFIGURAÇÃO "
        "CONFIRMADA NO DYNAMODB <<<"
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


    for nome, valor_esperado in parametros.items():

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
        "[LOTOFACIL] >>> TODOS OS PARÂMETROS "
        "CONFIRMADOS <<<"
    )
    print(
        "=========================================================="
    )


# ==========================================================
# ATUALIZAR PARÂMETROS
# ==========================================================

def AtualizarParametros():

    # ------------------------------------------------------
    # 1. CARREGAR ESTATÍSTICAS
    # ------------------------------------------------------

    concursos = CarregarConcursos()


    # ------------------------------------------------------
    # 2. CALCULAR PARÂMETROS
    # ------------------------------------------------------

    parametros = AnalisarIndicadores(
        concursos
    )


    # ------------------------------------------------------
    # 3. REMOVER CONFIGURAÇÃO ANTERIOR
    # ------------------------------------------------------

    LimparParametros()


    # ------------------------------------------------------
    # 4. GRAVAR NOVA CONFIGURAÇÃO
    # ------------------------------------------------------

    SalvarParametros(
        parametros
    )


    # ------------------------------------------------------
    # 5. VALIDAR
    # ------------------------------------------------------

    ValidarParametros(
        parametros
    )


    return parametros


# ==========================================================
# LAMBDA
# ==========================================================

def lambda_handler(
    event,
    context
):

    print()
    print(
        "=========================================================="
    )
    print(
        "[LOTOFACIL] >>> ATUALIZAÇÃO DE PARÂMETROS <<<"
    )
    print(
        "=========================================================="
    )

    print(
        f"[LOTOFACIL] QTD_DIAS: {QTD_DIAS}"
    )


    try:

        parametros = AtualizarParametros()


        print()
        print(
            "[LOTOFACIL] >>> CONFIGURAÇÃO "
            "APLICADA COM SUCESSO <<<"
        )


        return {

            "statusCode": 200,

            "body": json.dumps(

                {

                    "mensagem":
                        "Parâmetros atualizados.",

                    "parametros":
                        parametros

                },

                ensure_ascii=False

            )

        }


    except Exception as erro:

        print()
        print(
            f"[LOTOFACIL] >>> ERRO: {erro} <<<"
        )


        return {

            "statusCode": 500,

            "body": json.dumps(

                {

                    "erro":
                        str(erro)

                },

                ensure_ascii=False

            )

        }

