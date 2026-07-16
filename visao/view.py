from tkinter import *
from tkinter import ttk, colorchooser, messagebox

# Criando o editor

class View:
# Interface 
    def __init__(self):
        self.root = None
        self.frame = None
        self.canvas = None
        self.tipo_figura_var = None
        self.btn_cor = None
        self.btn_preenchimento = None


    def criar_interface(self):

        self.root = Tk()
        self.root.title("Editor de Desenhos")

        self.frame = Frame(self.root)
        self.frame.pack()

        paddings = {"padx": 5, "pady": 5}

        ttk.Label(
            self.frame,
            text="Escolha uma figura:"
        ).grid(column=0, row=0, sticky=W, **paddings)

        self.tipo_figura_var = StringVar(value="Linha")

        self.tipo_figura_var.trace_add("write", self.instrucao_poligono)


        ttk.OptionMenu(
            self.frame,
            self.tipo_figura_var,
            "Linha",
            "Linha",
            "Rabisco",
            "Retângulo",
            "Círculo",
            "Oval",
            "Poligono"
        ).grid(column=1, row=0, sticky=W, **paddings)

        self.btn_cor = Button(
            self.frame,
            text="Cor da Borda",
            command=self.escolher_cor_borda,
            bg=self.cor_borda,
            fg="white"
        )

        self.btn_cor.grid(column=0, row=1, sticky=W, **paddings)

        self.btn_preenchimento = Button(
            self.frame,
            text="Cor de Preenchimento",
            command=self.escolher_cor_preenchimento,
            bg="white"
        )

        self.btn_preenchimento.grid(column=1, row=1, sticky=W, **paddings)

        self.canvas = Canvas(
            self.frame,
            width=600,
            height=600,
            bg="white"
        )

        self.canvas.grid(column=0, row=2, columnspan=2, sticky=W, **paddings)

        self.canvas.bind("<Button-1>", self.iniciar_figura)
        self.canvas.bind("<B1-Motion>", self.atualizar_figura)
        self.canvas.bind("<ButtonRelease-1>", self.finalizar_figura)
        self.canvas.bind("<Button-3>", self.finalizar_poligono)