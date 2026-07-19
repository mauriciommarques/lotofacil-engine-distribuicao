import sqlite3

# ==========================================
# BANCO
# ==========================================

DATABASE = "database/lotofacil.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

resumo = []

resumo = []

INDICADORES = [
    ("pares", "PARES"),
    ("impares", "ÍMPARES"),
    ("primos", "PRIMOS"),
    ("fibonacci", "FIBONACCI"),
    ("multiplos3", "MÚLTIPLOS 3"),
    ("moldura", "MOLDURA"),
    ("centro", "CENTRO"),
    ("linha1", "LINHA 1"),
    ("linha2", "LINHA 2"),
    ("linha3", "LINHA 3"),
    ("linha4", "LINHA 4"),
    ("linha5", "LINHA 5"),
    ("coluna1", "COLUNA 1"),
    ("coluna2", "COLUNA 2"),
    ("coluna3", "COLUNA 3"),
    ("coluna4", "COLUNA 4"),
    ("coluna5", "COLUNA 5"),
]

def gerar_estatistica(indicador, titulo):

    cursor.execute(f"""
    SELECT
        {indicador},
        COUNT(*) AS quantidade
    FROM indicadores
    GROUP BY {indicador}
    ORDER BY {indicador}
    """)

    registros = cursor.fetchall()

    print("=" * 55)
    print(f"ESTATÍSTICA - {titulo}")
    print("=" * 55)
    print(f"{titulo:>8} {'QTDE':>8} {'%':>8}")
    print("-" * 55)

    total = sum(qtd for _, qtd in registros)

    for valor, quantidade in registros:

        percentual = quantidade / total * 100

        print(
            f"{valor:>8}"
            f"{quantidade:>8}"
            f"{percentual:>8.2f}%"
        )

    maior_quantidade = max(qtd for _, qtd in registros)

    modas = [
        valor
        for valor, qtd in registros
        if qtd == maior_quantidade
    ]

    percentual = maior_quantidade / total * 100

    resumo.append({
        "titulo": titulo,
        "moda": " e ".join(map(str, modas)),
        "quantidade": maior_quantidade,
        "percentual": percentual
    })

    print("\n")

# ==========================================
# GERA TODAS AS ESTATÍSTICAS
# ==========================================

for indicador, titulo in INDICADORES:
    gerar_estatistica(indicador, titulo)

print("=" * 70)
print("RESUMO GERAL")
print("=" * 70)

print(f"{'INDICADOR':<18} {'VALOR':<12} {'QTDE':>8} {'%':>8}")
print("-" * 70)

for item in resumo:

    print(
        f"{item['titulo']:<18}"
        f"{item['moda']:<12}"
        f"{item['quantidade']:>8}"
        f"{item['percentual']:>8.2f}%"
    )

conn.close()    