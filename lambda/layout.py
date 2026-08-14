# ==========================================================
# LAYOUT - VISUALIZADOR DE JOGOS LOTOFÁCIL
# ==========================================================

import tkinter as tk
from tkinter import messagebox
import boto3

from datetime import datetime
from zoneinfo import ZoneInfo


# ==========================================================
# CONFIG
# ==========================================================

REGION = "ap-east-1"
TABLE_NAME = "jogos_lotofacil"

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

table = dynamodb.Table(TABLE_NAME)


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
        response.get("Items", [])
    )

    while "LastEvaluatedKey" in response:

        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )

        itens.extend(
            response.get("Items", [])
        )

    jogos = [
        item
        for item in itens
        if item.get("data") == hoje
    ]

    jogos.sort(
        key=lambda item: item.get("sk", "")
    )

    return jogos


# ==========================================================
# APLICAÇÃO
# ==========================================================

class LayoutLotofacil:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Visualizador de Jogos - Lotofácil"
        )

        self.root.geometry("1100x850")
        self.root.minsize(900, 650)

        self.root.configure(
            bg=COR_FUNDO
        )

        self.jogos = []
        self.selecionados = set()
        self.cards_frame = None

        self.montar_tela()

        self.carregar_jogos()


    # ======================================================
    # TELA PRINCIPAL
    # ======================================================

    def montar_tela(self):

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
            text="Visualizador de Jogos - Lotofácil",
            font=("Segoe UI", 22, "bold"),
            fg=COR_TEXTO,
            bg=COR_FUNDO
        )

        titulo.pack(
            anchor="w"
        )

        self.info = tk.Label(
            header,
            text="Carregando jogos...",
            font=("Segoe UI", 11),
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
            font=("Segoe UI", 10, "bold"),
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
            font=("Segoe UI", 13),
            fg=COR_DESTAQUE,
            bg=COR_FUNDO
        ).pack(
            side="left"
        )

        tk.Label(
            legenda,
            text=" Número gerado pela engine",
            font=("Segoe UI", 10),
            fg="#665B73",
            bg=COR_FUNDO
        ).pack(
            side="left",
            padx=(2, 20)
        )

        tk.Label(
            legenda,
            text="□",
            font=("Segoe UI", 13),
            fg="#8A7D99",
            bg=COR_FUNDO
        ).pack(
            side="left"
        )

        tk.Label(
            legenda,
            text=" Número não escolhido",
            font=("Segoe UI", 10),
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

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.cards_frame,
            anchor="nw"
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
            font=("Segoe UI", 12, "bold"),
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
            text="Selecionar jogos para aposta",
            command=self.mostrar_selecionados,
            font=("Segoe UI", 10, "bold"),
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

    def carregar_jogos(self):

        try:

            self.jogos = BuscarJogos()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível consultar o DynamoDB.\n\n{erro}"
            )

            return

        self.selecionados.clear()

        for widget in self.cards_frame.winfo_children():

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
                text="Nenhum jogo encontrado para hoje.",
                font=("Segoe UI", 14),
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

        card = tk.Frame(
            self.cards_frame,
            bg=COR_CARTAO,
            highlightbackground=COR_BORDA,
            highlightthickness=1
        )

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
            command=lambda i=indice - 1, v=selecionado:
                self.alternar_selecao(i, v),
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
            font=("Segoe UI", 17, "bold"),
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

        tk.Label(
            topo,
            text=f"Concurso: {concurso}   •   Engine: {engine}",
            font=("Segoe UI", 10),
            fg="#665B73",
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

        for numero in range(1, 26):

            linha = (numero - 1) // 9
            coluna = (numero - 1) % 9

            escolhido = numero in dezenas

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
                font=("Segoe UI", 11, "bold"),
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
            font=("Segoe UI", 9),
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

        if variavel.get():

            self.selecionados.add(
                indice
            )

        else:

            self.selecionados.discard(
                indice
            )

        self.atualizar_contador()


    def atualizar_contador(self):

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

    def mostrar_selecionados(self):

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
    # SCROLL
    # ======================================================

    def atualizar_scroll(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )


    def ajustar_largura(self, event):

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
