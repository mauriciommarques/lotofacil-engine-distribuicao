import sqlite3

# ==========================================
# CONSTANTES
# ==========================================

PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}

FIBONACCI = {1, 2, 3, 5, 8, 13, 21}

MOLDURA = {
    1,2,3,4,5,
    6,10,
    11,15,
    16,20,
    21,22,23,24,25
}

CENTRO = {
    7,8,9,
    12,13,14,
    17,18,19
}

LINHA1 = {1, 2, 3, 4, 5}
LINHA2 = {6, 7, 8, 9, 10}
LINHA3 = {11, 12, 13, 14, 15}
LINHA4 = {16, 17, 18, 19, 20}
LINHA5 = {21, 22, 23, 24, 25}

COLUNA1 = {1, 6, 11, 16, 21}
COLUNA2 = {2, 7, 12, 17, 22}
COLUNA3 = {3, 8, 13, 18, 23}
COLUNA4 = {4, 9, 14, 19, 24}
COLUNA5 = {5, 10, 15, 20, 25}


# ==========================================
# INDICADORES
# ==========================================

def calcular_pares(dezenas):

    quantidade = 0

    for dezena in dezenas:

        if dezena % 2 == 0:
            quantidade += 1

    return quantidade

def calcular_impares(dezenas):

    quantidade = 0

    for dezena in dezenas:

        if dezena % 2 != 0:
            quantidade += 1

    return quantidade

def calcular_primos(dezenas):

    quantidade = 0

    for dezena in dezenas:

        if dezena in PRIMOS:
            quantidade += 1

    return quantidade

def calcular_fibonacci(dezenas):

    quantidade = 0

    for dezena in dezenas:

        if dezena in FIBONACCI:
            quantidade += 1

    return quantidade

def calcular_multiplos3(dezenas):

    quantidade = 0

    for dezena in dezenas:

        if dezena % 3 == 0:
            quantidade += 1

    return quantidade


def calcular_moldura(dezenas):

    quantidade = 0

    for dezena in dezenas:

        if dezena in MOLDURA:
            quantidade += 1

    return quantidade

def calcular_centro(dezenas):

    quantidade = 0

    for dezena in dezenas:

        if dezena in CENTRO:
            quantidade += 1

    return quantidade

def calcular_linha1(dezenas):

    quantidade = 0

    for dezena in dezenas:
        if dezena in LINHA1:
            quantidade += 1

    return quantidade


def calcular_linha2(dezenas):

    quantidade = 0

    for dezena in dezenas:
        if dezena in LINHA2:
            quantidade += 1

    return quantidade


def calcular_linha3(dezenas):

    quantidade = 0

    for dezena in dezenas:
        if dezena in LINHA3:
            quantidade += 1

    return quantidade


def calcular_linha4(dezenas):

    quantidade = 0

    for dezena in dezenas:
        if dezena in LINHA4:
            quantidade += 1

    return quantidade


def calcular_linha5(dezenas):

    quantidade = 0

    for dezena in dezenas:
        if dezena in LINHA5:
            quantidade += 1

    return quantidade


def calcular_coluna1(dezenas):

    quantidade = 0

    for dezena in dezenas:
        if dezena in COLUNA1:
            quantidade += 1

    return quantidade


def calcular_coluna2(dezenas):

    quantidade = 0

    for dezena in dezenas:
        if dezena in COLUNA2:
            quantidade += 1

    return quantidade


def calcular_coluna3(dezenas):

    quantidade = 0

    for dezena in dezenas:
        if dezena in COLUNA3:
            quantidade += 1

    return quantidade


def calcular_coluna4(dezenas):

    quantidade = 0

    for dezena in dezenas:
        if dezena in COLUNA4:
            quantidade += 1

    return quantidade


def calcular_coluna5(dezenas):

    quantidade = 0

    for dezena in dezenas:
        if dezena in COLUNA5:
            quantidade += 1

    return quantidade

# ==========================================
# BANCO
# ==========================================

DATABASE = "database/lotofacil.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()


# ==========================================
# LER CONCURSOS
# ==========================================

cursor.execute("""
SELECT *
FROM concursos
ORDER BY concurso
""")

concursos = cursor.fetchall()

print(f"Total de concursos: {len(concursos)}")
print()


# ==========================================
# GERAR INDICADORES
# ==========================================
print("=" * 120)
print(
    f"{'CONC':>5} "
    f"{'P':>2} "
    f"{'I':>2} "
    f"{'PR':>2} "
    f"{'FB':>2} "
    f"{'M3':>2} "
    f"{'MO':>2} "
    f"{'CE':>2} "
    f"{'L1':>2} "
    f"{'L2':>2} "
    f"{'L3':>2} "
    f"{'L4':>2} "
    f"{'L5':>2} "
    f"{'C1':>2} "
    f"{'C2':>2} "
    f"{'C3':>2} "
    f"{'C4':>2} "
    f"{'C5':>2}"
)
print("=" * 120)

for concurso in concursos:

    numero = concurso[0]

    dezenas = list(concurso[2:17])

    pares = calcular_pares(dezenas)
    impares = calcular_impares(dezenas)
    primos = calcular_primos(dezenas)
    fibonacci = calcular_fibonacci(dezenas)
    multiplos3 = calcular_multiplos3(dezenas)
    moldura = calcular_moldura(dezenas)
    centro = calcular_centro(dezenas)    
    linha1 = calcular_linha1(dezenas)
    linha2 = calcular_linha2(dezenas)
    linha3 = calcular_linha3(dezenas)
    linha4 = calcular_linha4(dezenas)
    linha5 = calcular_linha5(dezenas)

    coluna1 = calcular_coluna1(dezenas)
    coluna2 = calcular_coluna2(dezenas)
    coluna3 = calcular_coluna3(dezenas)
    coluna4 = calcular_coluna4(dezenas)
    coluna5 = calcular_coluna5(dezenas)    

    print(
        f"{numero:>5} "
        f"{pares:>2} "
        f"{impares:>2} "
        f"{primos:>2} "
        f"{fibonacci:>2} "
        f"{multiplos3:>2} "
        f"{moldura:>2} "
        f"{centro:>2} "
        f"{linha1:>2} "
        f"{linha2:>2} "
        f"{linha3:>2} "
        f"{linha4:>2} "
        f"{linha5:>2} "
        f"{coluna1:>2} "
        f"{coluna2:>2} "
        f"{coluna3:>2} "
        f"{coluna4:>2} "
        f"{coluna5:>2}"
    )

    if pares + impares != 15:
        raise Exception(f"Erro no concurso {numero}: pares + impares != 15")

    if moldura + centro != 15:
        raise Exception(f"Erro no concurso {numero}: moldura + centro != 15")

    if linha1 + linha2 + linha3 + linha4 + linha5 != 15:
        raise Exception(f"Erro no concurso {numero}: linhas != 15")

    if coluna1 + coluna2 + coluna3 + coluna4 + coluna5 != 15:
        raise Exception(f"Erro no concurso {numero}: colunas != 15")

    cursor.execute("""
        INSERT OR REPLACE INTO indicadores
        (
            concurso,
            pares,
            impares,
            primos,
            fibonacci,
            multiplos3,
            moldura,
            centro,
            linha1,
            linha2,
            linha3,
            linha4,
            linha5,
            coluna1,
            coluna2,
            coluna3,
            coluna4,
            coluna5                                      
        )
        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?                          
        )
    """, (
        numero,
        pares,
        impares,
        primos,
        fibonacci,
        multiplos3,
        moldura,
        centro,
        linha1,
        linha2,
        linha3,
        linha4,
        linha5,
        coluna1,
        coluna2,
        coluna3,
        coluna4,
        coluna5        
    ))

conn.commit()

conn.close()

print()
print("Indicadores gerados com sucesso.")