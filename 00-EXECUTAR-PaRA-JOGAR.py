# ==========================================================
# LAYOUT - VISUALIZADOR E APOSTAS LOTOFÁCIL
# ==========================================================

import tkinter as tk
from tkinter import messagebox

import boto3

from datetime import datetime
from zoneinfo import ZoneInfo

import time

from playwright.sync_api import sync_playwright


# ==========================================================
# CONFIG
# ==========================================================

REGION = "ap-east-1"

TABLE_NAME = "jogos_lotofacil"

PLAYWRIGHT_USER_DATA = (
    r"C:\Users\Mauricio\.playwright\lotofacil"
)

URL_LOTOFACIL = (
    "https://www.sorteonline.com.br/"
    "lotofacil/faca-seu-jogo/3763"
)


# ==========================================================
# CORES
# ==========================================================

COR_DESTAQUE = "#7B3FE4"

COR_FUNDO = "#F7F5FA"

COR_CARTAO = "#FFFFFF"

COR_TEXTO = "#2E2340"

COR_BORDA = "#DDD6E8"

COR_VAZIO = "#FFFFFF"


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


# ==========================================================
# BUSCAR JOGOS
# ==========================================================

def BuscarJogos():

    hoje = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    ).strftime("%Y-%m-%d")

    itens = []

    response = table.scan()

    itens.extend(
        response.get(
            "Items",
            []
        )
    )

    while "LastEvaluatedKey" in response:

        response = table.scan(
            ExclusiveStartKey=response[
                "LastEvaluatedKey"
            ]
        )

        itens.extend(
            response.get(
                "Items",
                []
            )
        )

    jogos = [

        item

        for item in itens

        if item.get("data") == hoje

    ]

    jogos.sort(
        key=lambda item: item.get(
            "sk",
            ""
        )
    )

    return jogos


# ==========================================================
# LIMPAR JOGOS DO DYNAMODB
# ==========================================================

def limpar_jogos(jogos):

    print()
    print("=" * 60)
    print("LIMPANDO JOGOS DO DYNAMODB")
    print("=" * 60)

    total = 0

    for jogo in jogos:

        pk = jogo.get("pk")
        sk = jogo.get("sk")

        if not pk or not sk:

            print(
                "Jogo ignorado: PK ou SK não encontrado."
            )

            continue

        table.delete_item(
            Key={
                "pk": pk,
                "sk": sk
            }
        )

        total += 1

        print(
            f"Removido: {sk}"
        )

    print()
    print(
        f"{total} jogo(s) removido(s) com sucesso."
    )

    return total


# ==========================================================
# APOSTAR NO SITE
# ==========================================================

def apostar(
    page,
    jogo
):

    dezenas = jogo.get(
        "jogo",
        []
    )

    print()
    print("=" * 50)
    print("MARCANDO DEZENAS")
    print("=" * 50)

    print(
        "Concurso :",
        jogo.get(
            "concurso",
            "-"
        )
    )

    print(
        "Data     :",
        jogo.get(
            "data",
            "-"
        )
    )

    print()

    # ------------------------------------------------------
    # MARCAR DEZENAS
    # ------------------------------------------------------

    for numero in dezenas:

        numero = int(numero)

        texto = f"{numero:02d}"

        print(
            "Marcando",
            texto
        )

        botao_numero = page.get_by_test_id(
            f"number-button-{numero}"
        )

        botao_numero.wait_for()

        botao_numero.click()

        time.sleep(1)

    # ------------------------------------------------------
    # AGUARDAR VALIDAÇÃO
    # ------------------------------------------------------

    print()

    print(
        "Aguardando validação do volante..."
    )

    time.sleep(2)

    # ------------------------------------------------------
    # INCLUIR APOSTA
    # ------------------------------------------------------

    botao = page.get_by_role(
        "button",
        name="Incluir aposta",
        exact=True
    )

    botao.wait_for()

    print(
        "Incluindo aposta no carrinho..."
    )

    botao.click()

    time.sleep(3)

    print(
        "Aposta incluída no carrinho."
    )


# ==========================================================
# APLICAÇÃO
# ==========================================================

class LayoutLotofacil:

    def __init__(
        self,
        root
    ):

        self.root = root

        self.root.title(
            "Visualizador de Jogos - Lotofácil"
        )

        self.root.geometry(
            "1100x850"
        )

        self.root.minsize(
            900,
            650
        )

        self.root.configure(
            bg=COR_FUNDO
        )

        self.jogos = []

        self.selecionados = set()

        self.cards = {}        

        self.cards_frame = None

        self.montar_tela()

        self.carregar_jogos()


    # ======================================================
    # TELA PRINCIPAL
    # ======================================================

    def montar_tela(
        self
    ):

        # --------------------------------------------------
        # CABEÇALHO
        # --------------------------------------------------

        header = tk.Frame(
            self.root,
            bg=COR_FUNDO
        )

        header.pack(
            fill="x",
            padx=28,
            pady=(22, 10)
        )

        titulo = tk.Label(
            header,
            text=(
                "Visualizador de Jogos - Lotofácil"
            ),
            font=(
                "Segoe UI",
                22,
                "bold"
            ),
            fg=COR_TEXTO,
            bg=COR_FUNDO
        )

        titulo.pack(
            anchor="w"
        )

        self.info = tk.Label(
            header,
            text="Carregando jogos...",
            font=(
                "Segoe UI",
                11
            ),
            fg="#665B73",
            bg=COR_FUNDO
        )

        self.info.pack(
            anchor="w",
            pady=(6, 0)
        )


        # --------------------------------------------------
        # BARRA DE AÇÕES
        # --------------------------------------------------

        actions = tk.Frame(
            self.root,
            bg=COR_FUNDO
        )

        actions.pack(
            fill="x",
            padx=28,
            pady=(0, 10)
        )

        botao_atualizar = tk.Button(
            actions,
            text="⟳  Atualizar",
            command=self.carregar_jogos,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            bg=COR_CARTAO,
            fg=COR_TEXTO,
            activebackground="#EEE8F7",
            relief="solid",
            bd=1,
            padx=15,
            pady=7,
            cursor="hand2"
        )

        botao_atualizar.pack(
            side="right"
        )


        # --------------------------------------------------
        # LEGENDA
        # --------------------------------------------------

        legenda = tk.Frame(
            self.root,
            bg=COR_FUNDO
        )

        legenda.pack(
            fill="x",
            padx=28,
            pady=(0, 12)
        )

        tk.Label(
            legenda,
            text="■",
            font=(
                "Segoe UI",
                13
            ),
            fg=COR_DESTAQUE,
            bg=COR_FUNDO
        ).pack(
            side="left"
        )

        tk.Label(
            legenda,
            text=(
                " Número gerado pela engine"
            ),
            font=(
                "Segoe UI",
                10
            ),
            fg="#665B73",
            bg=COR_FUNDO
        ).pack(
            side="left",
            padx=(2, 20)
        )

        tk.Label(
            legenda,
            text="□",
            font=(
                "Segoe UI",
                13
            ),
            fg="#8A7D99",
            bg=COR_FUNDO
        ).pack(
            side="left"
        )

        tk.Label(
            legenda,
            text=(
                " Número não escolhido"
            ),
            font=(
                "Segoe UI",
                10
            ),
            fg="#665B73",
            bg=COR_FUNDO
        ).pack(
            side="left",
            padx=2
        )


        # --------------------------------------------------
        # ÁREA ROLÁVEL
        # --------------------------------------------------

        container = tk.Frame(
            self.root,
            bg=COR_FUNDO
        )

        container.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=(0, 10)
        )

        self.canvas = tk.Canvas(
            container,
            bg=COR_FUNDO,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.cards_frame = tk.Frame(
            self.canvas,
            bg=COR_FUNDO
        )

        self.canvas_window = (
            self.canvas.create_window(
                (0, 0),
                window=self.cards_frame,
                anchor="nw"
            )
        )

        self.cards_frame.bind(
            "<Configure>",
            self.atualizar_scroll
        )

        self.canvas.bind(
            "<Configure>",
            self.ajustar_largura
        )


        # --------------------------------------------------
        # RODAPÉ
        # --------------------------------------------------

        footer = tk.Frame(
            self.root,
            bg=COR_CARTAO,
            highlightbackground=COR_BORDA,
            highlightthickness=1
        )

        footer.pack(
            fill="x",
            padx=28,
            pady=(0, 20)
        )

        self.selecao_label = tk.Label(
            footer,
            text="0 jogos selecionados",
            font=(
                "Segoe UI",
                12,
                "bold"
            ),
            fg=COR_TEXTO,
            bg=COR_CARTAO
        )

        self.selecao_label.pack(
            side="left",
            padx=18,
            pady=14
        )

        self.apostar_button = tk.Button(
            footer,
            text="Enviar selecionados para aposta",
            command=self.executar_apostas,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            bg=COR_DESTAQUE,
            fg="white",
            activebackground="#6930C3",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=9,
            cursor="hand2"
        )

        self.apostar_button.pack(
            side="right",
            padx=18,
            pady=10
        )


    # ======================================================
    # JOGOS
    # ======================================================

    def carregar_jogos(
        self
    ):

        try:

            self.jogos = BuscarJogos()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível consultar "
                    f"o DynamoDB.\n\n{erro}"
                )
            )

            return

        self.selecionados.clear()

        self.cards.clear()

        for widget in (
            self.cards_frame.winfo_children()
        ):

            widget.destroy()


        self.info.config(
            text=(
                f"Jogos de hoje: {len(self.jogos)}"
                "   •   Fonte: jogos_lotofacil"
            )
        )

        if not self.jogos:

            tk.Label(
                self.cards_frame,
                text=(
                    "Nenhum jogo encontrado "
                    "para hoje."
                ),
                font=(
                    "Segoe UI",
                    14
                ),
                fg="#665B73",
                bg=COR_FUNDO
            ).pack(
                pady=50
            )

            self.atualizar_contador()

            return

        for indice, jogo in enumerate(
            self.jogos,
            start=1
        ):

            self.criar_card(
                indice,
                jogo
            )

        self.atualizar_contador()


    # ======================================================
    # CARD
    # ======================================================

    def criar_card(
        self,
        indice,
        jogo
    ):


        engine = jogo.get(
            "engine",
            "-"
        )

        if engine == "ENGINE":
            cor_borda = COR_DESTAQUE
            espessura_borda = 2
            fundo_card = "#F8F3FF"
        else:
            cor_borda = COR_BORDA
            espessura_borda = 1
            fundo_card = COR_CARTAO

        card = tk.Frame(
            self.cards_frame,
            bg=fundo_card,
            highlightbackground=cor_borda,
            highlightthickness=espessura_borda
        )        

        self.cards[indice - 1] = card        

        card.pack(
            fill="x",
            pady=(0, 14)
        )


        # --------------------------------------------------
        # CABEÇALHO DO CARD
        # --------------------------------------------------

        topo = tk.Frame(
            card,
            bg=COR_CARTAO
        )

        topo.pack(
            fill="x",
            padx=18,
            pady=(15, 8)
        )

        selecionado = tk.BooleanVar(
            value=False
        )

        checkbox = tk.Checkbutton(
            topo,
            variable=selecionado,
            command=(
                lambda i=indice - 1,
                v=selecionado:
                self.alternar_selecao(
                    i,
                    v
                )
            ),
            bg=COR_CARTAO,
            activebackground=COR_CARTAO,
            selectcolor=COR_DESTAQUE,
            bd=0,
            highlightthickness=0,
            cursor="hand2"
        )

        checkbox.pack(
            side="left"
        )

        tk.Label(
            topo,
            text=f"Jogo {indice:02d}",
            font=(
                "Segoe UI",
                17,
                "bold"
            ),
            fg=COR_DESTAQUE,
            bg=COR_CARTAO
        ).pack(
            side="left",
            padx=(4, 12)
        )

        concurso = jogo.get(
            "concurso",
            "-"
        )

        engine = jogo.get(
            "engine",
            "-"
        )


        # --------------------------------------------------
        # IDENTIFICAÇÃO DA ENGINE
        # --------------------------------------------------

        if engine == "ENGINE":
            texto_engine = "★ ENGINE 1 • ORIGINAL"
            cor_engine = COR_DESTAQUE
            fonte_engine = (
                "Segoe UI",
                11,
                "bold"
            )

        elif engine == "ENGINE-02":
            texto_engine = "ENGINE 2"
            cor_engine = "#665B73"
            fonte_engine = (
                "Segoe UI",
                10,
                "bold"
            )

        elif engine == "ENGINE-03":
            texto_engine = "ENGINE 3"
            cor_engine = "#665B73"
            fonte_engine = (
                "Segoe UI",
                10,
                "bold"
            )

        else:
            texto_engine = f"ENGINE: {engine}"
            cor_engine = "#665B73"
            fonte_engine = (
                "Segoe UI",
                10
            )

        tk.Label(
            topo,
            text=(
                f"Concurso: {concurso}"
                f"   •   {texto_engine}"
            ),
            font=fonte_engine,
            fg=cor_engine,
            bg=COR_CARTAO
        ).pack(
            side="left"
        )        

        # --------------------------------------------------
        # GRADE DE DEZENAS
        # --------------------------------------------------

        grade = tk.Frame(
            card,
            bg=COR_CARTAO
        )

        grade.pack(
            anchor="w",
            padx=30,
            pady=(2, 18)
        )

        dezenas = set(
            int(numero)
            for numero in jogo.get(
                "jogo",
                []
            )
        )

        for numero in range(
            1,
            26
        ):

            linha = (
                numero - 1
            ) // 9

            coluna = (
                numero - 1
            ) % 9

            escolhido = (
                numero in dezenas
            )

            if escolhido:

                bg = COR_DESTAQUE
                fg = "white"

            else:

                bg = COR_VAZIO
                fg = COR_TEXTO

            numero_label = tk.Label(
                grade,
                text=f"{numero:02d}",
                width=4,
                height=1,
                font=(
                    "Segoe UI",
                    11,
                    "bold"
                ),
                bg=bg,
                fg=fg,
                relief="solid",
                bd=1,
                highlightbackground=(
                    COR_DESTAQUE
                    if escolhido
                    else COR_BORDA
                )
            )

            numero_label.grid(
                row=linha,
                column=coluna,
                padx=3,
                pady=3
            )


        # --------------------------------------------------
        # INFORMAÇÕES DA ENGINE
        # --------------------------------------------------

        detalhes = tk.Frame(
            card,
            bg=COR_CARTAO
        )

        detalhes.pack(
            fill="x",
            padx=30,
            pady=(0, 16)
        )

        fixos = jogo.get(
            "fixos",
            []
        )

        universo = jogo.get(
            "universo",
            []
        )

        tk.Label(
            detalhes,
            text=(
                f"15 dezenas   •   "
                f"Fixos: {len(fixos)}   •   "
                f"Universo: {len(universo)}"
            ),
            font=(
                "Segoe UI",
                9
            ),
            fg="#776A84",
            bg=COR_CARTAO
        ).pack(
            anchor="w"
        )


    # ======================================================
    # SELEÇÃO
    # ======================================================

    def alternar_selecao(
        self,
        indice,
        variavel
    ):

        card = self.cards.get(indice)

        if variavel.get():

            self.selecionados.add(
                indice
            )

            if card:
                card.config(
                    bg="#F1E9FC",
                    highlightbackground=COR_DESTAQUE,
                    highlightthickness=2
                )

        else:

            self.selecionados.discard(
                indice
            )

            if card:
                card.config(
                    bg=COR_CARTAO,
                    highlightbackground=COR_BORDA,
                    highlightthickness=1
                )

        self.atualizar_contador()

    # ======================================================
    # CONTADOR
    # ======================================================

    def atualizar_contador(
        self
    ):

        quantidade = len(
            self.selecionados
        )

        self.selecao_label.config(
            text=(
                f"{quantidade} "
                f"jogo"
                f"{'' if quantidade == 1 else 's'} "
                f"selecionado"
                f"{'' if quantidade == 1 else 's'}"
            )
        )


    # ======================================================
    # CONFIRMAÇÃO VISUAL
    # ======================================================

    def mostrar_selecionados(
        self
    ):

        if not self.selecionados:

            messagebox.showinfo(
                "Seleção",
                "Nenhum jogo foi selecionado."
            )

            return

        jogos = [
            self.jogos[indice]
            for indice in sorted(
                self.selecionados
            )
        ]

        linhas = []

        for indice, jogo in enumerate(
            jogos,
            start=1
        ):

            dezenas = ", ".join(
                f"{int(numero):02d}"
                for numero in jogo.get(
                    "jogo",
                    []
                )
            )

            linhas.append(
                f"Jogo {indice:02d}: {dezenas}"
            )

        messagebox.showinfo(
            "Jogos selecionados",
            "Jogos escolhidos:\n\n"
            + "\n".join(linhas)
        )


    # ======================================================
    # EXECUTAR APOSTAS
    # ======================================================

    def executar_apostas(
        self
    ):

        # --------------------------------------------------
        # VERIFICAR SE EXISTEM JOGOS SELECIONADOS
        # --------------------------------------------------

        if not self.selecionados:

            messagebox.showinfo(
                "Apostas",
                "Nenhum jogo foi selecionado."
            )

            return


        # --------------------------------------------------
        # PEGAR SOMENTE OS JOGOS SELECIONADOS
        # --------------------------------------------------

        jogos = [
            self.jogos[indice]
            for indice in sorted(
                self.selecionados
            )
        ]


        # --------------------------------------------------
        # CONFIRMAR
        # --------------------------------------------------

        confirmacao = messagebox.askyesno(
            "Confirmar apostas",
            (
                f"{len(jogos)} jogo(s) serão "
                "enviados para o carrinho.\n\n"
                "Deseja continuar?"
            )
        )

        if not confirmacao:

            return


        # --------------------------------------------------
        # DESABILITAR BOTÃO
        # --------------------------------------------------

        self.apostar_button.config(
            state="disabled",
            text="Enviando apostas..."
        )

        self.root.update()


        # --------------------------------------------------
        # AUTOMATIZAÇÃO
        # --------------------------------------------------

        try:

            with sync_playwright() as p:

                print()
                print("=" * 60)
                print("ABRINDO SORTE ONLINE")
                print("=" * 60)

                context = (
                    p.chromium.launch_persistent_context(
                        user_data_dir=PLAYWRIGHT_USER_DATA,
                        channel="chrome",
                        headless=False
                    )
                )

                page = context.new_page()


                # ------------------------------------------
                # ABRIR SITE
                # ------------------------------------------

                print(
                    "Abrindo Lotofácil..."
                )

                page.goto(
                    URL_LOTOFACIL,
                    wait_until="domcontentloaded"
                )

                print(
                    "Página carregada."
                )

                time.sleep(5)


                # ------------------------------------------
                # ENVIAR JOGOS
                # ------------------------------------------

                total = len(jogos)

                for indice, jogo in enumerate(
                    jogos,
                    start=1
                ):

                    self.info.config(
                        text=(
                            f"Enviando jogo "
                            f"{indice} de {total}..."
                        )
                    )

                    self.root.update()

                    print()
                    print("=" * 60)
                    print(
                        f"JOGO SELECIONADO "
                        f"{indice} DE {total}"
                    )
                    print("=" * 60)

                    apostar(
                        page,
                        jogo
                    )


                # ------------------------------------------
                # TODOS ENVIADOS
                # ------------------------------------------

                self.info.config(
                    text=(
                        f"{total} jogo(s) "
                        "enviado(s) para o carrinho."
                    )
                )

                self.root.update()

                print()
                print("=" * 60)
                print(
                    "TODOS OS JOGOS FORAM ENVIADOS"
                )
                print("=" * 60)


                # ------------------------------------------
                # CONFIRMAÇÃO
                # ------------------------------------------

                messagebox.showinfo(
                    "Apostas",
                    (
                        f"{total} jogo(s) foram "
                        "adicionados ao carrinho.\n\n"
                        "O navegador continuará aberto "
                        "para você revisar."
                    )
                )


                # ------------------------------------------
                # LIMPAR DYNAMODB
                # ------------------------------------------
                #
                # IMPORTANTE:
                # A pergunta acontece ANTES de esperar
                # o fechamento do navegador.
                #

                resposta = messagebox.askyesno(
                    "Aposta realizada",
                    (
                        f"{total} jogo(s) foram "
                        "enviados para o carrinho.\n\n"
                        "Deseja limpar esses jogos "
                        "do DynamoDB?"
                    )
                )


                if resposta:

                    try:

                        quantidade_removida = (
                            limpar_jogos(jogos)
                        )

                        self.info.config(
                            text=(
                                f"{quantidade_removida} "
                                "jogo(s) removido(s) "
                                "do DynamoDB."
                            )
                        )

                        self.root.update()

                        messagebox.showinfo(
                            "Banco de dados",
                            (
                                f"{quantidade_removida} "
                                "jogo(s) apostado(s) "
                                "foram removidos "
                                "do DynamoDB."
                            )
                        )

                    except Exception as erro:

                        messagebox.showerror(
                            "Erro ao limpar banco",
                            (
                                "Os jogos foram enviados "
                                "ao carrinho, porém ocorreu "
                                "um erro ao limpar o "
                                f"DynamoDB:\n\n{erro}"
                            )
                        )

                else:

                    messagebox.showinfo(
                        "Banco de dados",
                        (
                            "Os jogos foram mantidos "
                            "no DynamoDB."
                        )
                    )


                # ------------------------------------------
                # LIMPAR SELEÇÃO DA INTERFACE
                # ------------------------------------------

                self.selecionados.clear()

                self.atualizar_contador()


                # ------------------------------------------
                # NAVEGADOR CONTINUA ABERTO
                # ------------------------------------------

                print()
                print(
                    "Navegador permanece aberto."
                )

                print(
                    "Revise o carrinho e finalize "
                    "a compra manualmente."
                )

                print(
                    "Feche o navegador quando terminar."
                )


                # ------------------------------------------
                # AGUARDAR FECHAMENTO
                # ------------------------------------------

                page.wait_for_event(
                    "close",
                    timeout=0
                )


        except Exception as erro:

            print()
            print("=" * 60)
            print("ERRO NA AUTOMAÇÃO")
            print("=" * 60)

            print(
                erro
            )

            messagebox.showerror(
                "Erro na aposta",
                (
                    "Ocorreu um erro durante "
                    f"a automação:\n\n{erro}"
                )
            )


        finally:

            self.apostar_button.config(
                state="normal",
                text="Enviar selecionados para aposta"
            )

            self.root.update()


    # ======================================================
    # SCROLL
    # ======================================================

    def atualizar_scroll(
        self,
        event=None
    ):

        self.canvas.configure(
            scrollregion=self.canvas.bbox(
                "all"
            )
        )


    # ======================================================
    # AJUSTAR LARGURA
    # ======================================================

    def ajustar_largura(
        self,
        event
    ):

        self.canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = LayoutLotofacil(
        root
    )

    root.mainloop()