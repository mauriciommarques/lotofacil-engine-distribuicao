import json
import boto3

REGION = "ap-east-1"
TABLE_ESTATISTICA = "estatistica_concurso"
TABLE_PARAMETROS = "parametrossistema"

PK = "LOTOFACIL"
SK = "PARAMETROS"

QTD_DIAS = 10

MAX_QTD_SEQUENCIAS = 3
TAMANHO_MINIMO_SEQUENCIA = 3

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


def AnalisarIndicadores(
    concursos
):

    concursos = sorted(
        concursos,
        key=lambda x: int(
            x["concurso"]
        ),
        reverse=True
    )

    concurso_referencia = int(
        concursos[0]["concurso"]
    )

    data_referencia = concursos[0].get(
        "dataApuracao"
    )

    print(
        f"[LOTOFACIL] Concursos carregados: "
        f"{len(concursos)}"
    )

    soma_pares = 0
    soma_impares = 0
    soma_primos = 0
    soma_fibonacci = 0
    soma_multiplos3 = 0
    soma_moldura = 0
    soma_centro = 0
    soma_quantidade_sequencias = 0
    
    quantidade_blocos = 0

    inicio = 0

    while (
        inicio + QTD_DIAS
        <= len(concursos)
    ):

        grupo = concursos[
            inicio:
            inicio + QTD_DIAS
        ]

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

        quantidade_blocos += 1

        inicio += QTD_DIAS

    if quantidade_blocos == 0:

        raise Exception(
            "Nenhum bloco completo disponível "
            "para análise."
        )

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

    parametros = {

        "concurso_atualizado":
            concurso_referencia,

        "dataApuracao":
            data_referencia,

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

        "MAX_QTD_SEQUENCIAS":
            MAX_QTD_SEQUENCIAS,

        "TAMANHO_MINIMO_SEQUENCIA":
            TAMANHO_MINIMO_SEQUENCIA

    }

    print()
    print(
        "=========================================================="
    )

    print(
        "[LOTOFACIL] >>> PARÂMETROS CALCULADOS <<<"
    )

    print(
        f"Concurso de referência: "
        f"{concurso_referencia}"
    )

    print(
        f"Data de apuração: "
        f"{data_referencia}"
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
        f"Blocos analisados: "
        f"{quantidade_blocos}"
    )

    print(
        f"Tamanho dos blocos: "
        f"{QTD_DIAS}"
    )

    print(
        "=========================================================="
    )

    return parametros

def LimparParametros():

    print("[LOTOFACIL] APAGANDO ITEM ANTIGO")

    parametros_table.delete_item(
        Key={
            "pk": PK,
            "sk": SK
        }
    )

    response = parametros_table.get_item(
        Key={
            "pk": PK,
            "sk": SK
        }
    )

    if "Item" in response:
        raise Exception(
            "ERRO: item antigo ainda existe após delete_item"
        )

    print("[LOTOFACIL] ITEM ANTIGO APAGADO E CONFIRMADO")

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
        "[LOTOFACIL] >>> NOVA CONFIGURAÇÃO "
        "SALVA <<<"
    )


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


def AtualizarParametros():

    concursos = CarregarConcursos()

    parametros = AnalisarIndicadores(
        concursos
    )

    LimparParametros()

    SalvarParametros(
        parametros
    )

    ValidarParametros(
        parametros
    )

    return parametros


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
        f"[LOTOFACIL] QTD_DIAS: "
        f"{QTD_DIAS}"
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
            f"[LOTOFACIL] >>> ERRO: "
            f"{erro} <<<"
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