# ============================================================
# EXPERIMENTO ALEATÓRIO - LOTOFÁCIL
# ============================================================
#
# OBJETIVO:
#   Testar diferentes quantidades de jogos ao longo de vários dias.
#
# CORTE DO MODELO:
#   Concurso: 3779
#   Data:     03/09/2026
#
# EXPERIMENTO:
#   Início: 07/09/2026
#
# ============================================================

from datetime import date, timedelta


# ============================================================
# ===================== CONFIGURAÇÃO =========================
# ============================================================

# >>> QUANTOS DIAS TERÁ O EXPERIMENTO <<<
DIAS_EXPERIMENTO = 7


# >>> QUANTOS JOGOS SERÃO FEITOS EM CADA DIA <<<
#
# DIA 1 = primeira posição
# DIA 2 = segunda posição
# DIA 3 = terceira posição
# etc.
#
# É AQUI QUE VOCÊ VAI MUDAR A QUANTIDADE DE JOGOS.
#
JOGOS_POR_DIA = [
    20,   # Dia 1
    30,   # Dia 2
    40,   # Dia 3
    50,   # Dia 4
    60,   # Dia 5
    70,   # Dia 6
    80    # Dia 7
]


# ============================================================
# ====================== CORTE HISTÓRICO =====================
# ============================================================

# >>> NÃO ALTERAR DURANTE O EXPERIMENTO <<<
#
# Este é o último concurso utilizado para congelar o modelo.
#
CONCURSO_CORTE = 3779
DATA_CORTE = "03/09/2026"


# ============================================================
# ===================== INÍCIO DO TESTE ======================
# ============================================================

# >>> DATA EM QUE COMEÇOU O EXPERIMENTO <<<
#
# Para este experimento:
#
# 07/09/2026 = Dia 1
# 08/09/2026 = Dia 2
# 09/09/2026 = Dia 3
# etc.
#
DATA_INICIO = date(2026, 9, 7)


# >>> NOME DO EXPERIMENTO <<<
NOME_EXPERIMENTO = "EXPERIMENTO_7_DIAS"


# ============================================================
# ====================== VALIDAÇÕES ==========================
# ============================================================

if DIAS_EXPERIMENTO <= 0:
    raise ValueError(
        "DIAS_EXPERIMENTO deve ser maior que zero."
    )


if len(JOGOS_POR_DIA) != DIAS_EXPERIMENTO:
    raise ValueError(
        f"DIAS_EXPERIMENTO = {DIAS_EXPERIMENTO}, "
        f"mas JOGOS_POR_DIA possui "
        f"{len(JOGOS_POR_DIA)} valores."
    )


if any(int(qtd) <= 0 for qtd in JOGOS_POR_DIA):
    raise ValueError(
        "Todos os valores de JOGOS_POR_DIA devem ser maiores que zero."
    )


# ============================================================
# ====================== FUNÇÕES =============================
# ============================================================

def obter_dia_experimento():

    hoje = date.today()

    diferenca = (hoje - DATA_INICIO).days

    dia = diferenca + 1

    return dia


def obter_configuracao_do_dia(dia):

    if dia < 1 or dia > DIAS_EXPERIMENTO:
        return None

    return JOGOS_POR_DIA[dia - 1]


def GerarJogos(quantidade):

    print()
    print("=" * 65)
    print("GERAÇÃO DE JOGOS")
    print("=" * 65)

    print(
        f"Quantidade de jogos solicitada: {quantidade}"
    )

    # ========================================================
    # POR ENQUANTO:
    # SOMENTE PRINT EM TELA.
    #
    # AQUI VAMOS CONECTAR SUA ENGINE DE GERAÇÃO DE JOGOS.
    # ========================================================

    jogos = []

    return jogos


# ============================================================
# ======================== EXECUÇÃO ==========================
# ============================================================

def main():

    dia = obter_dia_experimento()

    hoje = date.today()

    print()
    print("=" * 65)
    print(f"       {NOME_EXPERIMENTO}")
    print("=" * 65)

    print()
    print("CORTE DO MODELO")
    print("-" * 65)

    print(
        f"Concurso congelado : {CONCURSO_CORTE}"
    )

    print(
        f"Data do corte      : {DATA_CORTE}"
    )

    print()
    print("EXPERIMENTO")
    print("-" * 65)

    print(
        f"Data de início     : "
        f"{DATA_INICIO.strftime('%d/%m/%Y')}"
    )

    print(
        f"Data de hoje       : "
        f"{hoje.strftime('%d/%m/%Y')}"
    )

    print(
        f"Dia do experimento : "
        f"{dia} / {DIAS_EXPERIMENTO}"
    )


    # ========================================================
    # VERIFICA SE O EXPERIMENTO JÁ TERMINOU
    # ========================================================

    if dia < 1:

        print()
        print(
            "O experimento ainda não começou."
        )
        print()

        return


    if dia > DIAS_EXPERIMENTO:

        print()
        print("=" * 65)
        print("EXPERIMENTO ENCERRADO")
        print("=" * 65)

        print()
        print(
            f"O experimento terminou após "
            f"{DIAS_EXPERIMENTO} dias."
        )

        print()

        return


    # ========================================================
    # CONFIGURAÇÃO DO DIA
    # ========================================================

    quantidade = obter_configuracao_do_dia(dia)

    data_dia = (
        DATA_INICIO
        + timedelta(days=dia - 1)
    )


    print()
    print("-" * 65)
    print("CONFIGURAÇÃO DO DIA")
    print("-" * 65)

    print(
        f"Dia                : {dia}"
    )

    print(
        f"Data               : "
        f"{data_dia.strftime('%d/%m/%Y')}"
    )

    print(
        f"Jogos planejados   : {quantidade}"
    )


    # ========================================================
    # PLANEJAMENTO COMPLETO
    # ========================================================

    print()
    print("-" * 65)
    print("PLANEJAMENTO DO EXPERIMENTO")
    print("-" * 65)

    for numero_dia, qtd in enumerate(
        JOGOS_POR_DIA,
        start=1
    ):

        data = (
            DATA_INICIO
            + timedelta(days=numero_dia - 1)
        )

        marcador = ""

        if numero_dia == dia:
            marcador = "  <<< HOJE"


        print(
            f"Dia {numero_dia:02d} | "
            f"{data.strftime('%d/%m/%Y')} | "
            f"{qtd:03d} jogos"
            f"{marcador}"
        )


    # ========================================================
    # GERAÇÃO
    # ========================================================

    jogos = GerarJogos(quantidade)


    print()
    print("-" * 65)
    print("RESULTADO DA EXECUÇÃO")
    print("-" * 65)

    print(
        f"Jogos planejados   : {quantidade}"
    )

    print(
        f"Jogos gerados      : {len(jogos)}"
    )


    if len(jogos) == 0:

        print()
        print(
            "ATENÇÃO:"
        )

        print(
            "A engine de geração ainda não foi conectada."
        )

        print(
            "Por enquanto o programa está apenas "
            "controlando o experimento."
        )


    print()
    print("=" * 65)
    print("EXPERIMENTO ATIVO")
    print("=" * 65)
    print()


# ============================================================
# ========================== MAIN =============================
# ============================================================

if __name__ == "__main__":
    main()