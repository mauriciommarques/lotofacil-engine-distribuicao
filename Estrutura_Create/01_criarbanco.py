import sqlite3

DATABASE = "database/lotofacil.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# ===========================
# TABELA CONCURSOS
# ===========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS concursos (

    concurso INTEGER PRIMARY KEY,
    data TEXT,

    d01 INTEGER,
    d02 INTEGER,
    d03 INTEGER,
    d04 INTEGER,
    d05 INTEGER,
    d06 INTEGER,
    d07 INTEGER,
    d08 INTEGER,
    d09 INTEGER,
    d10 INTEGER,
    d11 INTEGER,
    d12 INTEGER,
    d13 INTEGER,
    d14 INTEGER,
    d15 INTEGER

)
""")

# ===========================
# TABELA INDICADORES
# ===========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS indicadores (

    concurso INTEGER PRIMARY KEY,

    pares INTEGER,
    impares INTEGER,

    primos INTEGER,
    fibonacci INTEGER,
    multiplos3 INTEGER,

    moldura INTEGER,
    centro INTEGER,

    linha1 INTEGER,
    linha2 INTEGER,
    linha3 INTEGER,
    linha4 INTEGER,
    linha5 INTEGER,

    coluna1 INTEGER,
    coluna2 INTEGER,
    coluna3 INTEGER,
    coluna4 INTEGER,
    coluna5 INTEGER,

    FOREIGN KEY(concurso) REFERENCES concursos(concurso)

)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso.")