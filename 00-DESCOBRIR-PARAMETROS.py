import boto3


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

REGION = "ap-east-1"

TABLE_NAME = "estatistica_concurso"

# INFORME AQUI O NUMERO DE DIAS A ANALISAR....
# ==========================================================
QTD_DIAS = 10
# ==========================================================


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
# CARREGAR CONCURSOS
# ==========================================================

def carregar_concursos():

    response = table.scan()

    itens = response.get(
        "Items",
        []
    )

    while "LastEvaluatedKey" in response:

        response = table.scan(
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

def calcular_media(grupo, campo):

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
# ANÁLISE
# ==========================================================

def analisar_indicadores(concursos):

    # ------------------------------------------------------
    # MAIS RECENTE → MAIS ANTIGO
    # ------------------------------------------------------

    concursos = sorted(
        concursos,
        key=lambda x: int(x["concurso"]),
        reverse=True
    )

    print(
        f"Concursos carregados: {len(concursos)}"
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

    # ------------------------------------------------------
    # BLOCOS DE 10
    # ------------------------------------------------------

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

        media_pares = calcular_media(
            grupo,
            "quantidade_pares"
        )

        media_impares = calcular_media(
            grupo,
            "quantidade_impares"
        )

        media_primos = calcular_media(
            grupo,
            "quantidade_primos"
        )

        media_fibonacci = calcular_media(
            grupo,
            "quantidade_fibonacci"
        )

        media_multiplos3 = calcular_media(
            grupo,
            "quantidade_multiplos3"
        )

        media_moldura = calcular_media(
            grupo,
            "quantidade_moldura"
        )

        media_centro = calcular_media(
            grupo,
            "quantidade_centro"
        )

        # ==================================================
        # SEQUÊNCIAS
        # ==================================================
        #
        # Somamos as ocorrências de sequência de tamanho
        # 2 até 9 para cada concurso.
        #
        # Exemplo:
        #
        # Seq2 = 4
        # Seq3 = 2
        # Seq4 = 1
        #
        # Total de sequências = 7
        #
        # ==================================================

        totais_sequencias = []

        for item in grupo:

            total = 0

            for tamanho in range(2, 10):

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
                sum(totais_sequencias)
                /
                len(totais_sequencias)
            )

        else:

            media_quantidade_sequencias = 0

        # --------------------------------------------------
        # MAIOR SEQUÊNCIA
        # --------------------------------------------------

        media_maior_sequencia = calcular_media(
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

        print(
            "Nenhum bloco completo disponível."
        )

        return

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
    # RESULTADO FINAL
    # ======================================================

    QTD_PARES = round(
        media_pares
    )

    QTD_IMPARES = round(
        media_impares
    )

    QTD_PRIMOS = round(
        media_primos
    )

    QTD_FIBONACCI = round(
        media_fibonacci
    )

    QTD_MULTIPLOS3 = round(
        media_multiplos3
    )

    QTD_MOLDURA = round(
        media_moldura
    )

    QTD_CENTRO = round(
        media_centro
    )

    MAX_QTD_SEQUENCIAS = round(
        media_quantidade_sequencias
    )

    MAX_SEQUENCIA = round(
        media_maior_sequencia
    )

    # ------------------------------------------------------
    # PARÂMETRO FIXO DA ANÁLISE
    # ------------------------------------------------------

    TAMANHO_MINIMO_SEQUENCIA = 3

    # ======================================================
    # RESUMO
    # ======================================================

    print()
    print("-" * 180)
    print("RESUMO")
    print("-" * 180)

    print(
        f"QTD_PARES:                     {QTD_PARES}"
    )

    print(
        f"QTD_IMPARES:                   {QTD_IMPARES}"
    )

    print(
        f"QTD_PRIMOS:                    {QTD_PRIMOS}"
    )

    print(
        f"QTD_FIBONACCI:                 {QTD_FIBONACCI}"
    )

    print(
        f"QTD_MULTIPLOS3:                {QTD_MULTIPLOS3}"
    )

    print(
        f"QTD_MOLDURA:                   {QTD_MOLDURA}"
    )

    print(
        f"QTD_CENTRO:                    {QTD_CENTRO}"
    )

    print(
        f"MAX_SEQUENCIA:                 {MAX_SEQUENCIA}"
    )

    print(
        f"TAMANHO_MINIMO_SEQUENCIA:      {TAMANHO_MINIMO_SEQUENCIA}"
    )


# ==========================================================
# EXECUÇÃO
# ==========================================================

concursos = carregar_concursos()

analisar_indicadores(
    concursos
)

