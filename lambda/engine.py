# ==========================================================
# IMPORTS
import json
import boto3

import random

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# ==========================================================
# CONSTANTES
# ==========================================================
QTD_PARES = 7
QTD_IMPARES = 8

QTD_PRIMOS = 5
QTD_FIBONACCI = 4
QTD_MULTIPLOS3 = 5
QTD_MOLDURA = 9
QTD_CENTRO = 6


MAX_QTD_SEQUENCIAS = 3
MAX_SEQUENCIA = 5
TAMANHO_MINIMO_SEQUENCIA = 3


TAMANHO_UNIVERSO = 19

MAX_SEQUENCIA_FIXOS = 2
MAX_TENTATIVAS_FIXOS = 100


# ==========================================================
# CONFIG
# ==========================================================

REGION = "ap-east-1"

TABLE_NAME = "jogos_lotofacil"

TABLE_ESTATISTICA = "estatistica_lotofacil"

ENGINE = "ENGINE-03"

ENGINE_VERSION = "1.0"

# ==========================================================
# DYNAMODB
# ==========================================================

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION
)

TABLE_RESULTADO = "resultado_lotofacil"

table = dynamodb.Table(
    TABLE_NAME
)

resultado_table = dynamodb.Table(
    TABLE_RESULTADO
)

estatistica_table = dynamodb.Table(
    TABLE_ESTATISTICA
)

def LimiteEngineAtingido():

    hoje = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    ).strftime("%Y-%m-%d")

    response = table.scan()

    jogos = response.get(
        "Items",
        []
    )

    quantidade = len([

        jogo

        for jogo in jogos

        if (
            jogo.get("data") == hoje
            and jogo.get("engine") == ENGINE
        )

    ])

    return quantidade >= 5

def maior_sequencia(jogo):
    jogo = sorted(jogo)

    maior = 1
    atual = 1

    for i in range(1, len(jogo)):
        if jogo[i] == jogo[i - 1] + 1:
            atual += 1
            maior = max(maior, atual)
        else:
            atual = 1

    return maior    

def contar_sequencias(jogo):

    jogo = sorted(jogo)

    quantidade = 0
    atual = 1

    for i in range(1, len(jogo)):

        if jogo[i] == jogo[i - 1] + 1:

            atual += 1

        else:
            if atual >= TAMANHO_MINIMO_SEQUENCIA:
                quantidade += 1

            atual = 1

    if atual >= TAMANHO_MINIMO_SEQUENCIA:
        quantidade += 1

    return quantidade

# ==========================================================
# OBTER RESULTADO
# ==========================================================
def buscar_fixos_concurso_anterior():

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

    for tentativa in range(
        MAX_TENTATIVAS_FIXOS
    ):

        fixos = sorted(
            random.sample(
                item["listaDezenas"],
                8
            )
        )

        maior_seq = maior_sequencia(
            fixos
        )

        if maior_seq <= MAX_SEQUENCIA_FIXOS:

            print(
                "[LOTOFACIL] >>> FIXOS APROVADOS <<<"
            )

            print(
                f"[LOTOFACIL] Tentativa: {tentativa + 1}"
            )

            print(
                f"[LOTOFACIL] Fixos: {fixos}"
            )

            print(
                f"[LOTOFACIL] Maior sequência: {maior_seq}"
            )

            return {
                "concurso": int(
                    item["concurso"]
                ),
                "fixos": fixos
            }

    raise Exception(
        "Não foi possível encontrar "
        "8 fixos sem sequência acima do limite."
    )

def BuscarResultadoBanco():

    response = resultado_table.get_item(

        Key={

            "pk": "LOTOFACIL",

            "sk": "ULTIMO"

        }

    )

    item = response.get(
        "Item"
    )

    return item

# ==========================================================
# UNIVERSO
# ==========================================================

def montar_universo(
    numeros_fixos
):
    faltam = (
        TAMANHO_UNIVERSO
        - len(numeros_fixos)
    )

    disponiveis = [

        n

        for n in range(1, 26)

        if n not in numeros_fixos
    ]

    universo = (
        numeros_fixos
        + random.sample(
            disponiveis,
            faltam
        )
    )

    return sorted(universo) 

def gerar_jogo_inicial(
    universo,
    numeros_fixos,
    concurso
):
    moldura_jogo = []
    centro_jogo = []
    primos_jogo = []
    multiplos3_jogo = []

    resultado = []

    fib = []

    pares_escolhidos = []
    impares_escolhidos = []

    # =====================================================
    # PARES E ÍMPARES DOS FIXOS
    # =====================================================

    pares = {2,4,6,8,10,12,14,16,18,20,22,24}
    impares = {1,3,5,7,9,11,13,15,17,19,21,23,25}
    moldura = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
    centro = {12, 13, 14, 17, 18, 19}
    primos = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    multiplos3 = { 3, 6, 9, 12, 15, 18, 21, 24 }

    pares_escolhidos = [
        n for n in numeros_fixos
        if n in pares
    ]

    impares_escolhidos = [
        n for n in numeros_fixos
        if n in impares
    ]

    faltam_pares = QTD_PARES - len(pares_escolhidos)
    faltam_impares = QTD_IMPARES - len(impares_escolhidos)

    # =====================================================
    # COMPLETA PARES
    # =====================================================

    pares_disponiveis = [
        n for n in universo
        if n in pares
        and n not in pares_escolhidos
    ]

    if len(pares_disponiveis) < faltam_pares:

        print("[LOTOFACIL] !!! FALHA PARES !!!")
        print(f"[LOTOFACIL] Pares disponíveis: {pares_disponiveis}")
        print(f"[LOTOFACIL] Faltam pares: {faltam_pares}")

        return None

    novos_pares = random.sample(
        pares_disponiveis,
        faltam_pares
    )

    pares_escolhidos.extend(novos_pares)

    # =====================================================
    # COMPLETA ÍMPARES
    # =====================================================

    impares_disponiveis = [
        n for n in universo
        if n in impares
        and n not in impares_escolhidos
    ]

    if len(impares_disponiveis) < faltam_impares:

        print("[LOTOFACIL] !!! FALHA ÍMPARES !!!")
        print(f"[LOTOFACIL] Ímpares disponíveis: {impares_disponiveis}")
        print(f"[LOTOFACIL] Faltam ímpares: {faltam_impares}")

        return None

    novos_impares = random.sample(
        impares_disponiveis,
        faltam_impares
    )

    impares_escolhidos.extend(novos_impares)

    resultado = sorted(
        pares_escolhidos + impares_escolhidos
    )

    numeros_livres = [
        n for n in resultado
        if n not in numeros_fixos
    ]

    fibonacci = {1,2,3,5,8,13,21}

    fib = [
        n for n in resultado
        if n in fibonacci
    ]

    fib_fixos = [
        n for n in fib
        if n in numeros_fixos
    ]

    if len(fib_fixos) > QTD_FIBONACCI:

        print("[LOTOFACIL] !!! FALHA FIBONACCI FIXOS !!!")
        print(f"[LOTOFACIL] Fibonacci fixos: {fib_fixos}")
        print(f"[LOTOFACIL] Quantidade: {len(fib_fixos)}")
        print(f"[LOTOFACIL] Limite: {QTD_FIBONACCI}")

        return None


    fib_removiveis = [
        n for n in fib
        if n in numeros_livres
    ]
    
    # =====================================================
    # AJUSTE FIBONACCI
    # =====================================================

    EXCESSO_FIB = max(0, len(fib) - QTD_FIBONACCI)

    fibonacci_ok = True

    while EXCESSO_FIB > 0:

        fib_removiveis = [
            n for n in fib
            if n not in numeros_fixos
        ]
            
        random.shuffle(fib_removiveis)
        
        trocou = False
        
        for remover in fib_removiveis:

            if remover in pares:

                pares_reposicao = [
                    n for n in universo
                    if n in pares
                    and n not in fibonacci
                    and n not in pares_escolhidos
                ]

                if pares_reposicao:

                    novo = random.choice(pares_reposicao)
                    
                    pares_escolhidos.remove(remover)
                    pares_escolhidos.append(novo)

                    trocou = True

                    break

            else:

                impares_reposicao = [
                    n for n in universo
                    if n in impares
                    and n not in fibonacci
                    and n not in impares_escolhidos
                ]

                if impares_reposicao:

                    novo = random.choice(impares_reposicao)

                    impares_escolhidos.remove(remover)
                    impares_escolhidos.append(novo)

                    trocou = True

                    break

        if not trocou:
            fibonacci_ok = False
            break

        resultado = sorted(
            pares_escolhidos + impares_escolhidos
        )

        numeros_livres = [
            n for n in resultado
            if n not in numeros_fixos
        ]

        fib = [
            n for n in resultado
            if n in fibonacci
        ]

        fib_removiveis = [
            n for n in fib
            if n in numeros_livres
        ]
        
        EXCESSO_FIB = max(0, len(fib) - QTD_FIBONACCI)

    # =====================================================
    # MOLDURA
    # =====================================================
    if fibonacci_ok:

        moldura_jogo = [
            n for n in resultado
            if n in moldura
        ]

        EXCESSO_MOLDURA = max(
            0,
            len(moldura_jogo) - QTD_MOLDURA
        )    

        moldura_livres = [
            n for n in moldura_jogo
            if n in numeros_livres
        ]

        EXCESSO_MOLDURA = max(
            0,
            len(moldura_jogo) - QTD_MOLDURA
        )

        while EXCESSO_MOLDURA > 0:

            trocou = False

            random.shuffle(moldura_livres)

            for remover in moldura_livres:

                if remover in pares:

                    pares_reposicao = [
                        n for n in universo
                        if n in centro
                        and n in pares
                        and n not in resultado
                    ]

                    if pares_reposicao:

                        novo = random.choice(pares_reposicao)

                        pares_escolhidos.remove(remover)
                        pares_escolhidos.append(novo)

                        trocou = True
                        break                  
                    
                else:
                    
                    impares_reposicao = [
                        n for n in universo
                        if n in centro
                        and n in impares
                        and n not in resultado
                    ]

                    if impares_reposicao:

                        novo = random.choice(impares_reposicao)

                        impares_escolhidos.remove(remover)
                        impares_escolhidos.append(novo)

                        trocou = True
                        break            

            if not trocou:

                break

            resultado = sorted(
                pares_escolhidos + impares_escolhidos
            )

            numeros_livres = [
                n for n in resultado
                if n not in numeros_fixos
            ]

            moldura_jogo = [
                n for n in resultado
                if n in moldura
            ]

            moldura_livres = [
                n for n in moldura_jogo
                if n in numeros_livres
            ]

            EXCESSO_MOLDURA = max(
                0,
                len(moldura_jogo) - QTD_MOLDURA
            )  
            
                                        

        centro_jogo = [
            n for n in resultado
            if n in centro
        ]

        EXCESSO_CENTRO = max(
            0,
            len(centro_jogo) - QTD_CENTRO
        )

        centro_fixos = [
            n for n in centro_jogo
            if n in numeros_fixos
        ]

        if len(centro_fixos) > QTD_CENTRO:

            print("[LOTOFACIL] !!! FALHA CENTRO FIXOS !!!")
            print(f"[LOTOFACIL] Centro fixos: {centro_fixos}")
            print(f"[LOTOFACIL] Quantidade: {len(centro_fixos)}")
            print(f"[LOTOFACIL] Limite: {QTD_CENTRO}")

            return None

        centro_livres = [
            n for n in centro_jogo
            if n in numeros_livres
        ]

        while EXCESSO_CENTRO > 0:

            random.shuffle(centro_livres)

            trocou = False    

            for remover in centro_livres:

                if remover in pares:                    

                    pares_reposicao = [
                        n for n in universo
                        if n in moldura
                        and n in pares
                        and n not in resultado
                    ]

                    if pares_reposicao:

                        novo = random.choice(pares_reposicao)

                        pares_escolhidos.remove(remover)
                        pares_escolhidos.append(novo)

                        trocou = True
                        break                

                else:
                
                    impares_reposicao = [
                        n for n in universo
                        if n in moldura
                        and n in impares
                        and n not in resultado
                    ]

                    if impares_reposicao:

                        novo = random.choice(impares_reposicao)

                        impares_escolhidos.remove(remover)
                        impares_escolhidos.append(novo)

                        trocou = True
                        break                       

            if not trocou:
                break
            
            resultado = sorted(
                pares_escolhidos + impares_escolhidos
            )

            numeros_livres = [
                n for n in resultado
                if n not in numeros_fixos
            ]

            centro_jogo = [
                n for n in resultado
                if n in centro
            ]

            centro_livres = [
                n for n in centro_jogo
                if n in numeros_livres
            ]

            EXCESSO_CENTRO = max(
                0,
                len(centro_jogo) - QTD_CENTRO
            )

        # =====================================================
        # PRIMOS
        # =====================================================

        primos_jogo = [
            n for n in resultado
            if n in primos
        ]

        primos_fixos = [
            n for n in primos_jogo
            if n in numeros_fixos
        ]

        if len(primos_fixos) > QTD_PRIMOS:

            print("[LOTOFACIL] !!! FALHA PRIMOS FIXOS !!!")
            print(f"[LOTOFACIL] Primos fixos: {primos_fixos}")
            print(f"[LOTOFACIL] Quantidade: {len(primos_fixos)}")
            print(f"[LOTOFACIL] Limite: {QTD_PRIMOS}")

            return None       

        primos_livres = [
            n for n in primos_jogo
            if n in numeros_livres
        ]

        EXCESSO_PRIMOS = max(
            0,
            len(primos_jogo) - QTD_PRIMOS
        )  

        while EXCESSO_PRIMOS > 0:

            random.shuffle(primos_livres)

            trocou = False

            for remover in primos_livres:

                if remover in pares:

                    pares_reposicao = [
                        n for n in universo
                        if n in pares
                        and n not in primos
                        and n not in resultado
                    ]

                    if pares_reposicao:

                        novo = random.choice(pares_reposicao)

                        pares_escolhidos.remove(remover)
                        pares_escolhidos.append(novo)

                        trocou = True
                        break

                else:

                    impares_reposicao = [
                        n for n in universo
                        if n in impares
                        and n not in primos
                        and n not in resultado
                    ]

                    if impares_reposicao:

                        novo = random.choice(impares_reposicao)

                        impares_escolhidos.remove(remover)
                        impares_escolhidos.append(novo)

                        trocou = True
                        break

            if not trocou:
                break

            resultado = sorted(pares_escolhidos + impares_escolhidos)

            numeros_livres = [
                n for n in resultado
                if n not in numeros_fixos
            ]

            primos_jogo = [
                n for n in resultado
                if n in primos
            ]

            primos_livres = [
                n for n in primos_jogo
                if n in numeros_livres
            ]

            EXCESSO_PRIMOS = max(
                0,
                len(primos_jogo) - QTD_PRIMOS
            )    

        multiplos3_jogo = [
            n for n in resultado
            if n in multiplos3
        ]     

        multiplos3_fixos = [
            n for n in multiplos3_jogo
            if n in numeros_fixos
        ]  


        if len(multiplos3_fixos) > QTD_MULTIPLOS3:

            print("[LOTOFACIL] !!! FALHA MÚLTIPLOS 3 FIXOS !!!")
            print(f"[LOTOFACIL] Múltiplos 3 fixos: {multiplos3_fixos}")
            print(f"[LOTOFACIL] Quantidade: {len(multiplos3_fixos)}")
            print(f"[LOTOFACIL] Limite: {QTD_MULTIPLOS3}")

            return None
            
        multiplos3_livres = [
            n for n in multiplos3_jogo
            if n in numeros_livres
        ]   

        EXCESSO_MULTIPLOS3 = max(
            0,
            len(multiplos3_jogo) - QTD_MULTIPLOS3
        )    

        while EXCESSO_MULTIPLOS3 > 0:

            random.shuffle(multiplos3_livres)

            trocou = False

            for remover in multiplos3_livres:

                if remover in pares:

                    pares_reposicao = [
                        n for n in universo
                        if n in pares
                        and n not in multiplos3
                        and n not in resultado
                    ]

                    if pares_reposicao:

                        novo = random.choice(pares_reposicao)
                                        
                        pares_escolhidos.remove(remover)
                        pares_escolhidos.append(novo)

                        trocou = True
                        break

                else:

                    impares_reposicao = [
                        n for n in universo
                        if n in impares
                        and n not in multiplos3
                        and n not in resultado
                    ]


                    if impares_reposicao:

                        novo = random.choice(impares_reposicao)

                        impares_escolhidos.remove(remover)
                        impares_escolhidos.append(novo)

                        trocou = True
                        break

            if not trocou:

                break

            resultado = sorted(pares_escolhidos + impares_escolhidos)

            numeros_livres = [
                n for n in resultado
                if n not in numeros_fixos
            ]

            multiplos3_jogo = [
                n for n in resultado
                if n in multiplos3
            ]

            multiplos3_livres = [
                n for n in multiplos3_jogo
                if n in numeros_livres
            ]
   
            EXCESSO_MULTIPLOS3 = max(
                0,
                len(multiplos3_jogo) - QTD_MULTIPLOS3
            )  
            
    qtd_sequencias = contar_sequencias(resultado)

    status_qtd_sequencias = (
        qtd_sequencias <= MAX_QTD_SEQUENCIAS
    )

    status_sequencia = (
        maior_sequencia(resultado) <= MAX_SEQUENCIA
    )                

    if not status_sequencia or not status_qtd_sequencias:

        print("[LOTOFACIL] !!! FALHA SEQUÊNCIAS !!!")
        print(f"[LOTOFACIL] Jogo: {resultado}")
        print(f"[LOTOFACIL] Maior sequência: {maior_sequencia(resultado)}")
        print(f"[LOTOFACIL] Limite sequência: {MAX_SEQUENCIA}")
        print(f"[LOTOFACIL] Quantidade de sequências: {qtd_sequencias}")
        print(f"[LOTOFACIL] Limite quantidade: {MAX_QTD_SEQUENCIAS}")

        return None


    # =====================================================
    # VALIDAÇÃO FINAL
    # =====================================================
    
    status_moldura = len(moldura_jogo) == QTD_MOLDURA
    status_centro = len(centro_jogo) == QTD_CENTRO
    status_primos = len(primos_jogo) == QTD_PRIMOS
    status_pares = len(pares_escolhidos) == QTD_PARES
    status_impares = len(impares_escolhidos) == QTD_IMPARES
    status_multiplos3 = len(multiplos3_jogo) == QTD_MULTIPLOS3
    status_fib = len(fib) == QTD_FIBONACCI
    status_total = len(resultado) == 15

    jogo_valido = all([
        status_fib,
        status_moldura,
        status_centro,
        status_primos,
        status_multiplos3,
        status_pares,
        status_impares,
        status_total,
        status_sequencia,
        status_qtd_sequencias
    ])

    print("==============================================")
    print("[LOTOFACIL] >>> RAIO-X DA VALIDAÇÃO FINAL <<<")
    print(f"[LOTOFACIL] JOGO: {resultado}")
    print(f"[LOTOFACIL] FIB: {len(fib)} / {QTD_FIBONACCI} -> {status_fib}")
    print(f"[LOTOFACIL] MOLDURA: {len(moldura_jogo)} / {QTD_MOLDURA} -> {status_moldura}")
    print(f"[LOTOFACIL] CENTRO: {len(centro_jogo)} / {QTD_CENTRO} -> {status_centro}")
    print(f"[LOTOFACIL] PRIMOS: {len(primos_jogo)} / {QTD_PRIMOS} -> {status_primos}")
    print(f"[LOTOFACIL] PARES: {len(pares_escolhidos)} / {QTD_PARES} -> {status_pares}")
    print(f"[LOTOFACIL] IMPARES: {len(impares_escolhidos)} / {QTD_IMPARES} -> {status_impares}")
    print(f"[LOTOFACIL] MULTIPLOS 3: {len(multiplos3_jogo)} / {QTD_MULTIPLOS3} -> {status_multiplos3}")
    print(f"[LOTOFACIL] TOTAL: {len(resultado)} / 15 -> {status_total}")
    print(f"[LOTOFACIL] MAIOR SEQUENCIA: {maior_sequencia(resultado)} / {MAX_SEQUENCIA} -> {status_sequencia}")
    print(f"[LOTOFACIL] QTD SEQUENCIAS: {qtd_sequencias} / {MAX_QTD_SEQUENCIAS} -> {status_qtd_sequencias}")
    print(f"[LOTOFACIL] >>> JOGO VALIDO: {jogo_valido} <<<")
    print("==============================================")    

    agora = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    )

    horario = agora.isoformat()

    data = agora.strftime("%Y-%m-%d")

    item = {

        "pk": "JOGO",

        "sk": horario,

        "data": data,

        "concurso": concurso,

        "engine": ENGINE,

        "engine_version": ENGINE_VERSION,

        "fixos": numeros_fixos,

        "universo": universo,

        "jogo": resultado

    }
    
    if jogo_valido:

        print("[LOTOFACIL] >>> JOGO APROVADO <<< ")

        return item

    else:

        print("[LOTOFACIL] >>> JOGO REPROVADO NA VALIDAÇÃO FINAL <<<")

        return None


def LimiteDiarioAtingido():

    hoje = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    ).strftime("%Y-%m-%d")

    response = table.scan()

    jogos = response.get(
        "Items",
        []
    )

    quantidade = len([

        jogo

        for jogo in jogos

        if jogo.get("data") == hoje

    ])

    return quantidade > 15


def ResultadoProntoParaGerar():

    agora = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    )

    hoje = agora.date()

    print(
        f"[LOTOFACIL] Data/hora São Paulo: {agora}"
    )

    # =====================================================
    # DOMINGO NÃO GERA JOGOS
    # =====================================================

    if hoje.weekday() == 6:

        print(
            "[LOTOFACIL] >>> DOMINGO - GERAÇÃO BLOQUEADA <<<"
        )

        return False

    # =====================================================
    # ÚLTIMO RESULTADO ESPERADO
    # =====================================================

    if hoje.weekday() == 0:

        # Segunda → último sorteio foi sábado
        data_esperada = hoje - timedelta(days=2)

    else:

        # Terça a sábado → último sorteio foi ontem
        data_esperada = hoje - timedelta(days=1)

    print(
        f"[LOTOFACIL] Último resultado esperado: "
        f"{data_esperada}"
    )

    # =====================================================
    # BUSCA RESULTADO NO BANCO
    # =====================================================

    resultado = BuscarResultadoBanco()

    if not resultado:

        print(
            "[LOTOFACIL] >>> RESULTADO NÃO EXISTE NO BANCO <<<"
        )

        return False

    data_resultado = datetime.strptime(
        resultado["dataApuracao"],
        "%d/%m/%Y"
    ).date()

    print(
        f"[LOTOFACIL] Data resultado DB: "
        f"{data_resultado}"
    )

    # =====================================================
    # VALIDA DATA
    # =====================================================

    if data_resultado < data_esperada:

        print(
            "[LOTOFACIL] >>> RESULTADO AINDA NÃO ESTÁ PRONTO <<<"
        )

        return False

    print(
        "[LOTOFACIL] >>> RESULTADO CORRETO PARA GERAR <<<"
    )

    print(
        f"[LOTOFACIL] Concurso disponível: "
        f"{resultado['concurso']}"
    )

    return True


# ==========================================================
# ENGINE
# ==========================================================
def ExecutarEngine():

    print("[LOTOFACIL] >>> ENTROU NA ENGINE <<<")

    # =====================================================
    # VALIDAR RESULTADO ANTES DE QUALQUER GERAÇÃO
    # =====================================================

    print(
        "[LOTOFACIL] Verificando se o resultado está pronto..."
    )

    if not ResultadoProntoParaGerar():

        print(
            "[LOTOFACIL] >>> ENGINE AGUARDANDO NOVO RESULTADO <<<"
        )

        return None

    print(
        "[LOTOFACIL] >>> RESULTADO PRONTO PARA GERAÇÃO <<<"
    )

    # =====================================================
    # LIMITE DIÁRIO
    # =====================================================

    print(
        "[LOTOFACIL] Verificando limite diário..."
    )

    if LimiteDiarioAtingido():

        print(
            "[LOTOFACIL] >>> LIMITE DIÁRIO ATINGIDO <<<"
        )

        return None

    # =====================================================
    # LIMITE DA ENGINE
    # =====================================================

    print(
        f"[LOTOFACIL] Verificando limite da {ENGINE}..."
    )

    if LimiteEngineAtingido():

        print(
            f"[LOTOFACIL] >>> LIMITE DA {ENGINE} ATINGIDO <<<"
        )

        return None

    print(
        f"[LOTOFACIL] >>> LIMITE DA {ENGINE} NÃO ATINGIDO <<<"
    )    

    print(
        "[LOTOFACIL] >>> LIMITE DIÁRIO NÃO ATINGIDO <<<"
    )

    # =====================================================
    # RESTANTE DA ENGINE
    # =====================================================

    print(
        "[LOTOFACIL] Buscando resultado do concurso anterior..."
    )

    dados = (
        buscar_fixos_concurso_anterior()
    )

    print(
        "[LOTOFACIL] >>> RESULTADO ANTERIOR ENCONTRADO <<<"
    )

    print(
        f"[LOTOFACIL] Concurso: {dados['concurso']}"
    )

    print(
        f"[LOTOFACIL] Fixos: {dados['fixos']}"
    )

    concurso = (
        dados["concurso"]
    )

    numeros_fixos = (
        dados["fixos"]
    )

    print(
        "[LOTOFACIL] Montando universo..."
    )

    universo = (
        montar_universo(
            numeros_fixos
        )
    )

    print(
        "[LOTOFACIL] >>> UNIVERSO MONTADO <<<"
    )

    print(
        f"[LOTOFACIL] Universo: {universo}"
    )

    print(
        f"[LOTOFACIL] Quantidade: {len(universo)}"
    )

    print(
        "[LOTOFACIL] Chamando gerador de jogo..."
    )

    jogo = gerar_jogo_inicial(
        universo,
        numeros_fixos,
        concurso
    )

    if jogo:

        print(
            "[LOTOFACIL] >>> GERADOR RETORNOU UM JOGO <<<"
        )

        print(
            f"[LOTOFACIL] Jogo: {jogo['jogo']}"
        )

    else:

        print(
            "[LOTOFACIL] >>> GERADOR RETORNOU NONE <<<"
        )

    return jogo


# ==========================================================
# PERSISTÊNCIA
# ==========================================================
def SalvarEstatistica(item):

    agora = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    )

    estatistica = {

        "pk": "ESTATISTICA",

        "sk": agora.isoformat(),

        "data": agora.strftime("%Y-%m-%d"),

        "concurso": item["concurso"],

        "engine": item["engine"],

        "engine_version": item["engine_version"],

        "quantidade_primos": len([
            n for n in item["jogo"]
            if n in {2, 3, 5, 7, 11, 13, 17, 19, 23}
        ]),

        "quantidade_pares": len([
            n for n in item["jogo"]
            if n % 2 == 0
        ]),

        "quantidade_fibonacci": len([
            n for n in item["jogo"]
            if n in {1, 2, 3, 5, 8, 13, 21}
        ]),

        "quantidade_multiplos3": len([
            n for n in item["jogo"]
            if n % 3 == 0
        ]),

        "quantidade_moldura": len([
            n for n in item["jogo"]
            if n in {
                1, 2, 3, 4, 5, 6,
                10, 11, 15, 16,
                20, 21, 22, 23, 24, 25
            }
        ]),

        "quantidade_centro": len([
            n for n in item["jogo"]
            if n in {12, 13, 14, 17, 18, 19}
        ]),

        "quantidade_sequencias": contar_sequencias(
            item["jogo"]
        ),

        "maior_sequencia": maior_sequencia(
            item["jogo"]
        ),

        "quantidade_total": len(
            item["jogo"]
        )
    }

    estatistica_table.put_item(
        Item=estatistica
    )

def SalvarJogo(item):

    table.put_item(
        Item=item
    )


def SalvarErro(
    erro
):

    print(
        str(erro)
    )

# ==========================================================
# LAMBDA
# ==========================================================

def lambda_handler(event, context):

    try:

        jogo = ExecutarEngine()

        if jogo:

            SalvarJogo(
                jogo
            )

            SalvarEstatistica(
                    jogo
                )

            return {

                "statusCode": 200,

                "body": json.dumps({

                    "mensagem": "Jogo salvo com sucesso."

                })
            }

        return {

            "statusCode": 204,

            "body": json.dumps({

                "mensagem": "Nenhum jogo encontrado."

            })
        }


    except Exception as erro:

        SalvarErro(
            erro
        )

        return {
            "statusCode": 500,
            "body": json.dumps({
                "erro": str(erro)
            })
        }

