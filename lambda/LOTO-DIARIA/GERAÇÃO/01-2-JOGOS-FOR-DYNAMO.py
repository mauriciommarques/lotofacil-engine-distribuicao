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

ENGINE = "COBERTURA-2"
ENGINE_VERSION = "1.1"

TIMEZONE = ZoneInfo(
    "America/Sao_Paulo"
)


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

    item = response.get("Item")

    if not item:
        raise Exception(
            "Resultado da Lotofácil não encontrado."
        )

    return item


# ==========================================================
# LIMPAR TABELA DE JOGOS
# ==========================================================

def limpar_tabela_jogos():

    itens_removidos = 0

    response = jogos_table.scan(
        ProjectionExpression="pk, sk"
    )

    while True:

        itens = response.get(
            "Items",
            []
        )

        if itens:

            with jogos_table.batch_writer() as batch:

                for item in itens:

                    batch.delete_item(
                        Key={
                            "pk": item["pk"],
                            "sk": item["sk"]
                        }
                    )

                    itens_removidos += 1

        if "LastEvaluatedKey" not in response:
            break

        response = jogos_table.scan(
            ProjectionExpression="pk, sk",
            ExclusiveStartKey=response[
                "LastEvaluatedKey"
            ]
        )

    return itens_removidos


# ==========================================================
# SALVAR JOGO
# ==========================================================

def salvar_jogo(
    concurso,
    jogo,
    tipo_combinacao,
    id_execucao
):

    agora = datetime.now(
        TIMEZONE
    )

    data = agora.strftime(
        "%Y-%m-%d"
    )

    # ------------------------------------------------------
    # SK ÚNICA
    #
    # O mesmo id_execucao é usado nos dois jogos,
    # identificando que pertencem ao mesmo par.
    # ------------------------------------------------------

    sk = (
        f"{concurso}"
        f"#{ENGINE}"
        f"#{id_execucao}"
        f"#{tipo_combinacao}"
    )

    item = {
        "pk":
            "JOGO",

        "sk":
            sk,

        "data":
            data,

        "concurso":
            concurso,

        "engine":
            ENGINE,

        "engine_version":
            ENGINE_VERSION,

        "id_execucao":
            id_execucao,

        "tipo_combinacao":
            tipo_combinacao,

        "jogo":
            jogo
    }

    jogos_table.put_item(
        Item=item
    )


# ==========================================================
# GERAR OS 2 JOGOS
#
# IMPORTANTE:
# Esta função NÃO limpa e NÃO grava nada.
# Apenas gera e valida.
# ==========================================================

def gerar_jogos():

    # ======================================================
    # RESULTADO ANTERIOR
    # ======================================================

    resultado_anterior = (
        buscar_resultado_concurso_anterior()
    )

    concurso_anterior = int(
        resultado_anterior["concurso"]
    )

    proximo_concurso = (
        concurso_anterior + 1
    )


    # ======================================================
    # 15 DEZENAS DO CONCURSO ANTERIOR
    # ======================================================

    anterior = [
        int(numero)
        for numero
        in resultado_anterior["listaDezenas"]
    ]


    # ======================================================
    # VALIDAR RESULTADO ANTERIOR
    # ======================================================

    if len(anterior) != 15:

        raise Exception(
            "O concurso anterior deve possuir "
            "exatamente 15 dezenas."
        )

    if len(set(anterior)) != 15:

        raise Exception(
            "O concurso anterior possui "
            "dezenas repetidas."
        )

    if any(
        numero < 1 or numero > 25
        for numero in anterior
    ):

        raise Exception(
            "Existem dezenas fora do intervalo 01-25."
        )


    # ======================================================
    # 3ANT
    #
    # 3 dezenas do concurso anterior.
    #
    # Serão comuns aos dois jogos.
    # ======================================================

    ant3 = random.sample(
        anterior,
        3
    )


    # ======================================================
    # RESTANTES DO CONCURSO ANTERIOR
    #
    # 15 - 3 = 12
    # ======================================================

    restantes_anterior = [
        dezena
        for dezena in anterior
        if dezena not in ant3
    ]

    random.shuffle(
        restantes_anterior
    )


    # ======================================================
    # CONJ A
    #
    # 3Ant + 7 exclusivas
    #
    # Total = 10
    # ======================================================

    extras_A = (
        restantes_anterior[:7]
    )

    conjA = (
        ant3
        + extras_A
    )


    # ======================================================
    # CONJ B
    #
    # 3Ant + outras 5 exclusivas
    #
    # Total = 8
    # ======================================================

    extras_B = (
        restantes_anterior[7:]
    )

    conjB = (
        ant3
        + extras_B
    )


    # ======================================================
    # 10 DEZENAS QUE NÃO SAÍRAM
    # ======================================================

    nao_sairam = [
        dezena
        for dezena in range(1, 26)
        if dezena not in anterior
    ]

    if len(nao_sairam) != 10:

        raise Exception(
            "Devem existir exatamente "
            "10 dezenas que não saíram."
        )


    # ======================================================
    # 2 FIXAS DAS QUE NÃO SAÍRAM
    #
    # Também serão comuns aos dois jogos.
    # ======================================================

    nSairam = random.sample(
        nao_sairam,
        2
    )


    # ======================================================
    # RESTANTES DAS NÃO SORTEADAS
    #
    # 10 - 2 = 8
    # ======================================================

    restantes_nao_sairam = [
        dezena
        for dezena in nao_sairam
        if dezena not in nSairam
    ]

    random.shuffle(
        restantes_nao_sairam
    )


    # ======================================================
    # CONJ R
    #
    # 2 fixas + 3 exclusivas
    #
    # Total = 5
    # ======================================================

    extras_R = (
        restantes_nao_sairam[:3]
    )

    conjR = (
        nSairam
        + extras_R
    )


    # ======================================================
    # CONJ S
    #
    # 2 fixas + outras 5 exclusivas
    #
    # Total = 7
    # ======================================================

    extras_S = (
        restantes_nao_sairam[3:]
    )

    conjS = (
        nSairam
        + extras_S
    )


    # ======================================================
    # JOGOS FINAIS
    #
    # JOGO 1 = A + R
    # JOGO 2 = B + S
    # ======================================================

    jogo_1 = (
        conjA
        + conjR
    )

    jogo_2 = (
        conjB
        + conjS
    )


    # ======================================================
    # VALIDAR TAMANHO
    # ======================================================

    if len(jogo_1) != 15:

        raise Exception(
            "Jogo 1 deve possuir exatamente 15 dezenas."
        )

    if len(jogo_2) != 15:

        raise Exception(
            "Jogo 2 deve possuir exatamente 15 dezenas."
        )


    # ======================================================
    # VALIDAR REPETIÇÕES INTERNAS
    # ======================================================

    if len(set(jogo_1)) != 15:

        raise Exception(
            "Jogo 1 possui dezenas repetidas."
        )

    if len(set(jogo_2)) != 15:

        raise Exception(
            "Jogo 2 possui dezenas repetidas."
        )


    # ======================================================
    # VALIDAR AS 5 DEZENAS COMUNS
    #
    # 3 do 3Ant
    # +
    # 2 do nSairam
    # ======================================================

    comuns = (
        set(jogo_1)
        &
        set(jogo_2)
    )

    if len(comuns) != 5:

        raise Exception(
            "Os jogos devem possuir exatamente "
            "5 dezenas em comum."
        )


    # ======================================================
    # VALIDAR SE AS COMUNS SÃO EXATAMENTE
    # 3ANT + nSairam
    # ======================================================

    comuns_esperadas = (
        set(ant3)
        |
        set(nSairam)
    )

    if comuns != comuns_esperadas:

        raise Exception(
            "As dezenas comuns não correspondem "
            "ao 3Ant + nSairam."
        )


    # ======================================================
    # VALIDAR COBERTURA DAS 25
    # ======================================================

    cobertura = (
        set(jogo_1)
        |
        set(jogo_2)
    )

    if cobertura != set(range(1, 26)):

        raise Exception(
            "Os dois jogos não cobrem todas "
            "as dezenas de 01 a 25."
        )


    # ======================================================
    # ORDENAR SOMENTE OS JOGOS FINAIS
    # ======================================================

    jogo_1 = sorted(
        jogo_1
    )

    jogo_2 = sorted(
        jogo_2
    )


    # ======================================================
    # RETORNAR
    #
    # ATÉ AQUI NADA FOI ALTERADO EM jogos_lotofacil
    # ======================================================

    return {
        "concurso_anterior":
            concurso_anterior,

        "concurso":
            proximo_concurso,

        "jogo_1":
            jogo_1,

        "jogo_2":
            jogo_2
    }


# ==========================================================
# PERGUNTAR MODO DE GRAVAÇÃO
# ==========================================================

def perguntar_agregar():

    print()
    print("========================================")
    print(" MODO DE GRAVAÇÃO")
    print("========================================")
    print()
    print("SIM = manter jogos existentes")
    print("      e agregar este novo par.")
    print()
    print("NÃO = limpar jogos existentes")
    print("      e salvar somente este novo par.")
    print()

    resposta = input(
        "Deseja agregar ao database? (Sim/Não): "
    )

    resposta = (
        resposta
        .strip()
        .lower()
    )


    # ------------------------------------------------------
    # SIM
    # ------------------------------------------------------

    if resposta in (
        "sim",
        "s"
    ):

        return True


    # ------------------------------------------------------
    # NÃO
    # ------------------------------------------------------

    if resposta in (
        "nao",
        "não",
        "n"
    ):

        return False


    # ------------------------------------------------------
    # QUALQUER OUTRA RESPOSTA
    #
    # NÃO FAZER NADA NO BANCO.
    # ------------------------------------------------------

    raise Exception(
        "Resposta inválida. "
        "Operação cancelada sem alterar o DynamoDB."
    )


# ==========================================================
# GRAVAR OS JOGOS
# ==========================================================

def gravar_jogos(
    resultado,
    agregar
):

    concurso = (
        resultado["concurso"]
    )

    jogo_1 = (
        resultado["jogo_1"]
    )

    jogo_2 = (
        resultado["jogo_2"]
    )


    # ======================================================
    # ID ÚNICO DO PAR
    #
    # Os dois jogos recebem o MESMO ID.
    # ======================================================

    agora = datetime.now(
        TIMEZONE
    )

    id_execucao = agora.strftime(
        "%Y%m%dT%H%M%S%f"
    )


    # ======================================================
    # LIMPAR SOMENTE SE NÃO FOR AGREGAR
    # ======================================================

    if agregar:

        removidos = 0

    else:

        removidos = (
            limpar_tabela_jogos()
        )


    # ======================================================
    # SALVAR JOGO 1
    # ======================================================

    salvar_jogo(
        concurso=concurso,
        jogo=jogo_1,
        tipo_combinacao="A-R",
        id_execucao=id_execucao
    )


    # ======================================================
    # SALVAR JOGO 2
    # ======================================================

    salvar_jogo(
        concurso=concurso,
        jogo=jogo_2,
        tipo_combinacao="B-S",
        id_execucao=id_execucao
    )


    return {
        "removidos":
            removidos,

        "salvos":
            2,

        "id_execucao":
            id_execucao
    }


# ==========================================================
# HANDLER
# ==========================================================

def lambda_handler(
    event,
    context
):

    try:

        # ==================================================
        # GERAR E VALIDAR PRIMEIRO
        # ==================================================

        resultado = (
            gerar_jogos()
        )


        # ==================================================
        # MOSTRAR OS JOGOS ANTES DE ALTERAR O BANCO
        # ==================================================

        print()
        print("========================================")
        print(" 2 JOGOS GERADOS - AINDA NÃO SALVOS")
        print("========================================")

        print(
            "JOGO 1:",
            resultado["jogo_1"]
        )

        print(
            "JOGO 2:",
            resultado["jogo_2"]
        )

        print("========================================")


        # ==================================================
        # PERGUNTAR O QUE FAZER
        #
        # ATÉ AQUI jogos_lotofacil CONTINUA INTACTA.
        # ==================================================

        agregar = (
            perguntar_agregar()
        )


        # ==================================================
        # GRAVAR
        # ==================================================

        gravacao = gravar_jogos(
            resultado,
            agregar
        )


        # ==================================================
        # RESULTADO FINAL
        # ==================================================

        print()
        print("========================================")

        if agregar:

            print(
                "MODO: AGREGAR"
            )

            print(
                "Jogos existentes foram mantidos."
            )

        else:

            print(
                "MODO: SUBSTITUIR"
            )

            print(
                "Jogos antigos removidos:",
                gravacao["removidos"]
            )

        print(
            "Jogos novos salvos:",
            gravacao["salvos"]
        )

        print(
            "ID do novo par:",
            gravacao["id_execucao"]
        )

        print("========================================")


        # ==================================================
        # RETORNO
        # ==================================================

        return {
            "statusCode": 200,

            "body": json.dumps({
                "concurso":
                    resultado["concurso"],

                "jogo_1":
                    resultado["jogo_1"],

                "jogo_2":
                    resultado["jogo_2"],

                "modo":
                    (
                        "AGREGAR"
                        if agregar
                        else "SUBSTITUIR"
                    ),

                "removidos":
                    gravacao["removidos"],

                "salvos":
                    gravacao["salvos"],

                "id_execucao":
                    gravacao["id_execucao"],

                "engine":
                    ENGINE
            })
        }


    except Exception as erro:

        print()
        print("========================================")
        print(" ERRO / OPERAÇÃO CANCELADA")
        print("========================================")
        print(str(erro))
        print("========================================")

        return {
            "statusCode": 500,

            "body": json.dumps({
                "erro":
                    str(erro)
            })
        }


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

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