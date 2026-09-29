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

ENGINE = "DESDOBRAMENTO-6"


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
# MONTAR OS 6 JOGOS
# ==========================================================

def montar_jogos():

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
    # Para o mesmo concurso teremos sempre
    # exatamente a mesma projeção.
    #
    # IMPORTANTE:
    #
    # NÃO ORDENAR AS DEZENAS ANTES DOS EMBARALHAMENTOS.
    # ======================================================

    gerador = random.Random(
        concurso_anterior
    )


    # ======================================================
    # EMBARALHAR AS 15 DEZENAS DO CONCURSO ANTERIOR
    # ======================================================

    dezenas_embaralhadas = (
        dezenas_anteriores.copy()
    )

    gerador.shuffle(
        dezenas_embaralhadas
    )


    # ======================================================
    # FORMAR 5 GRUPOS DE 2 DEZENAS
    # ======================================================
    #
    # Utilizamos as primeiras 10 posições:
    #
    # G1 = posições 1 e 2
    # G2 = posições 3 e 4
    # G3 = posições 5 e 6
    # G4 = posições 7 e 8
    # G5 = posições 9 e 10
    #
    # NÃO ORDENAR.
    # ======================================================

    g1 = (
        dezenas_embaralhadas[0:2]
    )

    g2 = (
        dezenas_embaralhadas[2:4]
    )

    g3 = (
        dezenas_embaralhadas[4:6]
    )

    g4 = (
        dezenas_embaralhadas[6:8]
    )

    g5 = (
        dezenas_embaralhadas[8:10]
    )


    # ======================================================
    # 5 DEZENAS RESTANTES DO CONCURSO ANTERIOR
    # ======================================================
    #
    # Estas cinco dezenas não entram nos jogos.
    # São mantidas apenas para conferência.
    # ======================================================

    restantes = (
        dezenas_embaralhadas[10:15]
    )


    # ======================================================
    # MONTAR OS 5 JOGOS PARCIAIS
    # ======================================================
    #
    # Cada grupo possui 2 dezenas.
    #
    # Cada jogo utiliza 4 grupos:
    #
    # 4 x 2 = 8 dezenas
    #
    # JOGO 1 = G1 + G2 + G3 + G4
    # JOGO 2 = G1 + G2 + G3 + G5
    # JOGO 3 = G1 + G2 + G4 + G5
    # JOGO 4 = G1 + G3 + G4 + G5
    # JOGO 5 = G2 + G3 + G4 + G5
    #
    # NÃO ORDENAR.
    # ======================================================

    jogo_1_parcial = (
        g1 +
        g2 +
        g3 +
        g4
    )

    jogo_2_parcial = (
        g1 +
        g2 +
        g3 +
        g5
    )

    jogo_3_parcial = (
        g1 +
        g2 +
        g4 +
        g5
    )

    jogo_4_parcial = (
        g1 +
        g3 +
        g4 +
        g5
    )

    jogo_5_parcial = (
        g2 +
        g3 +
        g4 +
        g5
    )


    # ======================================================
    # VALIDAR JOGOS PARCIAIS
    # ======================================================

    jogos_parciais = [
        jogo_1_parcial,
        jogo_2_parcial,
        jogo_3_parcial,
        jogo_4_parcial,
        jogo_5_parcial
    ]

    for indice, jogo in enumerate(
        jogos_parciais,
        start=1
    ):

        if len(jogo) != 8:

            raise Exception(
                f"Jogo parcial {indice} deve possuir "
                "exatamente 8 dezenas."
            )

        if len(set(jogo)) != 8:

            raise Exception(
                f"Jogo parcial {indice} possui "
                "dezenas repetidas."
            )


    # ======================================================
    # DESCOBRIR AS 10 DEZENAS NÃO SORTEADAS
    # ======================================================
    #
    # A comparação é feita contra as 15 dezenas
    # ORIGINAIS do concurso anterior.
    #
    # NÃO ORDENAR.
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
    #
    # ATENÇÃO:
    #
    # Utilizamos o MESMO objeto "gerador".
    #
    # Portanto o estado do gerador já foi alterado
    # pelo shuffle das 15 dezenas anteriores.
    #
    # NÃO CRIAR OUTRO random.Random().
    # NÃO MOVER ESTE SHUFFLE.
    # NÃO ORDENAR ANTES DESTE SHUFFLE.
    # ======================================================

    nao_sorteadas_embaralhadas = (
        nao_sorteadas.copy()
    )

    gerador.shuffle(
        nao_sorteadas_embaralhadas
    )


    # ======================================================
    # COMPLEMENTOS DE 7 DEZENAS
    # ======================================================
    #
    # Considerando:
    #
    # N1 N2 N3 N4 N5 N6 N7 N8 N9 N10
    #
    # C1 = N1 N2 N3 N4 N5 N6 N7
    # C2 = N2 N3 N4 N5 N6 N7 N8
    # C3 = N3 N4 N5 N6 N7 N8 N9
    # C4 = N4 N5 N6 N7 N8 N9 N10
    # C5 = N5 N6 N7 N8 N9 N10 N1
    #
    # NÃO ORDENAR.
    # ======================================================

    complemento_1 = (
        nao_sorteadas_embaralhadas[0:7]
    )

    complemento_2 = (
        nao_sorteadas_embaralhadas[1:8]
    )

    complemento_3 = (
        nao_sorteadas_embaralhadas[2:9]
    )

    complemento_4 = (
        nao_sorteadas_embaralhadas[3:10]
    )

    complemento_5 = (
        nao_sorteadas_embaralhadas[4:10]
        +
        nao_sorteadas_embaralhadas[0:1]
    )


    # ======================================================
    # MONTAR OS 5 JOGOS COMPLETOS
    # ======================================================
    #
    # Cada cartão:
    #
    # 8 dezenas que estavam no concurso anterior
    # +
    # 7 dezenas que NÃO estavam no concurso anterior
    # =
    # 15 dezenas
    #
    # AINDA NÃO ORDENAR.
    # ======================================================

    jogo_1 = (
        jogo_1_parcial +
        complemento_1
    )

    jogo_2 = (
        jogo_2_parcial +
        complemento_2
    )

    jogo_3 = (
        jogo_3_parcial +
        complemento_3
    )

    jogo_4 = (
        jogo_4_parcial +
        complemento_4
    )

    jogo_5 = (
        jogo_5_parcial +
        complemento_5
    )

    jogo_6 = (
        restantes +
        nao_sorteadas_embaralhadas
    )

    # ======================================================
    # VALIDAR OS 6 JOGOS COMPLETOS
    # ======================================================

    jogos = [
        jogo_1,
        jogo_2,
        jogo_3,
        jogo_4,
        jogo_5,
        jogo_6
    ]

    for indice, jogo in enumerate(
        jogos,
        start=1
    ):

        if len(jogo) != 15:

            raise Exception(
                f"Jogo {indice} deve possuir "
                "exatamente 15 dezenas."
            )

        if len(set(jogo)) != 15:

            raise Exception(
                f"Jogo {indice} possui "
                "dezenas repetidas."
            )


    # ======================================================
    # ORDENAR SOMENTE AGORA
    # ======================================================
    #
    # PONTO CRÍTICO DA LÓGICA.
    #
    # TODAS AS ESCOLHAS JÁ ACONTECERAM:
    #
    # - shuffle das 15 anteriores
    # - criação dos grupos
    # - criação dos jogos parciais
    # - descoberta das 10 não sorteadas
    # - shuffle das 10 não sorteadas
    # - escolha dos complementos
    # - montagem dos jogos completos
    #
    # Portanto, daqui para baixo, sorted()
    # serve SOMENTE para apresentação e gravação
    # organizada dos cartões.
    #
    # NÃO MOVER ESTE BLOCO PARA CIMA.
    # ======================================================

    jogo_1_final = sorted(
        jogo_1
    )

    jogo_2_final = sorted(
        jogo_2
    )

    jogo_3_final = sorted(
        jogo_3
    )

    jogo_4_final = sorted(
        jogo_4
    )

    jogo_5_final = sorted(
        jogo_5
    )

    jogo_6_final = sorted(
        jogo_6
    )

    # ======================================================
    # RETORNO
    # ======================================================

    return {

        "concurso_anterior":
            concurso_anterior,

        "dezenas_concurso_anterior":
            dezenas_anteriores,

        "dezenas_embaralhadas":
            dezenas_embaralhadas,

        "g1":
            g1,

        "g2":
            g2,

        "g3":
            g3,

        "g4":
            g4,

        "g5":
            g5,

        "restantes":
            restantes,

        "jogo_1_parcial":
            jogo_1_parcial,

        "jogo_2_parcial":
            jogo_2_parcial,

        "jogo_3_parcial":
            jogo_3_parcial,

        "jogo_4_parcial":
            jogo_4_parcial,

        "jogo_5_parcial":
            jogo_5_parcial,

        "nao_sorteadas":
            nao_sorteadas,

        "nao_sorteadas_embaralhadas":
            nao_sorteadas_embaralhadas,

        "complemento_1":
            complemento_1,

        "complemento_2":
            complemento_2,

        "complemento_3":
            complemento_3,

        "complemento_4":
            complemento_4,

        "complemento_5":
            complemento_5,

        "jogo_1":
            jogo_1_final,

        "jogo_2":
            jogo_2_final,

        "jogo_3":
            jogo_3_final,

        "jogo_4":
            jogo_4_final,

        "jogo_5":
            jogo_5_final,

        "jogo_6":
            jogo_6_final            
    }


# ==========================================================
# SALVAR OS 6 JOGOS
# ==========================================================

def salvar_jogos(
    resultado
):

    agora = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    )

    data = agora.strftime(
        "%Y-%m-%d"
    )

    # Jogos destinados ao próximo concurso
    concurso = (
        resultado["concurso_anterior"] + 1
    )

    jogos = {
        "J1": resultado["jogo_1"],
        "J2": resultado["jogo_2"],
        "J3": resultado["jogo_3"],
        "J4": resultado["jogo_4"],
        "J5": resultado["jogo_5"],
        "J6": resultado["jogo_6"],

    }

    for nome, dezenas in jogos.items():

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

    return len(jogos)


# ==========================================================
# HANDLER
# ==========================================================

def lambda_handler(
    event,
    context
):

    try:

        # --------------------------------------------------
        # PRIMEIRO MONTAR TUDO EM MEMÓRIA
        # --------------------------------------------------
        #
        # Se houver qualquer erro durante a geração,
        # a tabela atual NÃO será apagada.
        # --------------------------------------------------

        resultado = (
            montar_jogos()
        )


        # --------------------------------------------------
        # VISUALIZAÇÃO DA PROJEÇÃO
        # --------------------------------------------------

        print()
        print("========================================")
        print(" CONCURSO ANTERIOR")
        print("========================================")

        print(
            "Concurso:",
            resultado["concurso_anterior"]
        )

        print(
            "Dezenas:",
            resultado["dezenas_concurso_anterior"]
        )


        print()
        print("========================================")
        print(" DEZENAS EMBARALHADAS")
        print("========================================")

        print(
            resultado["dezenas_embaralhadas"]
        )


        print()
        print("========================================")
        print(" GRUPOS DE 2 DEZENAS")
        print("========================================")

        print(
            "G1:",
            resultado["g1"]
        )

        print(
            "G2:",
            resultado["g2"]
        )

        print(
            "G3:",
            resultado["g3"]
        )

        print(
            "G4:",
            resultado["g4"]
        )

        print(
            "G5:",
            resultado["g5"]
        )
    
        print(
            "Restantes:",
            resultado["restantes"]
        )


        print()
        print("========================================")
        print(" 5 JOGOS PARCIAIS - 8 DEZENAS")
        print("========================================")

        print(
            "JOGO 1:",
            resultado["jogo_1_parcial"]
        )

        print(
            "JOGO 2:",
            resultado["jogo_2_parcial"]
        )

        print(
            "JOGO 3:",
            resultado["jogo_3_parcial"]
        )

        print(
            "JOGO 4:",
            resultado["jogo_4_parcial"]
        )

        print(
            "JOGO 5:",
            resultado["jogo_5_parcial"]
        )

        print()
        print("========================================")
        print(" 10 NÃO SORTEADAS")
        print("========================================")

        print(
            "Originais:",
            resultado["nao_sorteadas"]
        )

        print(
            "Embaralhadas:",
            resultado["nao_sorteadas_embaralhadas"]
        )


        print()
        print("========================================")
        print(" COMPLEMENTOS - 7 DEZENAS")
        print("========================================")

        print(
            "C1:",
            resultado["complemento_1"]
        )

        print(
            "C2:",
            resultado["complemento_2"]
        )

        print(
            "C3:",
            resultado["complemento_3"]
        )

        print(
            "C4:",
            resultado["complemento_4"]
        )

        print(
            "C5:",
            resultado["complemento_5"]
        )


        print()
        print("========================================")
        print(" 6 JOGOS FINAIS - 15 DEZENAS")
        print("========================================")

        print(
            "JOGO 1:",
            resultado["jogo_1"]
        )

        print(
            "JOGO 2:",
            resultado["jogo_2"]
        )

        print(
            "JOGO 3:",
            resultado["jogo_3"]
        )

        print(
            "JOGO 4:",
            resultado["jogo_4"]
        )

        print(
            "JOGO 5:",
            resultado["jogo_5"]
        )

        print(
            "JOGO 6:",
            resultado["jogo_6"]
        )        

        print("========================================")


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
            salvar_jogos(
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
                    "Projeção de 6 jogos gerada "
                    "com sucesso.",

                "jogos_removidos":
                    removidos,

                "jogos_salvos":
                    quantidade,

                "concurso":
                    resultado[
                        "concurso_anterior"
                    ] + 1,

                "engine":
                    ENGINE
            })
        }


    except Exception as erro:

        print()
        print(
            "Erro:",
            str(erro)
        )

        return {
            "statusCode": 500,

            "body": json.dumps({
                "erro": str(erro)
            })
        }


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print()
    print("========================================")
    print(" GERAR CANDIDATOS - EXECUÇÃO LOCAL")
    print("========================================")

    resposta = lambda_handler(
        {},
        None
    )

    print()
    print(
        "Status:",
        resposta["statusCode"]
    )

    print(
        "Resposta:",
        resposta["body"]
    )

    print("========================================")
    print()