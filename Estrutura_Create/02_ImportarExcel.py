import sqlite3
import pandas as pd

# ==========================================
# CONFIGURAÇÕES
# ==========================================

ARQUIVO_EXCEL = "database/2026_07.xlsx"
DATABASE = "database/lotofacil.db"

# ==========================================
# CONEXÃO
# ==========================================

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# ==========================================
# LEITURA DO EXCEL
# ==========================================

df = pd.read_excel(ARQUIVO_EXCEL, header=6)

print("=" * 60)
print("IMPORTAÇÃO DE CONCURSOS")
print("=" * 60)
print(f"Arquivo........: {ARQUIVO_EXCEL}")
print(f"Concursos XLS..: {len(df)}")
print()

# ==========================================
# CONTADORES
# ==========================================

importados = 0
existentes = 0
erros = 0

# ==========================================
# IMPORTAÇÃO
# ==========================================

for _, linha in df.iterrows():

    concurso = int(linha["Concurso"])

    # Verifica se já existe
    cursor.execute(
        "SELECT 1 FROM concursos WHERE concurso = ?",
        (concurso,)
    )

    if cursor.fetchone():

        existentes += 1
        print(f"[IGNORADO] Concurso {concurso} já existe.")

        continue

    try:

        cursor.execute("""
            INSERT INTO concursos
            (
                concurso,
                data,
                d01,d02,d03,d04,d05,
                d06,d07,d08,d09,d10,
                d11,d12,d13,d14,d15
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            concurso,
            str(linha["Data"]),

            int(linha["bola 1"]),
            int(linha["bola 2"]),
            int(linha["bola 3"]),
            int(linha["bola 4"]),
            int(linha["bola 5"]),
            int(linha["bola 6"]),
            int(linha["bola 7"]),
            int(linha["bola 8"]),
            int(linha["bola 9"]),
            int(linha["bola 10"]),
            int(linha["bola 11"]),
            int(linha["bola 12"]),
            int(linha["bola 13"]),
            int(linha["bola 14"]),
            int(linha["bola 15"])
        ))

        importados += 1

        print(f"[OK] Concurso {concurso} importado.")

    except Exception as erro:

        erros += 1

        print(f"[ERRO] Concurso {concurso}")
        print(erro)

# ==========================================
# FINALIZAÇÃO
# ==========================================

conn.commit()
conn.close()

print()
print("=" * 60)
print("RESUMO")
print("=" * 60)

print(f"Novos importados : {importados}")
print(f"Já existentes    : {existentes}")
print(f"Erros            : {erros}")

print("=" * 60)
print("Importação concluída.")
print("=" * 60)