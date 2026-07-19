import random
import requests
from bs4 import BeautifulSoup

import random
import requests

# =====================================================
# PARÂMETROS ESTATÍSTICOS
# Obtidos através da análise histórica
# =====================================================
QTD_PARES = 8
QTD_IMPARES = 7

QTD_CENTRO = 5
QTD_PRIMOS = 5
QTD_FIBONACCI = 3
QTD_MULTIPLOS3 = 5
QTD_MOLDURA = 10

QTD_MIN_LINHA = 2
QTD_MAXLINHA = 4

QTD_MIN_COLUNA = 2
QTD_MAX_COLUNA = 4

def carregar_numeros_fixos():

    url = "https://api.guidi.dev.br/loteria/lotofacil/ultimo"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    dados = response.json()

    dezenas = [int(n) for n in dados["listaDezenas"]]

    return sorted(random.sample(dezenas, 8))

def erro_configuracao(regra, quantidade, maximo):

    print()
    print("=" * 50)
    print("CONFIGURAÇÃO IMPOSSÍVEL")
    print("=" * 50)

    print(
        f"Os números fixos já possuem {quantidade} {regra}."
    )

    print(f"Máximo permitido: {maximo}")

    print()
    print("A engine não pode corrigir esta situação,")
    print("pois números fixos não podem ser removidos.")

    print()
    print("Sugestão:")
    print("Altere a sequência dos NÚMEROS FIXOS")
    print("e execute novamente o gerador.")

    exit()




# =====================================================
# CONFIGURAÇÃO
# =====================================================
moldura_jogo = []
centro_jogo = []
primos_jogo = []
multiplos3_jogo = []

linhas_ok = False
colunas_ok = False

resultado = []

fib = []

pares_escolhidos = []
impares_escolhidos = []

TAMANHO_UNIVERSO = 19

# 8 Números escolhidos por você
NUMEROS_FIXOS = carregar_numeros_fixos()

multiplos3 = {
    3, 6, 9, 12, 15, 18, 21, 24
}


linha1 = {1,2,3,4,5}
linha2 = {6,7,8,9,10}
linha3 = {11,12,13,14,15}
linha4 = {16,17,18,19,20}
linha5 = {21,22,23,24,25}

coluna1 = {1, 6, 11, 16, 21}
coluna2 = {2, 7, 12, 17, 22}
coluna3 = {3, 8, 13, 18, 23}
coluna4 = {4, 9, 14, 19, 24}
coluna5 = {5,10,15,20,25}

# =====================================================
# GERA UNIVERSO
# =====================================================

faltam = TAMANHO_UNIVERSO - len(NUMEROS_FIXOS)

disponiveis = [
    n for n in range(1, 26)
    if n not in NUMEROS_FIXOS
]


universo = NUMEROS_FIXOS + random.sample(disponiveis, faltam)

# =====================================================
# EXIBIÇÃO
# =====================================================

print("=" * 50)
print("NÚMEROS FIXOS")
print("=" * 50)
print(sorted(NUMEROS_FIXOS))
print(f"Quantidade: {len(NUMEROS_FIXOS)}")

print()

print("=" * 50)
print("UNIVERSO GERADO")
print("=" * 50)
print(sorted(universo))
print(f"Quantidade: {len(universo)}")

print()

# =====================================================
# PARES E ÍMPARES DOS FIXOS
# =====================================================

pares = {2,4,6,8,10,12,14,16,18,20,22,24}
impares = {1,3,5,7,9,11,13,15,17,19,21,23,25}
moldura = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
centro = {12, 13, 14, 17, 18, 19}
primos = {2, 3, 5, 7, 11, 13, 17, 19, 23}

pares_escolhidos = [
    n for n in NUMEROS_FIXOS
    if n in pares
]

impares_escolhidos = [
    n for n in NUMEROS_FIXOS
    if n in impares
]

faltam_pares = QTD_PARES - len(pares_escolhidos)
faltam_impares = QTD_IMPARES - len(impares_escolhidos)


print()
print("=" * 50)
print("O QUE FALTA")
print("=" * 50)
print(f"Faltam pares   : {faltam_pares}")
print(f"Faltam ímpares : {faltam_impares}")


print()
print("="*50)
print("PARES DOS FIXOS")
print("="*50)
print(pares_escolhidos)
print(f"Quantidade: {len(pares_escolhidos)}")


# =====================================================
# COMPLETA PARES
# =====================================================

pares_disponiveis = [
    n for n in universo
    if n in pares
    and n not in pares_escolhidos
]

print("Quantidade disponível:", len(pares_disponiveis))
print("Preciso:", faltam_pares)
print("Lista:", sorted(pares_disponiveis))

print()
print("=" * 50)
print("DEPURAÇÃO PARES")
print("=" * 50)
print("Pares disponíveis :", sorted(pares_disponiveis))
print("Quantidade        :", len(pares_disponiveis))
print("Preciso escolher  :", faltam_pares)

if len(pares_disponiveis) < faltam_pares:
    print("ERRO: não há pares suficientes para completar o jogo.")
    print("Disponíveis:", sorted(pares_disponiveis))
    print("Preciso:", faltam_pares)
    exit()

novos_pares = random.sample(
    pares_disponiveis,
    faltam_pares
)

pares_escolhidos.extend(novos_pares)

print()
print("=" * 50)
print("PARES COMPLETOS")
print("=" * 50)
print(sorted(pares_escolhidos))
print(f"Quantidade: {len(pares_escolhidos)}")


print()
print("="*50)
print("ÍMPARES DOS FIXOS")
print("="*50)
print(impares_escolhidos)
print(f"Quantidade: {len(impares_escolhidos)}")

# =====================================================
# COMPLETA ÍMPARES
# =====================================================

impares_disponiveis = [
    n for n in universo
    if n in impares
    and n not in impares_escolhidos
]


print()
print("=" * 50)
print("DEPURAÇÃO ÍMPARES")
print("=" * 50)
print("Ímpares disponíveis :", sorted(impares_disponiveis))
print("Quantidade          :", len(impares_disponiveis))
print("Preciso escolher    :", faltam_impares)

novos_impares = random.sample(
    impares_disponiveis,
    faltam_impares
)

impares_escolhidos.extend(novos_impares)

print()
print("=" * 50)
print("ÍMPARES COMPLETOS")
print("=" * 50)
print(sorted(impares_escolhidos))
print(f"Quantidade: {len(impares_escolhidos)}")

resultado = sorted(
    pares_escolhidos + impares_escolhidos
)

numeros_livres = [
    n for n in resultado
    if n not in NUMEROS_FIXOS
]

print()
print("="*50)
print("NÚMEROS REMOVÍVEIS")
print("="*50)
print(numeros_livres)
print(f"Quantidade: {len(numeros_livres)}")

fibonacci = {1,2,3,5,8,13,21}

fib = [
    n for n in resultado
    if n in fibonacci
]

print()
print("=" * 50)
print("FIBONACCI")
print("=" * 50)
print(fib)
print(f"Quantidade: {len(fib)}")

fib_fixos = [
    n for n in fib
    if n in NUMEROS_FIXOS
]

if len(fib_fixos) > QTD_FIBONACCI:

    erro_configuracao(
        "números Fibonacci",
        len(fib_fixos),
        QTD_FIBONACCI
    )

fib_removiveis = [
    n for n in fib
    if n in numeros_livres
]

print()
print("="*50)
print("FIBONACCI FIXOS")
print("="*50)
print(fib_fixos)

print()
print("="*50)
print("FIBONACCI REMOVÍVEIS")
print("="*50)
print(fib_removiveis)

fib_removiveis_pares = [
    n for n in fib_removiveis
    if n in pares
]

fib_removiveis_impares = [
    n for n in fib_removiveis
    if n in impares
]

print()
print("=" * 50)
print("FIBONACCI REMOVÍVEIS PARES")
print("=" * 50)
print(fib_removiveis_pares)

print()
print("=" * 50)
print("FIBONACCI REMOVÍVEIS ÍMPARES")
print("=" * 50)
print(fib_removiveis_impares)

# =====================================================
# AJUSTE FIBONACCI
# =====================================================

EXCESSO_FIB = max(0, len(fib) - QTD_FIBONACCI)

FALTA_FIB = max(
    0,
    QTD_FIBONACCI - len(fib)
)

print()
print("=" * 50)
print("AJUSTE FIBONACCI")
print("=" * 50)

print("Excesso :", EXCESSO_FIB)
print("Falta   :", FALTA_FIB)

fibonacci_ok = True

while EXCESSO_FIB > 0:

    print()
    print("Precisamos remover", EXCESSO_FIB, "Fibonacci")

    fib_removiveis = [
        n for n in fib
        if n not in NUMEROS_FIXOS
    ]
        
    random.shuffle(fib_removiveis)
    
    trocou = False
    
    for remover in fib_removiveis:

        print()
        print("Tentando remover:", remover)

        if remover in pares:

            print("É um PAR")

            pares_reposicao = [
                n for n in universo
                if n in pares
                and n not in fibonacci
                and n not in pares_escolhidos
            ]

            if pares_reposicao:

                novo = random.choice(pares_reposicao)
                
                print("Entrando:", novo)

                pares_escolhidos.remove(remover)
                pares_escolhidos.append(novo)

                trocou = True

                break

        else:

            print("É um ÍMPAR")

            impares_reposicao = [
                n for n in universo
                if n in impares
                and n not in fibonacci
                and n not in impares_escolhidos
            ]

            print("Reposição possível:", sorted(impares_reposicao))


            if impares_reposicao:

                novo = random.choice(impares_reposicao)

                print("Entrando:", novo)

                impares_escolhidos.remove(remover)
                impares_escolhidos.append(novo)

                trocou = True

                break

    if not trocou:
        print()
        print("Não existe reposição possível.")
        print("O universo sorteado não permite cumprir essa regra.")

        fibonacci_ok = False

        break

    resultado = sorted(
        pares_escolhidos + impares_escolhidos
    )

    numeros_livres = [
        n for n in resultado
        if n not in NUMEROS_FIXOS
    ]

    print()
    print("="*50)
    print("NÚMEROS LIVRES")
    print("="*50)
    print(numeros_livres)
    print(f"Quantidade: {len(numeros_livres)}")

    fib = [
        n for n in resultado
        if n in fibonacci
    ]

    fib_removiveis = [
        n for n in fib
        if n in numeros_livres
    ]
    
    EXCESSO_FIB = max(0, len(fib) - QTD_FIBONACCI)

    FALTA_FIB = max(
        0,
        QTD_FIBONACCI - len(fib)
    )    


# =====================================================
# MOLDURA
# =====================================================
if fibonacci_ok:

    moldura_jogo = [
        n for n in resultado
        if n in moldura
    ]

    FALTA_MOLDURA = max(
        0,
        QTD_MOLDURA - len(moldura_jogo)
    )

    EXCESSO_MOLDURA = max(
        0,
        len(moldura_jogo) - QTD_MOLDURA
    )    

    moldura_fixas = [
        n for n in moldura_jogo
        if n in NUMEROS_FIXOS
    ]

    moldura_livres = [
        n for n in moldura_jogo
        if n in numeros_livres
    ]

    moldura_livres_pares = [
        n for n in moldura_livres
        if n in pares
    ]

    moldura_livres_impares = [
        n for n in moldura_livres
        if n in impares
    ]

    EXCESSO_MOLDURA = max(
        0,
        len(moldura_jogo) - QTD_MOLDURA
    )

    moldura_ok = True

    while EXCESSO_MOLDURA > 0:

        print()

        print("Precisamos remover", EXCESSO_MOLDURA, "Moldura")

        trocou = False

        random.shuffle(moldura_livres)

        for remover in moldura_livres:

            print()

            print("Tentando remover:", remover)

            if remover in pares:

                print("É um PAR")

                pares_reposicao = [
                    n for n in universo
                    if n in centro
                    and n in pares
                    and n not in resultado
                ]

                print("Reposição possível:", sorted(pares_reposicao))    


                if pares_reposicao:

                    novo = random.choice(pares_reposicao)

                    print("Entrando:", novo)

                    pares_escolhidos.remove(remover)
                    pares_escolhidos.append(novo)

                    trocou = True
                    break                  
                
            else:

                print("É um ÍMPAR")
                
                impares_reposicao = [
                    n for n in universo
                    if n in centro
                    and n in impares
                    and n not in resultado
                ]

                print("Reposição possível:", sorted(impares_reposicao))

                if impares_reposicao:

                    novo = random.choice(impares_reposicao)

                    print("Entrando:", novo)

                    impares_escolhidos.remove(remover)
                    impares_escolhidos.append(novo)

                    trocou = True
                    break            

        if not trocou:

            print()
            print("Não existe reposição possível.")
            print("O universo sorteado não permite cumprir essa regra.")

            moldura_ok = False

            break

        resultado = sorted(
            pares_escolhidos + impares_escolhidos
        )

        numeros_livres = [
            n for n in resultado
            if n not in NUMEROS_FIXOS
        ]

        moldura_jogo = [
            n for n in resultado
            if n in moldura
        ]

        moldura_livres = [
            n for n in moldura_jogo
            if n in numeros_livres
        ]

        moldura_fixas = [
            n for n in moldura_jogo
            if n in NUMEROS_FIXOS
        ]

        moldura_livres_pares = [
            n for n in moldura_livres
            if n in pares
        ]

        moldura_livres_impares = [
            n for n in moldura_livres
            if n in impares
        ]        

        EXCESSO_MOLDURA = max(
            0,
            len(moldura_jogo) - QTD_MOLDURA
        )  
        
                                    
    print()
    print("=" * 50)
    print("MOLDURA")
    print("=" * 50)
    print(moldura_jogo)
    print(f"Quantidade: {len(moldura_jogo)}")

    print()
    print("=" * 50)
    print("MOLDURA FIXAS")
    print("=" * 50)
    print(moldura_fixas)

    print()
    print("=" * 50)
    print("MOLDURA LIVRES")
    print("=" * 50)
    print(moldura_livres)

    print()
    print("=" * 50)
    print("MOLDURA LIVRES PARES")
    print("=" * 50)
    print(moldura_livres_pares)

    print()
    print("=" * 50)
    print("MOLDURA LIVRES ÍMPARES")
    print("=" * 50)
    print(moldura_livres_impares)

    print()
    print("=" * 50)
    print("AJUSTE MOLDURA")
    print("=" * 50)
    print("Excesso :", EXCESSO_MOLDURA)
    print("Falta   :", FALTA_MOLDURA)

    centro_jogo = [
        n for n in resultado
        if n in centro
    ]

    EXCESSO_CENTRO = max(
        0,
        len(centro_jogo) - QTD_CENTRO
    )

    FALTA_CENTRO = max(
        0,
        QTD_CENTRO - len(centro_jogo)
    )    

    centro_fixos = [
        n for n in centro_jogo
        if n in NUMEROS_FIXOS
    ]

    if len(centro_fixos) > QTD_CENTRO:

        erro_configuracao(
            "números do centro",
            len(centro_fixos),
            QTD_CENTRO
        )    

    centro_livres = [
        n for n in centro_jogo
        if n in numeros_livres
    ]

    centro_livres_pares = [
        n for n in centro_livres
        if n in pares
    ]

    centro_livres_impares = [
        n for n in centro_livres
        if n in impares
    ]  

    print()
    print("=" * 50)
    print("AJUSTE CENTRO")
    print("=" * 50)
    print("Excesso:", EXCESSO_CENTRO)
    print("Falta  :", FALTA_CENTRO)  

    centro_ok = True

    while EXCESSO_CENTRO > 0:

        print()
        print("Precisamos remover", EXCESSO_CENTRO, "Centro")

        random.shuffle(centro_livres)

        trocou = False    

        for remover in centro_livres:

            print()
            print("Tentando remover:", remover)

            if remover in pares:

                print("É um PAR")

                pares_reposicao = [
                    n for n in universo
                    if n in moldura
                    and n in pares
                    and n not in resultado
                ]

                print("Reposição possível:", sorted(pares_reposicao))

                if pares_reposicao:

                    novo = random.choice(pares_reposicao)

                    print("Entrando:", novo)

                    pares_escolhidos.remove(remover)
                    pares_escolhidos.append(novo)

                    trocou = True
                    break                

            else:

                print("É um ÍMPAR")

                impares_reposicao = [
                    n for n in universo
                    if n in moldura
                    and n in impares
                    and n not in resultado
                ]

                print("Reposição possível:", sorted(impares_reposicao))   

                if impares_reposicao:

                    novo = random.choice(impares_reposicao)

                    print("Entrando:", novo)

                    impares_escolhidos.remove(remover)
                    impares_escolhidos.append(novo)

                    trocou = True
                    break                       

        if not trocou:

            print()
            print("Não existe reposição possível.")
            print("O universo sorteado não permite cumprir essa regra.")

            centro_ok = False
            break
        
        resultado = sorted(
            pares_escolhidos + impares_escolhidos
        )

        numeros_livres = [
            n for n in resultado
            if n not in NUMEROS_FIXOS
        ]

        centro_jogo = [
            n for n in resultado
            if n in centro
        ]

        centro_livres = [
            n for n in centro_jogo
            if n in numeros_livres
        ]

        centro_livres_pares = [
            n for n in centro_livres
            if n in pares
        ]

        centro_livres_impares = [
            n for n in centro_livres
            if n in impares
        ]

        EXCESSO_CENTRO = max(
            0,
            len(centro_jogo) - QTD_CENTRO
        )

        FALTA_CENTRO = max(
            0,
            QTD_CENTRO - len(centro_jogo)
        )            

    print()
    print("=" * 50)
    print("CENTRO")
    print("=" * 50)
    print(centro_jogo)
    print(f"Quantidade: {len(centro_jogo)}")

    print()
    print("=" * 50)
    print("CENTRO FIXOS")
    print("=" * 50)
    print(centro_fixos)

    print()
    print("=" * 50)
    print("CENTRO LIVRES")
    print("=" * 50)
    print(centro_livres)

    print()
    print("=" * 50)
    print("CENTRO LIVRES PARES")
    print("=" * 50)
    print(centro_livres_pares)

    print()
    print("=" * 50)
    print("CENTRO LIVRES ÍMPARES")
    print("=" * 50)
    print(centro_livres_impares)

    # =====================================================
    # PRIMOS
    # =====================================================

    primos_jogo = [
        n for n in resultado
        if n in primos
    ]

    primos_fixos = [
        n for n in primos_jogo
        if n in NUMEROS_FIXOS
    ]

    if len(primos_fixos) > QTD_PRIMOS:

        erro_configuracao(
            "números primos",
            len(primos_fixos),
            QTD_PRIMOS
        )    

    primos_livres = [
        n for n in primos_jogo
        if n in numeros_livres
    ]

    primos_livres_pares = [
        n for n in primos_livres
        if n in pares
    ]

    primos_livres_impares = [
        n for n in primos_livres
        if n in impares
    ]

    EXCESSO_PRIMOS = max(
        0,
        len(primos_jogo) - QTD_PRIMOS
    )  

    FALTA_PRIMOS = max(
        0,
        QTD_PRIMOS - len(primos_jogo)
    )    

    primos_ok = True

    while EXCESSO_PRIMOS > 0:

        print()
        print("Precisamos remover", EXCESSO_PRIMOS, "Primos")

        random.shuffle(primos_livres)

        trocou = False

        for remover in primos_livres:

            print()
            print("Tentando remover:", remover)

            if remover in pares:

                print("É um PAR")

                pares_reposicao = [
                    n for n in universo
                    if n in pares
                    and n not in primos
                    and n not in resultado
                ]

                print("Reposição possível:", sorted(pares_reposicao))

                if pares_reposicao:

                    novo = random.choice(pares_reposicao)

                    print("Entrando:", novo)

                    pares_escolhidos.remove(remover)
                    pares_escolhidos.append(novo)

                    trocou = True
                    break

            else:

                print("É um ÍMPAR")

                impares_reposicao = [
                    n for n in universo
                    if n in impares
                    and n not in primos
                    and n not in resultado
                ]

                print("Reposição possível:", sorted(impares_reposicao))

                if impares_reposicao:

                    novo = random.choice(impares_reposicao)

                    print("Entrando:", novo)

                    impares_escolhidos.remove(remover)
                    impares_escolhidos.append(novo)

                    trocou = True
                    break

        if not trocou:

            print()
            print("Não existe reposição possível.")
            print("O universo sorteado não permite cumprir essa regra.")

            primos_ok = False
            break

        resultado = sorted(pares_escolhidos + impares_escolhidos)

        numeros_livres = [
            n for n in resultado
            if n not in NUMEROS_FIXOS
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

        FALTA_PRIMOS = max(
            0,
            QTD_PRIMOS - len(primos_jogo)
        )


    multiplos3_jogo = [
        n for n in resultado
        if n in multiplos3
    ]     

    multiplos3_fixos = [
        n for n in multiplos3_jogo
        if n in NUMEROS_FIXOS
    ]  


    if len(multiplos3_fixos) > QTD_MULTIPLOS3:

        erro_configuracao(
            "múltiplos de 3",
            len(multiplos3_fixos),
            QTD_MULTIPLOS3
        )


    multiplos3_livres = [
        n for n in multiplos3_jogo
        if n in numeros_livres
    ]   

    multiplos3_livres_pares = [
        n for n in multiplos3_livres
        if n in pares
    ]

    multiplos3_livres_impares = [
        n for n in multiplos3_livres
        if n in impares
    ]      

    EXCESSO_MULTIPLOS3 = max(
        0,
        len(multiplos3_jogo) - QTD_MULTIPLOS3
    )    

    FALTA_MULTIPLOS3 = max(
        0,
        QTD_MULTIPLOS3 - len(multiplos3_jogo)
    )    

    multiplos3_ok = True

    while EXCESSO_MULTIPLOS3 > 0:

        print()
        print("Precisamos remover", EXCESSO_MULTIPLOS3, "Múltiplos de 3")

        random.shuffle(multiplos3_livres)

        trocou = False

        for remover in multiplos3_livres:

            print()
            print("Tentando remover:", remover)

            if remover in pares:

                pares_reposicao = [
                    n for n in universo
                    if n in pares
                    and n not in multiplos3
                    and n not in resultado
                ]

                print("Reposição possível:", sorted(pares_reposicao))

                if pares_reposicao:

                    novo = random.choice(pares_reposicao)
                    
                    print("Entrando:", novo)                    

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

                print("Reposição possível:", sorted(impares_reposicao))

                if impares_reposicao:

                    novo = random.choice(impares_reposicao)

                    print("Entrando:", novo)

                    impares_escolhidos.remove(remover)
                    impares_escolhidos.append(novo)

                    trocou = True
                    break

        if not trocou:

            print()
            print("Não existe reposição possível.")
            print("O universo sorteado não permite cumprir essa regra.")

            multiplos3_ok = False
            break

        resultado = sorted(pares_escolhidos + impares_escolhidos)

        numeros_livres = [
            n for n in resultado
            if n not in NUMEROS_FIXOS
        ]

        multiplos3_jogo = [
            n for n in resultado
            if n in multiplos3
        ]

        multiplos3_livres = [
            n for n in multiplos3_jogo
            if n in numeros_livres
        ]

        multiplos3_livres_pares = [
            n for n in multiplos3_livres
            if n in pares
        ]

        multiplos3_livres_impares = [
            n for n in multiplos3_livres
            if n in impares
        ]        

        EXCESSO_MULTIPLOS3 = max(
            0,
            len(multiplos3_jogo) - QTD_MULTIPLOS3
        )  
        
            
    print()
    print("=" * 50)
    print("PRIMOS")
    print("=" * 50)
    print(primos_jogo)
    print(f"Quantidade: {len(primos_jogo)}")

    print()
    print("=" * 50)
    print("PRIMOS FIXOS")
    print("=" * 50)
    print(primos_fixos)

    print()
    print("=" * 50)
    print("PRIMOS LIVRES")
    print("=" * 50)
    print(primos_livres)

    print()
    print("=" * 50)
    print("PRIMOS LIVRES PARES")
    print("=" * 50)
    print(primos_livres_pares)

    print()
    print("=" * 50)
    print("PRIMOS LIVRES ÍMPARES")
    print("=" * 50)
    print(primos_livres_impares)

    print()
    print("=" * 50)
    print("AJUSTE PRIMOS")
    print("=" * 50)

    print("Excesso :", EXCESSO_PRIMOS)
    print("Falta   :", FALTA_PRIMOS)

    print()
    print("=" * 50)
    print("MÚLTIPLOS DE 3")
    print("=" * 50)
    print(multiplos3_jogo)
    print(f"Quantidade: {len(multiplos3_jogo)}")

    print()
    print("=" * 50)
    print("MÚLTIPLOS DE 3 FIXOS")
    print("=" * 50)
    print(multiplos3_fixos)

    print()
    print("=" * 50)
    print("MÚLTIPLOS DE 3 LIVRES")
    print("=" * 50)
    print(multiplos3_livres)

    print()
    print("=" * 50)
    print("MÚLTIPLOS DE 3 LIVRES PARES")
    print("=" * 50)
    print(multiplos3_livres_pares)

    print()
    print("=" * 50)
    print("MÚLTIPLOS DE 3 LIVRES ÍMPARES")
    print("=" * 50)
    print(multiplos3_livres_impares)

    print()
    print("=" * 50)
    print("AJUSTE MÚLTIPLOS DE 3")
    print("=" * 50)
    
    print("Excesso :", EXCESSO_MULTIPLOS3)
    print("Falta   :", FALTA_MULTIPLOS3)

    linha1_jogo = [n for n in resultado if n in linha1]
    linha2_jogo = [n for n in resultado if n in linha2]
    linha3_jogo = [n for n in resultado if n in linha3]
    linha4_jogo = [n for n in resultado if n in linha4]
    linha5_jogo = [n for n in resultado if n in linha5]

    coluna1_jogo = [n for n in resultado if n in coluna1]
    coluna2_jogo = [n for n in resultado if n in coluna2]
    coluna3_jogo = [n for n in resultado if n in coluna3]
    coluna4_jogo = [n for n in resultado if n in coluna4]
    coluna5_jogo = [n for n in resultado if n in coluna5]


    linhas_ok = all([

        QTD_MIN_LINHA <= len(linha1_jogo) <= QTD_MAXLINHA,
        QTD_MIN_LINHA <= len(linha2_jogo) <= QTD_MAXLINHA,
        QTD_MIN_LINHA <= len(linha3_jogo) <= QTD_MAXLINHA,
        QTD_MIN_LINHA <= len(linha4_jogo) <= QTD_MAXLINHA,
        QTD_MIN_LINHA <= len(linha5_jogo) <= QTD_MAXLINHA,

    ])    

    colunas_ok = all([

        QTD_MIN_COLUNA <= len(coluna1_jogo) <= QTD_MAX_COLUNA,
        QTD_MIN_COLUNA <= len(coluna2_jogo) <= QTD_MAX_COLUNA,
        QTD_MIN_COLUNA <= len(coluna3_jogo) <= QTD_MAX_COLUNA,
        QTD_MIN_COLUNA <= len(coluna4_jogo) <= QTD_MAX_COLUNA,
        QTD_MIN_COLUNA <= len(coluna5_jogo) <= QTD_MAX_COLUNA,

    ])        

    if not linhas_ok:

        print()
        print("=" * 50)
        print("LINHAS INVÁLIDAS")
        print("=" * 50)

        print("A distribuição das linhas não atende")
        print(f"ao intervalo permitido ({QTD_MIN_LINHA} a {QTD_MAXLINHA}).")

        print()
        print("Sugestão:")
        print("Execute novamente o gerador (F5).")
        print("Uma nova combinação poderá atender esta regra.")

        exit()

    if not colunas_ok:

        print()
        print("=" * 50)
        print("COLUNAS INVÁLIDAS")
        print("=" * 50)

        print("A distribuição das colunas não atende")
        print(f"ao intervalo permitido ({QTD_MIN_COLUNA} a {QTD_MAX_COLUNA}).")

        print()
        print("Sugestão:")
        print("Execute novamente o gerador (F5).")
        print("Uma nova combinação poderá atender esta regra.")

        exit()        


    EXCESSO_L1 = max(0, len(linha1_jogo) - QTD_MAXLINHA)
    EXCESSO_L2 = max(0, len(linha2_jogo) - QTD_MAXLINHA)
    EXCESSO_L3 = max(0, len(linha3_jogo) - QTD_MAXLINHA)
    EXCESSO_L4 = max(0, len(linha4_jogo) - QTD_MAXLINHA)
    EXCESSO_L5 = max(0, len(linha5_jogo) - QTD_MAXLINHA)

    FALTA_L1 = max(0, QTD_MIN_LINHA - len(linha1_jogo))
    FALTA_L2 = max(0, QTD_MIN_LINHA - len(linha2_jogo))
    FALTA_L3 = max(0, QTD_MIN_LINHA - len(linha3_jogo))
    FALTA_L4 = max(0, QTD_MIN_LINHA - len(linha4_jogo))
    FALTA_L5 = max(0, QTD_MIN_LINHA - len(linha5_jogo))

    EXCESSO_C1 = max(0, len(coluna1_jogo) - QTD_MAX_COLUNA)
    EXCESSO_C2 = max(0, len(coluna2_jogo) - QTD_MAX_COLUNA)
    EXCESSO_C3 = max(0, len(coluna3_jogo) - QTD_MAX_COLUNA)
    EXCESSO_C4 = max(0, len(coluna4_jogo) - QTD_MAX_COLUNA)
    EXCESSO_C5 = max(0, len(coluna5_jogo) - QTD_MAX_COLUNA)

    FALTA_C1 = max(0, QTD_MIN_COLUNA - len(coluna1_jogo))
    FALTA_C2 = max(0, QTD_MIN_COLUNA - len(coluna2_jogo))
    FALTA_C3 = max(0, QTD_MIN_COLUNA - len(coluna3_jogo))
    FALTA_C4 = max(0, QTD_MIN_COLUNA - len(coluna4_jogo))
    FALTA_C5 = max(0, QTD_MIN_COLUNA - len(coluna5_jogo))    

    print()
    print("=" * 50)

    print("LINHAS")
    print("=" * 50)

    print("Linha 1:", linha1_jogo)
    print("Quantidade:", len(linha1_jogo))

    print()

    print("Linha 2:", linha2_jogo)
    print("Quantidade:", len(linha2_jogo))

    print()

    print("Linha 3:", linha3_jogo)
    print("Quantidade:", len(linha3_jogo))

    print()

    print("Linha 4:", linha4_jogo)
    print("Quantidade:", len(linha4_jogo))

    print()

    print("Linha 5:", linha5_jogo)
    print("Quantidade:", len(linha5_jogo))

    print()
    print("=" * 50)
    print("AJUSTE LINHAS")
    print("=" * 50)

    print(f"Linha 1 -> Excesso: {EXCESSO_L1} | Falta: {FALTA_L1}")
    print(f"Linha 2 -> Excesso: {EXCESSO_L2} | Falta: {FALTA_L2}")
    print(f"Linha 3 -> Excesso: {EXCESSO_L3} | Falta: {FALTA_L3}")
    print(f"Linha 4 -> Excesso: {EXCESSO_L4} | Falta: {FALTA_L4}")
    print(f"Linha 5 -> Excesso: {EXCESSO_L5} | Falta: {FALTA_L5}")    

    #aqui
    print()
    print("=" * 50)

    print("COLUNAS")
    print("=" * 50)

    print("Coluna 1:", coluna1_jogo)
    print("Quantidade:", len(coluna1_jogo))

    print()

    print("Coluna 2:", coluna2_jogo)
    print("Quantidade:", len(coluna2_jogo))

    print()

    print("Coluna 3:", coluna3_jogo)
    print("Quantidade:", len(coluna3_jogo))

    print()

    print("Coluna 4:", coluna4_jogo)
    print("Quantidade:", len(coluna4_jogo))

    print()

    print("Coluna 5:", coluna5_jogo)
    print("Quantidade:", len(coluna5_jogo))

    print()
    print("=" * 50)
    print("AJUSTE COLUNAS")
    print("=" * 50)

    print(f"Coluna 1 -> Excesso: {EXCESSO_C1} | Falta: {FALTA_C1}")
    print(f"Coluna 2 -> Excesso: {EXCESSO_C2} | Falta: {FALTA_C2}")
    print(f"Coluna 3 -> Excesso: {EXCESSO_C3} | Falta: {FALTA_C3}")
    print(f"Coluna 4 -> Excesso: {EXCESSO_C4} | Falta: {FALTA_C4}")
    print(f"Coluna 5 -> Excesso: {EXCESSO_C5} | Falta: {FALTA_C5}")    

print()
print("=" * 50)
print("NOVO RESULTADO")
print("=" * 50)
print(resultado)

print()
print("=" * 50)
print("STATUS FIBONACCI")
print("=" * 50)
print(fibonacci_ok)

print("Fibonacci:", fib)
print("Quantidade:", len(fib))

print()
print("Ainda faltam remover:", EXCESSO_FIB)

# =====================================================
# VALIDAÇÃO FINAL
# =====================================================

print()
print("=" * 50)
print("VALIDAÇÃO FINAL")
print("=" * 50)

status_moldura = len(moldura_jogo) == QTD_MOLDURA
status_centro = len(centro_jogo) == QTD_CENTRO
status_primos = len(primos_jogo) == QTD_PRIMOS
status_pares = len(pares_escolhidos) == QTD_PARES
status_impares = len(impares_escolhidos) == QTD_IMPARES
status_multiplos3 = len(multiplos3_jogo) == QTD_MULTIPLOS3
status_fib = len(fib) == QTD_FIBONACCI
status_total = len(resultado) == 15
status_linhas = linhas_ok
status_colunas = colunas_ok

print(
    f"Fibonacci : {len(fib)} / {QTD_FIBONACCI} ->",
    "OK" if status_fib else "ERRO"
)

print(
    f"Moldura   : {len(moldura_jogo)} / {QTD_MOLDURA} ->",
    "OK" if status_moldura else "ERRO"
)

print(
    f"Centro    : {len(centro_jogo)} / {QTD_CENTRO} ->",
    "OK" if status_centro else "ERRO"
)

print(
    f"Primos    : {len(primos_jogo)} / {QTD_PRIMOS} ->",
    "OK" if status_primos else "ERRO"
)

print(
    f"Múltiplos3: {len(multiplos3_jogo)} / {QTD_MULTIPLOS3} ->",
    "OK" if status_multiplos3 else "ERRO"
)

print(
    f"Linhas    : {'OK' if status_linhas else 'ERRO'}"
)

print(
    f"Colunas   : {'OK' if status_colunas else 'ERRO'}"
)

print(
    f"Pares     : {len(pares_escolhidos)} / {QTD_PARES} ->",
    "OK" if status_pares else "ERRO"
)

print(
    f"Ímpares   : {len(impares_escolhidos)} / {QTD_IMPARES} ->",
    "OK" if status_impares else "ERRO"
)

print(
    f"Total     : {len(resultado)} / 15 ->",
    "OK" if status_total else "ERRO"
)

jogo_valido = all([
    status_fib,
    status_moldura,
    status_centro,
    status_primos,
    status_multiplos3,
    status_pares,
    status_impares,
    status_total,
    status_linhas,
    status_colunas
])

print()
print("=" * 50)

if jogo_valido:
    print("JOGO VÁLIDO")
else:
    print("JOGO INVÁLIDO")

print("=" * 50)

           