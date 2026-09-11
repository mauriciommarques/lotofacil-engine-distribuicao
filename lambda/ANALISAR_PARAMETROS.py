# ============================================================
# LOTOFÁCIL - ANALISADOR DO EXPERIMENTO
# ============================================================
#
# OBJETIVO:
#   Buscar os concursos históricos no DynamoDB e descobrir
#   os parâmetros pela MODA para diferentes janelas:
#
#       50 concursos
#       40 concursos
#       30 concursos
#       20 concursos
#
#   O resultado será impresso na tela.
#
# CORTE DO EXPERIMENTO:
#       Concurso 3779
#       Data 03/09/2026
#
# IMPORTANTE:
#   Este programa é SOMENTE LEITURA.
#   NÃO altera parametrossistema.
#   NÃO altera estatistica_concurso.
#   NÃO gera jogos.
#
# ============================================================

from collections import Counter
from decimal import Decimal
import boto3


# ============================================================
# ====================== CONFIGURAÇÃO ========================
# ============================================================

REGION = "ap-east-1"

TABLE_ESTATISTICA = "estatistica_concurso"

PK = "LOTOFACIL"

# >>> CONCURSO DE CORTE DO EXPERIMENTO <<<
CONCURSO_CORTE = 3779

# >>> TAMANHOS DAS JANELAS QUE QUEREMOS TESTAR <<<
JANELAS = [50, 40, 30, 20]


# ============================================================
# ======================== CAMPOS ============================
# ============================================================

CAMPOS = [
    "quantidade_pares",
    "quantidade_impares",
    "quantidade_primos",
    "quantidade_fibonacci",
    "quantidade_multiplos3",
    "quantidade_moldura",
    "quantidade_centro",
    "maior_sequencia",
]


# ============================================================
# ======================= DYNAMODB ===========================
# ============================================================

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION
)

table = dynamodb.Table(
    TABLE_ESTATISTICA
)


# ============================================================
# ===================== CONVERSÃO =============================
# ============================================================

def numero(valor):

    if isinstance(valor, Decimal):

        if valor % 1 == 0:
            return int(valor)

        return float(valor)

    return int(valor)


# ============================================================
# ======================= BUSCAR DADOS =======================
# ============================================================

def buscar_concursos():

    itens = []

    scan_kwargs = {
        "FilterExpression": "pk = :pk",
        "ExpressionAttributeValues": {
            ":pk": PK
        }
    }

    while True:

        resposta = table.scan(
            **scan_kwargs
        )

        itens.extend(
            resposta.get("Items", [])
        )

        ultima_chave = resposta.get(
            "LastEvaluatedKey"
        )

        if not ultima_chave:
            break

        scan_kwargs["ExclusiveStartKey"] = ultima_chave


    # Mantém somente concursos até o corte.
    itens = [
        item
        for item in itens
        if int(item["concurso"]) <= CONCURSO_CORTE
    ]


    # Ordena do mais antigo para o mais recente.
    itens.sort(
        key=lambda item: int(item["concurso"])
    )


    return itens


# ============================================================
# ======================= MODA ===============================
# ============================================================

def calcular_moda(valores):

    contador = Counter(
        numero(valor)
        for valor in valores
    )

    maior_frequencia = max(
        contador.values()
    )

    modas = sorted(
        valor
        for valor, frequencia
        in contador.items()
        if frequencia == maior_frequencia
    )

    # Se houver empate, escolhemos o valor mais próximo
    # da média da própria janela.
    media = sum(valores) / len(valores)

    recomendada = min(
        modas,
        key=lambda valor: (
            abs(valor - media),
            valor
        )
    )

    return recomendada, modas, contador


# ============================================================
# ===================== ANALISAR JANELA ======================
# ============================================================

def analisar_janela(itens):

    resultado = {}

    for campo in CAMPOS:

        valores = [
            numero(item[campo])
            for item in itens
        ]

        recomendada, modas, contador = calcular_moda(
            valores
        )

        resultado[campo] = {
            "valor": recomendada,
            "modas": modas,
            "frequencias": dict(
                sorted(contador.items())
            )
        }

    return resultado


# ============================================================
# ======================== PRINT ==============================
# ============================================================

def imprimir_resultado(tamanho, itens, resultado):

    primeiro = int(
        itens[0]["concurso"]
    )

    ultimo = int(
        itens[-1]["concurso"]
    )

    print()
    print("=" * 75)
    print(
        f"JANELA DE {tamanho} CONCURSOS"
    )
    print("=" * 75)

    print(
        f"Concursos analisados : {primeiro} -> {ultimo}"
    )

    print()

    print(
        f"{'PARAMETRO':<28}"
        f"{'MODA':>8}"
        f"{'FREQUÊNCIA':>12}"
        f"  MODAS"
    )

    print("-" * 75)

    nomes = {
        "quantidade_pares": "QTD_PARES",
        "quantidade_impares": "QTD_IMPARES",
        "quantidade_primos": "QTD_PRIMOS",
        "quantidade_fibonacci": "QTD_FIBONACCI",
        "quantidade_multiplos3": "QTD_MULTIPLOS3",
        "quantidade_moldura": "QTD_MOLDURA",
        "quantidade_centro": "QTD_CENTRO",
        "maior_sequencia": "MAX_SEQUENCIA",
    }

    for campo in CAMPOS:

        dados = resultado[campo]

        valor = dados["valor"]

        frequencia = dados["frequencias"][valor]

        modas = dados["modas"]

        print(
            f"{nomes[campo]:<28}"
            f"{valor:>8}"
            f"{frequencia:>12}"
            f"  {modas}"
        )


    print()
    print(">>> CONFIGURAÇÃO PARA COPIAR AO parametrossistema")
    print()

    print(
        f"QTD_PARES         = "
        f"{resultado['quantidade_pares']['valor']}"
    )

    print(
        f"QTD_IMPARES       = "
        f"{resultado['quantidade_impares']['valor']}"
    )

    print(
        f"QTD_PRIMOS        = "
        f"{resultado['quantidade_primos']['valor']}"
    )

    print(
        f"QTD_FIBONACCI     = "
        f"{resultado['quantidade_fibonacci']['valor']}"
    )

    print(
        f"QTD_MULTIPLOS3    = "
        f"{resultado['quantidade_multiplos3']['valor']}"
    )

    print(
        f"QTD_MOLDURA       = "
        f"{resultado['quantidade_moldura']['valor']}"
    )

    print(
        f"QTD_CENTRO        = "
        f"{resultado['quantidade_centro']['valor']}"
    )

    print(
        f"MAX_SEQUENCIA     = "
        f"{resultado['maior_sequencia']['valor']}"
    )


# ============================================================
# ========================== MAIN =============================
# ============================================================

def main():

    print()
    print("=" * 75)
    print("       LOTOFÁCIL - EXPERIMENTO DE JANELAS")
    print("=" * 75)

    print()
    print(
        f"Corte do modelo : concurso {CONCURSO_CORTE}"
    )

    print(
        "Data do corte   : 03/09/2026"
    )

    print()
    print("Buscando estatísticas no DynamoDB...")

    itens = buscar_concursos()

    print(
        f"Registros encontrados até o corte: {len(itens)}"
    )

    if not itens:
        raise RuntimeError(
            "Nenhum concurso encontrado até o concurso de corte."
        )


    ultimo = int(
        itens[-1]["concurso"]
    )

    print(
        f"Concurso mais recente considerado: {ultimo}"
    )


    for tamanho in JANELAS:

        if len(itens) < tamanho:

            print()
            print(
                f"Não há {tamanho} concursos disponíveis."
            )

            continue


        janela = itens[-tamanho:]

        resultado = analisar_janela(
            janela
        )

        imprimir_resultado(
            tamanho,
            janela,
            resultado
        )


    print()
    print("=" * 75)
    print("FIM DA ANÁLISE")
    print("=" * 75)

    print()
    print(
        "ATENÇÃO: nenhum parâmetro foi alterado."
    )

    print(
        "Os valores acima são apenas sugestões para o experimento."
    )

    print()


if __name__ == "__main__":
    main()
