import json
import boto3
from datetime import datetime
from zoneinfo import ZoneInfo


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================
REGION = "ap-east-1"
TABLE_RESULTADO = "resultado_lotofacil"
TABLE_JOGOS = "jogos_lotofacil"
TAMANHO_CONJUNTO = 9
ENGINE = "DESDOBRAMENTO-SIMPLES"
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
# ZERAR TABELA DE JOGOS
# ==========================================================

def zerar_tabela_jogos():

    response = jogos_table.scan(
        ProjectionExpression="pk, sk"
    )

    itens = response.get("Items", [])

    while "LastEvaluatedKey" in response:

        response = jogos_table.scan(
            ProjectionExpression="pk, sk",
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )

        itens.extend(
            response.get("Items", [])
        )

    if not itens:
        print("Tabela jogos_lotofacil já está vazia.")
        return 0

    with jogos_table.batch_writer() as batch:

        for item in itens:

            batch.delete_item(
                Key={
                    "pk": item["pk"],
                    "sk": item["sk"]
                }
            )

    print(
        f"{len(itens)} jogo(s) removido(s) "
        "de jogos_lotofacil."
    )

    return len(itens)


# ==========================================================
# SALVAR COMBINAÇÕES NA TABELA DE JOGOS
# ==========================================================

def salvar_combinacoes(resultado):

    agora = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    )

    data = agora.strftime("%Y-%m-%d")

    # Os jogos serão destinados ao concurso seguinte
    concurso = resultado["concurso_anterior"] + 1

    combinacoes = {
        "AR": resultado["combinacao_ar"],
        "AS": resultado["combinacao_as"],
        "BR": resultado["combinacao_br"],
        "BS": resultado["combinacao_bs"]
    }

    for nome, dezenas in combinacoes.items():

        horario = datetime.now(
            ZoneInfo("America/Sao_Paulo")
        ).isoformat()

        item = {
            "pk": "JOGO",
            "sk": f"{horario}#{nome}",
            "data": data,
            "concurso": concurso,
            "engine": ENGINE,
            "tipo_combinacao": nome,
            "jogo": dezenas
        }

        jogos_table.put_item(
            Item=item
        )

    return len(combinacoes)


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

    item = response.get("Item")

    if not item:
        raise Exception(
            "Resultado da Lotofácil não encontrado."
        )

    return item


# ==========================================================
# SEPARAR CONJUNTO A E CONJUNTO B
# ==========================================================

def separar_conjuntos(dezenas_anteriores):

    if len(dezenas_anteriores) != 15:
        raise Exception(
            "O concurso anterior deve possuir exatamente 15 dezenas."
        )

    # Primeiras 9 dezenas da esquerda para a direita
    conjunto_a = dezenas_anteriores[:TAMANHO_CONJUNTO]

    # Últimas 9 dezenas
    conjunto_b = dezenas_anteriores[-TAMANHO_CONJUNTO:]

    return conjunto_a, conjunto_b


# ==========================================================
# MONTAR CONJUNTOS DO CONCURSO ANTERIOR
# ==========================================================

def montar_conjuntos_concurso_anterior():

    resultado_anterior = buscar_resultado_concurso_anterior()

    # 15 dezenas sorteadas no concurso anterior
    dezenas_anteriores = sorted([
        int(numero)
        for numero in resultado_anterior["listaDezenas"]
    ])

    # Conjuntos posicionais A e B
    conjunto_a, conjunto_b = separar_conjuntos(
        dezenas_anteriores
    )

    # 10 dezenas que NÃO foram sorteadas
    nao_sorteadas = [
        numero
        for numero in range(1, 26)
        if numero not in dezenas_anteriores
    ]

    # Primeiras 6 dezenas das não sorteadas
    conjunto_r = nao_sorteadas[:6]

    # Últimas 6 dezenas das não sorteadas
    conjunto_s = nao_sorteadas[-6:]   

    # ==========================================================
    # MONTAR AS 4 COMBINAÇÕES
    # ==========================================================

    combinacao_ar = sorted(conjunto_a + conjunto_r)
    combinacao_as = sorted(conjunto_a + conjunto_s)
    combinacao_br = sorted(conjunto_b + conjunto_r)
    combinacao_bs = sorted(conjunto_b + conjunto_s)     

    return {
        "concurso_anterior": int(
            resultado_anterior["concurso"]
        ),
        "dezenas_concurso_anterior": dezenas_anteriores,
        "nao_sorteadas": nao_sorteadas,

        "conjunto_a": conjunto_a,
        "conjunto_b": conjunto_b,
        "conjunto_r": conjunto_r,
        "conjunto_s": conjunto_s,

        "combinacao_ar": combinacao_ar,
        "combinacao_as": combinacao_as,
        "combinacao_br": combinacao_br,
        "combinacao_bs": combinacao_bs
    }


# ==========================================================
# HANDLER
# ==========================================================

def lambda_handler(event, context):

    try:

        # Primeiro monta tudo em memória.
        # Se houver problema no resultado anterior,
        # não apagamos os jogos existentes.
        resultado = montar_conjuntos_concurso_anterior()

        # A nova projeção sempre substitui a anterior.
        removidos = zerar_tabela_jogos()

        quantidade = salvar_combinacoes(
            resultado
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "mensagem": "Projeção gerada com sucesso.",
                "jogos_removidos": removidos,
                "jogos_salvos": quantidade,
                "concurso": resultado["concurso_anterior"] + 1
            })
        }

    except Exception as erro:

        return {
            "statusCode": 500,
            "body": json.dumps({
                "erro": str(erro)
            })
        }

# ==========================================================
# TESTE LOCAL
# ==========================================================

if __name__ == "__main__":

    print("\n========================================")
    print(" GERAR CANDIDATOS - EXECUÇÃO LOCAL")
    print("========================================")

    resposta = lambda_handler({}, None)

    print()
    print(f"Status: {resposta['statusCode']}")
    print(f"Resposta: {resposta['body']}")

    print("========================================\n")    