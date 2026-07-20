from tkinter import *
from tkinter import ttk

class EditorView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.frame = None
        self.canvas = None
        self.tipo_figura_var = None
        self.btn_cor = None
        self.btn_preenchimento = None

        self.mensagem_poligono_mostrada = False

    def criar_interface(self, cor_borda_inicial):
        self.frame = Frame(self.root)
        self.frame.pack()

        paddings = {"padx": 5, "pady": 5}

        ttk.Label(
            self.frame,
            text="Escolha uma figura:"
        ).grid(column=0, row=0, sticky=W, **paddings)

        self.tipo_figura_var = StringVar(value="Linha")
        self.tipo_figura_var.trace_add("write", self.controller.instrucao_poligono)

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
            command=self.controller.escolher_cor_borda,
            bg=cor_borda_inicial,
            fg="white"
        )
        self.btn_cor.grid(column=0, row=1, sticky=W, **paddings)

        self.btn_preenchimento = Button(
            self.frame,
            text="Cor de Preenchimento",
            command=self.controller.escolher_cor_preenchimento,
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

        self.canvas.bind("<Button-1>", self.controller.iniciar_figura)
        self.canvas.bind("<B1-Motion>", self.controller.atualizar_figura)
        self.canvas.bind("<ButtonRelease-1>", self.controller.finalizar_figura)
        self.canvas.bind("<Button-3>", self.controller.finalizar_poligono)

        self.btn_salvar = Button(self.frame, text="Salvar Projeto", command=self.controller.salvar_projeto, bg ='white')
        self.btn_salvar.grid(column=0, row=3, sticky=W, **paddings)

        self.btn_carregar = Button(self.frame, text="Carregar Projeto", command= None, bg ='white')
        self.btn_carregar.grid(column=1, row=3, sticky=W, **paddings)

    def desenhar(self, modelo):
        self.canvas.delete("all")

        for figura in modelo.figuras:
            figura.desenhar(self.canvas)

        if modelo.figura_nova:
            modelo.figura_nova.desenhar_preview(self.canvas)