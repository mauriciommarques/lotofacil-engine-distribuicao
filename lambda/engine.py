# ==========================================================
# IMPORTS
import json
import boto3

import requests
import random

from datetime import datetime, timezone

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

MAX_SEQUENCIA = 3
MAX_QTD_SEQUENCIAS = 2
TAMANHO_UNIVERSO = 19


# ==========================================================
# CONFIG
# ==========================================================

REGION = "ap-east-1"

TABLE_NAME = "jogos_lotofacil"

ENGINE = "DISTRIBUICAO"

ENGINE_VERSION = "1.0"

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

def contar_sequencias_maximas(jogo, tamanho):

    jogo = sorted(jogo)

    quantidade = 0
    atual = 1

    for i in range(1, len(jogo)):

        if jogo[i] == jogo[i - 1] + 1:
            atual += 1
        else:

            if atual == tamanho:
                quantidade += 1

            atual = 1

    if atual == tamanho:
        quantidade += 1

    return quantidade    

# ==========================================================
# OBTER RESULTADO
# ==========================================================
def buscar_fixos_concurso_anterior():

    url = (
        "https://raw.githubusercontent.com/"
        "maickon/free-apiloterias/"
        "refs/heads/master/"
        "database/lotofacil/_ultimo.json"
    )

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    dados = response.json()

    dezenas = [
        int(numero)
        for numero in dados["listaDezenas"]
    ]

    return {

        "concurso": dados["numero"],

        "fixos": sorted(
            random.sample(
                dezenas,
                8
            )
        )

    }

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
            
                

    qtd_sequencias = contar_sequencias_maximas(resultado, MAX_SEQUENCIA)

    status_qtd_sequencias = (
        qtd_sequencias <= MAX_QTD_SEQUENCIAS
    )

    status_sequencia = maior_sequencia(resultado) <= MAX_SEQUENCIA

    if not status_sequencia or not status_qtd_sequencias:
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

    horario = datetime.now(
        timezone.utc
    ).isoformat() 

    item = {

        "pk": "JOGO",

        "sk": horario,

        "concurso": concurso,

        "engine": ENGINE,

        "engine_version": ENGINE_VERSION,

        "fixos": numeros_fixos,

        "universo": universo,

        "jogo": resultado

    }
    
    if jogo_valido:
        return item
    else:
        return None

# ==========================================================
# ENGINE
# ==========================================================
def ExecutarEngine():

    dados = (
        buscar_fixos_concurso_anterior()
    )

    concurso = (
        dados["concurso"]
    )

    numeros_fixos = (
        dados["fixos"]
    )

    universo = (
        montar_universo(
            numeros_fixos
        )
    )

    return gerar_jogo_inicial(
        universo,
        numeros_fixos,
        concurso
    )

# ==========================================================
# PERSISTÊNCIA
# ==========================================================

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

