import tkinter as tk
from tkinter import scrolledtext, messagebox


# ============================================================
# APOSTAS INICIAIS
# ============================================================
# COLE AQUI AS APOSTAS QUE VOCÊ QUER QUE JÁ APAREÇAM
# NA CAIXA DE ENTRADA QUANDO A APLICAÇÃO FOR ABERTA.
#
# Exemplo:
#
# Aposta 1
# 01
# 05
# 09
# 15
# 20
#
# Aposta 2
# 02
# 07
# 11
# 18
# 25
#
# ============================================================

APOSTAS_INICIAIS = """
Aposta 1
01
03
04
05
06
07
10
11
12
16
18
19
23
24
25
Aposta 2
01
03
04
06
07
10
11
12
13
14
20
21
23
24
25
Aposta 3
01
03
05
06
08
10
12
13
15
16
17
19
20
24
25
Aposta 4
01
03
04
06
08
10
11
12
13
15
19
22
23
24
25
Aposta 5
01
04
05
06
07
11
12
13
14
16
18
19
21
24
25
Aposta 6
01
03
04
06
07
10
13
14
16
17
18
21
23
24
25
Aposta 7
03
04
05
06
09
10
13
14
16
17
19
21
22
24
25
Aposta 8
03
04
05
06
10
13
14
15
16
17
19
21
22
24
25
Aposta 9
03
04
05
08
10
12
14
15
16
17
19
21
23
24
25
Aposta 10
03
04
08
11
12
14
15
16
17
19
21
22
23
24
25
Aposta 11
01
03
04
05
06
08
10
14
15
17
18
19
23
24
25
Aposta 12
05
06
09
10
11
13
14
16
17
18
20
21
23
24
25
Aposta 13
03
04
06
08
10
11
13
14
15
17
19
21
22
24
25
Aposta 14
03
04
07
09
10
12
13
14
16
17
19
20
21
24
25
Aposta 15
03
04
07
09
10
13
14
15
16
18
19
20
23
24
25
Aposta 16
01
04
06
07
09
10
11
12
13
16
17
18
21
22
23
Aposta 17
01
03
05
06
10
11
13
14
17
18
20
21
22
23
24
Aposta 18
03
04
05
06
08
11
12
14
15
16
17
19
20
21
25
Aposta 19
01
03
04
05
06
10
11
12
13
14
16
21
23
24
25
Aposta 20
01
03
04
07
10
11
12
13
14
16
17
18
21
24
25
Aposta 21
01
03
04
05
06
10
12
13
17
18
19
20
23
24
25
Aposta 22
01
04
05
06
10
11
13
14
15
16
18
19
21
23
24
Aposta 23
03
04
05
06
09
10
13
14
16
17
19
20
21
24
25
Aposta 24
03
05
06
09
10
11
13
14
16
17
18
19
22
23
24
Aposta 25
01
03
04
06
07
10
11
12
13
16
18
19
23
24
25
Aposta 26
01
03
04
07
10
12
13
15
16
18
19
22
23
24
25
Aposta 27
03
05
06
07
08
10
13
16
18
19
21
22
23
24
25
Aposta 28
01
02
03
04
06
07
09
10
16
17
18
21
22
23
25
Aposta 29
02
04
05
07
10
11
12
13
15
16
18
19
21
24
25
Aposta 30
01
03
04
08
10
11
14
15
17
18
19
21
22
23
24
Aposta 31
01
03
05
07
10
11
14
15
16
18
20
21
22
23
24
Aposta 32
03
04
05
07
09
10
13
14
16
18
20
21
23
24
25
Aposta 33
01
03
04
05
06
08
10
11
13
14
15
18
19
24
25
Aposta 34
01
03
04
05
06
08
10
11
12
14
17
21
23
24
25
Aposta 35
01
03
05
06
07
10
12
13
14
15
18
19
20
22
25
Aposta 36
02
03
04
06
08
11
13
14
15
16
19
21
23
24
25
Aposta 37
01
02
04
08
10
11
12
15
17
18
19
21
23
24
25
Aposta 38
01
03
04
06
07
10
11
13
14
15
16
21
22
23
24
Aposta 39
01
03
04
05
06
10
11
14
16
17
18
19
21
23
24
Aposta 40
02
04
05
09
10
11
12
14
15
17
18
20
21
23
25
Aposta 41
01
03
04
06
07
10
13
14
18
19
21
22
23
24
25
Aposta 42
02
03
04
05
06
09
10
11
13
14
16
17
21
24
25
Aposta 43
02
03
05
06
07
08
10
13
14
15
19
20
21
24
25
Aposta 44
03
04
05
06
08
10
11
12
15
16
17
20
21
23
25
Aposta 45
01
03
05
07
08
10
11
14
15
17
18
20
21
22
24
Aposta 46
01
03
05
06
08
11
12
13
15
16
17
20
22
23
24
Aposta 47
03
04
06
07
10
11
14
15
16
18
19
21
22
23
25
Aposta 48
01
03
04
05
06
08
10
11
12
14
17
19
21
24
25
Aposta 49
01
02
03
04
09
10
11
13
14
15
17
18
22
24
25
Aposta 50
04
05
06
08
10
11
14
15
17
18
19
21
23
24
25
Aposta 51
03
04
06
07
09
10
11
13
14
16
17
19
20
21
24
Aposta 52
01
03
04
06
07
09
12
13
14
16
17
22
23
24
25
Aposta 53
01
03
04
05
08
11
12
13
15
16
18
19
22
24
25
Aposta 54
01
02
03
04
06
07
09
10
11
12
14
16
21
23
25
Aposta 55
01
03
04
05
07
08
10
11
12
15
16
17
18
20
21
Aposta 56
01
03
05
06
08
09
10
11
13
14
16
18
19
24
25
Aposta 57
02
03
05
06
07
10
13
14
15
16
19
21
22
24
25
Aposta 58
01
03
04
06
08
11
13
14
15
18
19
20
23
24
25
Aposta 59
01
03
06
07
08
10
11
14
16
17
18
21
23
24
25
-----------------
Aposta 60
01
04
05
06
07
09
10
11
12
14
19
20
21
23
24
Aposta 61
01
03
04
07
08
10
11
12
14
17
18
21
23
24
25
Aposta 62
01
04
05
06
07
09
13
14
16
17
18
20
21
23
24
Aposta 63
01
03
04
07
08
11
12
14
15
18
19
20
23
24
25
Aposta 64
03
04
06
07
08
10
12
14
15
17
19
21
22
23
25
Aposta 65
03
04
05
08
09
11
12
14
15
16
19
20
23
24
25
Aposta 66
03
05
07
08
10
11
14
15
16
18
19
20
21
24
25
Aposta 67
03
05
06
08
10
11
13
14
16
18
19
21
23
24
25
Aposta 68
01
02
03
04
07
09
10
13
14
16
17
18
21
24
25
Aposta 69
01
03
06
07
08
09
11
14
15
16
18
19
20
22
23
Aposta 70
01
03
05
08
09
10
13
14
15
16
18
19
20
23
24
Aposta 71
01
03
06
07
08
11
12
14
15
16
18
19
20
23
25
Aposta 72
01
02
03
04
07
09
10
13
14
17
18
21
22
24
25
Aposta 73
01
03
07
08
10
11
12
14
16
18
19
21
23
24
25
Aposta 74
03
04
07
08
10
13
14
15
16
18
19
21
23
24
25
Aposta 75
01
02
03
04
06
10
11
13
14
17
18
21
23
24
25
Aposta 76
01
03
05
06
07
09
10
14
16
17
18
19
22
24
25
Aposta 77
03
05
07
08
10
12
14
15
16
17
19
21
22
24
25
Aposta 78
03
05
07
09
10
12
13
14
16
17
20
21
22
24
25
Aposta 79
01
02
03
04
07
08
09
12
13
15
16
17
19
20
24
Aposta 80
01
03
04
05
08
09
10
11
14
15
16
18
19
23
24
Aposta 81
01
03
05
06
07
09
10
12
13
14
16
19
22
24
25
Aposta 82
01
03
05
07
09
10
12
13
14
16
17
18
20
24
25
Aposta 83
05
06
07
08
10
11
13
14
15
18
20
21
23
24
25
Aposta 84
01
02
03
04
06
10
11
14
15
16
17
19
21
24
25
Aposta 85
01
03
06
07
08
10
11
14
15
16
17
19
20
21
24
Aposta 86
03
04
05
08
09
10
12
13
15
16
17
18
20
23
25
Aposta 87
03
04
05
06
08
10
11
13
16
17
18
19
21
24
25
Aposta 88
01
03
04
05
07
08
09
11
12
14
16
18
23
24
25
Aposta 89
02
04
05
06
08
09
10
13
15
16
17
19
21
24
25
Aposta 90
01
03
06
07
08
10
11
14
16
17
18
19
21
23
24
Aposta 91
01
02
06
07
09
10
11
13
14
16
18
21
23
24
25
Aposta 92
01
03
04
05
06
08
10
11
13
14
15
16
21
23
24
Aposta 93
02
03
04
05
08
09
10
11
13
14
15
16
21
23
24
Aposta 94
01
03
04
05
08
09
11
12
15
16
17
19
20
22
24
Aposta 95
01
03
04
06
07
08
10
13
14
15
17
20
21
23
24
Aposta 96
03
04
05
06
09
10
11
14
15
16
17
19
22
24
25
Aposta 97
01
03
04
05
06
08
10
11
12
14
15
19
20
21
23
Aposta 98
01
03
04
06
07
08
10
11
12
14
15
17
20
21
23
Aposta 99
01
03
04
06
08
09
10
11
14
15
16
17
19
23
24
Aposta 100
01
03
04
06
08
09
10
11
14
15
17
19
20
23
24
Aposta 101
01
03
04
07
10
11
12
14
15
16
18
19
21
22
23
Aposta 102
01
03
04
07
08
10
13
15
16
18
19
21
22
23
24
Aposta 103
02
05
07
08
09
11
12
14
15
16
17
20
21
24
25
Aposta 104
03
05
06
08
09
10
13
14
15
17
18
20
22
23
25
Aposta 105
01
05
06
08
09
11
12
13
16
18
19
20
23
24
25
Aposta 106
03
04
05
08
10
11
13
15
17
18
20
21
22
24
25
Aposta 107
01
03
04
06
07
08
09
11
12
13
14
16
23
24
25
Aposta 108
01
03
04
06
07
08
10
11
14
15
16
17
19
21
24
Aposta 109
01
03
04
05
07
09
10
11
12
14
16
19
21
22
24
Aposta 110
01
03
04
06
07
08
09
11
12
13
16
20
23
24
25
Aposta 111
01
03
05
06
08
09
10
12
13
16
17
20
23
24
25
Aposta 112
01
03
04
05
07
08
10
13
14
15
19
20
21
24
25
Aposta 113
01
04
05
07
09
10
11
13
14
15
16
18
19
24
25
Aposta 114
01
03
04
05
07
09
12
14
15
16
19
20
22
23
25
Aposta 115
03
04
05
08
09
10
11
13
14
16
17
19
21
24
25
Aposta 116
01
03
04
06
08
10
11
13
14
17
19
21
23
24
25
Aposta 117
02
03
05
07
09
10
11
13
16
18
19
22
23
24
25
Aposta 118
03
04
05
08
09
13
14
16
17
19
20
21
23
24
25
"""


# ============================================================
# ORGANIZAR APOSTAS
# ============================================================

def organizar_apostas():

    texto = entrada.get("1.0", tk.END)

    if not texto.strip():
        messagebox.showwarning(
            "Atenção",
            "Cole as apostas primeiro!"
        )
        return

    linhas = texto.strip().splitlines()

    apostas = []
    aposta_atual = []

    # ========================================================
    # LER O BLOCO
    # ========================================================

    for linha in linhas:

        linha = linha.strip()

        if not linha:
            continue

        if linha.lower().startswith("aposta"):

            if aposta_atual:
                apostas.append(aposta_atual)

            aposta_atual = []

        else:

            try:

                numero = int(linha)

                if 1 <= numero <= 25:
                    aposta_atual.append(numero)

            except ValueError:
                pass


    # Guarda a última
    if aposta_atual:
        apostas.append(aposta_atual)


    # ============================================================
    # ORDENA TODAS AS APOSTAS
    # ============================================================

    apostas = [
        sorted(aposta)
        for aposta in apostas
    ]


    # ============================================================
    # LIMPA RESULTADO
    # ============================================================

    resultado.delete(
        "1.0",
        tk.END
    )


    # ============================================================
    # MOSTRA APOSTAS ORGANIZADAS
    # ============================================================

    resultado.insert(
        tk.END,
        "APOSTAS ORGANIZADAS\n"
    )

    resultado.insert(
        tk.END,
        "=" * 90
        + "\n\n"
    )


    for numero, aposta in enumerate(
        apostas,
        start=1
    ):

        dezenas = " ".join(
            f"{n:02d}"
            for n in aposta
        )

        resultado.insert(
            tk.END,
            f"Aposta {numero} - {dezenas}\n"
        )


    # ============================================================
    # ENCONTRAR DUPLICADAS
    # ============================================================

    grupos = {}

    for numero, aposta in enumerate(
        apostas,
        start=1
    ):

        chave = tuple(aposta)

        if chave not in grupos:
            grupos[chave] = []

        grupos[chave].append(numero)


    # ============================================================
    # FILTRA SOMENTE AS DUPLICADAS
    # ============================================================

    duplicadas = {
        chave: numeros
        for chave, numeros in grupos.items()
        if len(numeros) > 1
    }


    # ============================================================
    # MOSTRA DUPLICADAS
    # ============================================================

    resultado.insert(
        tk.END,
        "\n\n"
    )

    resultado.insert(
        tk.END,
        "!" * 90
        + "\n"
    )

    resultado.insert(
        tk.END,
        "!!! APOSTAS DUPLICADAS !!!\n"
    )

    resultado.insert(
        tk.END,
        "!" * 90
        + "\n\n"
    )


    if duplicadas:

        for chave, numeros in duplicadas.items():

            nomes = "  <==== IGUAL ====>  ".join(
                f"Aposta {n}"
                for n in numeros
            )

            resultado.insert(
                tk.END,
                nomes
                + "\n"
            )

            dezenas = " ".join(
                f"{n:02d}"
                for n in chave
            )

            resultado.insert(
                tk.END,
                f"Jogo: {dezenas}\n\n"
            )

    else:

        resultado.insert(
            tk.END,
            "NENHUMA APOSTA DUPLICADA!\n"
        )


    # ============================================================
    # RESUMO
    # ============================================================

    resultado.insert(
        tk.END,
        "\n"
        + "=" * 90
        + "\n"
    )

    resultado.insert(
        tk.END,
        f"TOTAL DE APOSTAS: {len(apostas)}\n"
    )

    resultado.insert(
        tk.END,
        f"TOTAL DE JOGOS ÚNICOS: {len(grupos)}\n"
    )

    resultado.insert(
        tk.END,
        f"GRUPOS DE DUPLICADAS: {len(duplicadas)}\n"
    )


# ============================================================
# LIMPAR
# ============================================================

def limpar():

    entrada.delete(
        "1.0",
        tk.END
    )

    resultado.delete(
        "1.0",
        tk.END
    )


# ============================================================
# JANELA
# ============================================================

janela = tk.Tk()

janela.title(
    "Organizador de Apostas"
)

janela.geometry(
    "1250x850"
)


# ============================================================
# TÍTULO
# ============================================================

titulo = tk.Label(
    janela,
    text="ORGANIZADOR DE APOSTAS",
    font=("Arial", 18, "bold")
)

titulo.pack(
    pady=10
)


# ============================================================
# ENTRADA
# ============================================================

label_entrada = tk.Label(
    janela,
    text="COLE TODAS AS APOSTAS AQUI:",
    font=("Arial", 11, "bold")
)

label_entrada.pack(
    anchor="w",
    padx=15
)


entrada = scrolledtext.ScrolledText(
    janela,
    height=20,
    font=("Consolas", 10)
)

entrada.pack(
    fill="both",
    padx=15,
    pady=5
)


# ============================================================
# CARREGAR APOSTAS INICIAIS
# ============================================================

entrada.insert(
    "1.0",
    APOSTAS_INICIAIS.strip()
)


# ============================================================
# BOTÕES
# ============================================================

frame_botoes = tk.Frame(
    janela
)

frame_botoes.pack(
    pady=10
)


botao_organizar = tk.Button(
    frame_botoes,
    text="ORGANIZAR E PROCURAR DUPLICADAS",
    font=("Arial", 11, "bold"),
    command=organizar_apostas,
    padx=20,
    pady=8
)

botao_organizar.pack(
    side="left",
    padx=5
)


botao_limpar = tk.Button(
    frame_botoes,
    text="LIMPAR",
    font=("Arial", 11),
    command=limpar,
    padx=20,
    pady=8
)

botao_limpar.pack(
    side="left",
    padx=5
)


# ============================================================
# RESULTADO
# ============================================================

label_resultado = tk.Label(
    janela,
    text="RESULTADO:",
    font=("Arial", 11, "bold")
)

label_resultado.pack(
    anchor="w",
    padx=15
)


resultado = scrolledtext.ScrolledText(
    janela,
    height=20,
    font=("Consolas", 10)
)

resultado.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


# ============================================================
# INICIAR
# ============================================================

janela.mainloop()

