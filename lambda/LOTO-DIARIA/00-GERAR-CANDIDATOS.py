import json
import boto3
import random

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

    itens = response.get(
        "Items",
        []
    )

    while "LastEvaluatedKey" in response:

        response = jogos_table.scan(
            ProjectionExpression="pk, sk",
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )

        itens.extend(
            response.get(
                "Items",
                []
            )
        )

    if not itens:

        print(
            "Tabela jogos_lotofacil já está vazia."
        )

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

    data = agora.strftime(
        "%Y-%m-%d"
    )

    # Os jogos serão destinados ao concurso seguinte
    concurso = (
        resultado["concurso_anterior"] + 1
    )

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

    item = response.get(
        "Item"
    )

    if not item:

        raise Exception(
            "Resultado da Lotofácil não encontrado."
        )

    return item


# ==========================================================
# SEPARAR CONJUNTO A E CONJUNTO B
# ==========================================================

def separar_conjuntos(
    dezenas_embaralhadas
):

    if len(dezenas_embaralhadas) != 15:

        raise Exception(
            "O concurso anterior deve possuir "
            "exatamente 15 dezenas."
        )

    # Primeiras 9 posições após o embaralhamento
    conjunto_a = (
        dezenas_embaralhadas[:TAMANHO_CONJUNTO]
    )

    # Últimas 9 posições após o embaralhamento
    conjunto_b = (
        dezenas_embaralhadas[-TAMANHO_CONJUNTO:]
    )

    return conjunto_a, conjunto_b


# ==========================================================
# MONTAR CONJUNTOS DO CONCURSO ANTERIOR
# ==========================================================

def montar_conjuntos_concurso_anterior():

    resultado_anterior = (
        buscar_resultado_concurso_anterior()
    )

    concurso_anterior = int(
        resultado_anterior["concurso"]
    )

    # ======================================================
    # 15 DEZENAS DO CONCURSO ANTERIOR
    # ======================================================

    dezenas_anteriores = [
        int(numero)
        for numero
        in resultado_anterior["listaDezenas"]
    ]

    if len(dezenas_anteriores) != 15:

        raise Exception(
            "O concurso anterior deve possuir "
            "exatamente 15 dezenas."
        )

    # ======================================================
    # GERADOR ALEATÓRIO DO CONCURSO
    # ======================================================
    #
    # A semente é o próprio concurso anterior.
    #
    # Isso significa:
    #
    # concurso 3790 -> sempre o mesmo embaralhamento
    # concurso 3791 -> outro embaralhamento
    # concurso 3792 -> outro embaralhamento
    #
    # Dessa forma podemos reproduzir a projeção.
    # ======================================================

    gerador = random.Random(
        concurso_anterior
    )


    # ======================================================
    # EMBARALHAR AS 15 SORTEADAS
    # ======================================================

    dezenas_embaralhadas = (
        dezenas_anteriores.copy()
    )

    gerador.shuffle(
        dezenas_embaralhadas
    )


    # ======================================================
    # FORMAR A E B
    # ======================================================

    conjunto_a, conjunto_b = separar_conjuntos(
        dezenas_embaralhadas
    )


    # ======================================================
    # DESCOBRIR AS 10 NÃO SORTEADAS
    # ======================================================

    nao_sorteadas = [
        numero
        for numero in range(1, 26)
        if numero not in dezenas_anteriores
    ]

    if len(nao_sorteadas) != 10:

        raise Exception(
            "Devem existir exatamente "
            "10 dezenas não sorteadas."
        )


    # ======================================================
    # EMBARALHAR AS 10 NÃO SORTEADAS
    # ======================================================

    nao_sorteadas_embaralhadas = (
        nao_sorteadas.copy()
    )

    gerador.shuffle(
        nao_sorteadas_embaralhadas
    )


    # ======================================================
    # FORMAR R E S
    # ======================================================

    # Primeiras 6 posições após o embaralhamento
    conjunto_r = (
        nao_sorteadas_embaralhadas[:6]
    )

    # Últimas 6 posições após o embaralhamento
    conjunto_s = (
        nao_sorteadas_embaralhadas[-6:]
    )


    # ======================================================
    # MONTAR AS 4 COMBINAÇÕES
    # ======================================================
    #
    # IMPORTANTE:
    #
    # Aqui podemos ordenar.
    #
    # A escolha das dezenas JÁ aconteceu.
    # O sorted() daqui para baixo serve somente
    # para apresentar/salvar o cartão organizado.
    # ======================================================

    combinacao_ar = sorted(
        conjunto_a + conjunto_r
    )

    combinacao_as = sorted(
        conjunto_a + conjunto_s
    )

    combinacao_br = sorted(
        conjunto_b + conjunto_r
    )

    combinacao_bs = sorted(
        conjunto_b + conjunto_s
    )


    # ======================================================
    # RETORNO
    # ======================================================

    return {

        "concurso_anterior":
            concurso_anterior,

        # Resultado original
        "dezenas_concurso_anterior":
            dezenas_anteriores,

        # Resultado após embaralhamento
        "dezenas_embaralhadas":
            dezenas_embaralhadas,

        # Não sorteadas originais
        "nao_sorteadas":
            nao_sorteadas,

        # Não sorteadas após embaralhamento
        "nao_sorteadas_embaralhadas":
            nao_sorteadas_embaralhadas,

        # Conjuntos
        "conjunto_a":
            conjunto_a,

        "conjunto_b":
            conjunto_b,

        "conjunto_r":
            conjunto_r,

        "conjunto_s":
            conjunto_s,

        # Combinações finais
        "combinacao_ar":
            combinacao_ar,

        "combinacao_as":
            combinacao_as,

        "combinacao_br":
            combinacao_br,

        "combinacao_bs":
            combinacao_bs
    }


# ==========================================================
# HANDLER
# ==========================================================

def lambda_handler(
    event,
    context
):

    try:

        # --------------------------------------------------
        # Primeiro monta tudo em memória.
        # --------------------------------------------------
        #
        # Se houver qualquer problema com o resultado
        # anterior, a tabela atual NÃO será apagada.
        # --------------------------------------------------

        resultado = (
            montar_conjuntos_concurso_anterior()
        )


        # --------------------------------------------------
        # APAGAR PROJEÇÃO ANTERIOR
        # --------------------------------------------------

        removidos = (
            zerar_tabela_jogos()
        )


        # --------------------------------------------------
        # SALVAR NOVA PROJEÇÃO
        # --------------------------------------------------

        quantidade = (
            salvar_combinacoes(
                resultado
            )
        )


        # --------------------------------------------------
        # RETORNO
        # --------------------------------------------------

        return {
            "statusCode": 200,

            "body": json.dumps({
                "mensagem":
                    "Projeção gerada com sucesso.",

                "jogos_removidos":
                    removidos,

                "jogos_salvos":
                    quantidade,

                "concurso":
                    resultado[
                        "concurso_anterior"
                    ] + 1
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

    print()
    print("========================================")
    print(" GERAR CANDIDATOS - EXECUÇÃO LOCAL")
    print("========================================")

    # Primeiro montamos para poder visualizar
    # exatamente como os conjuntos foram formados.

    resultado = (
        montar_conjuntos_concurso_anterior()
    )

    print()
    print(
        "Concurso anterior:",
        resultado["concurso_anterior"]
    )

    print()
    print(
        "Resultado anterior:",
        resultado["dezenas_concurso_anterior"]
    )

    print()
    print(
        "Sorteadas embaralhadas:",
        resultado["dezenas_embaralhadas"]
    )

    print()
    print(
        "A:",
        resultado["conjunto_a"]
    )

    print(
        "B:",
        resultado["conjunto_b"]
    )

    print()
    print(
        "Não sorteadas:",
        resultado["nao_sorteadas"]
    )

    print()
    print(
        "Não sorteadas embaralhadas:",
        resultado["nao_sorteadas_embaralhadas"]
    )

    print()
    print(
        "R:",
        resultado["conjunto_r"]
    )

    print(
        "S:",
        resultado["conjunto_s"]
    )

    print()
    print("========================================")
    print(" COMBINAÇÕES FINAIS")
    print("========================================")

    print(
        "AR:",
        resultado["combinacao_ar"]
    )

    print(
        "AS:",
        resultado["combinacao_as"]
    )

    print(
        "BR:",
        resultado["combinacao_br"]
    )

    print(
        "BS:",
        resultado["combinacao_bs"]
    )

    print()
    print("========================================")
    print(" SALVANDO PROJEÇÃO")
    print("========================================")

    resposta = lambda_handler(
        {},
        None
    )

    print()
    print(
        f"Status: {resposta['statusCode']}"
    )

    print(
        f"Resposta: {resposta['body']}"
    )

    print("========================================")
    print()