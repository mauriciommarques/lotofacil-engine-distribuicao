import sqlite3

# ==========================================
# BANCO
# ==========================================

DATABASE = "database/lotofacil.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# ==========================================
# CONSULTA
# ==========================================

cursor.execute("""
SELECT
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
FROM indicadores
ORDER BY concurso
""")

registros = cursor.fetchall()

# ==========================================
# SAÍDA
# ==========================================

print(f"Total de registros: {len(registros)}")
print()

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

for registro in registros:

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
    ) = registro

    print(
        f"{concurso:>5} "
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

conn.close()

print()
print("Consulta realizada com sucesso.")