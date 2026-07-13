from tkinter import *
from tkinter import ttk, colorchooser
from abc import ABC, abstractmethod


# Classe mãe

class Figura(ABC):

    def __init__(self, x, y, cor_borda, cor_preenchimento=None):
        self.x1 = self.x2 = x
        self.y1 = self.y2 = y
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def atualizar(self, x, y):
        self.x2, self.y2 = x, y

    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2

    @abstractmethod
    def desenhar(self, canvas):
        pass

    @abstractmethod
    def desenhar_preview(self, canvas):
        pass

# Subclasses de figura

class Linha(Figura):

    def desenhar(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda)

    def desenhar_preview(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                           fill=self.cor_borda, dash=(4, 2))


class Retangulo(Figura):

    def desenhar(self, canvas):
        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            outline=self.cor_borda,
            fill=self.cor_preenchimento
        )

    def desenhar_preview(self, canvas):
        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            dash=(4, 2)
        )

class Oval(Figura):

    def desenhar(self, canvas):
        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            outline=self.cor_borda,
            fill=self.cor_preenchimento
        )

    def desenhar_preview(self, canvas):
        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            dash=(4, 2)
        )

class Circulo(Figura):

    def _raio(self):
        return ((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2) ** 0.5

    def desenhar(self, canvas):
        r = self._raio()

        canvas.create_oval(
            self.x1 - r,
            self.y1 - r,
            self.x1 + r,
            self.y1 + r,
            outline=self.cor_borda,
            fill=self.cor_preenchimento
        )

    def desenhar_preview(self, canvas):
        r = self._raio()

        canvas.create_oval(
            self.x1 - r,
            self.y1 - r,
            self.x1 + r,
            self.y1 + r,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            dash=(4, 2)
        )

class Rabisco(Figura):

    def __init__(self, x, y, cor_borda):
        super().__init__(x, y, cor_borda)
        self.pontos = [(x, y)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))

    def desenhar(self, canvas):
        canvas.create_line(self.pontos, fill=self.cor_borda)

    def desenhar_preview(self, canvas):
        canvas.create_line(self.pontos, fill=self.cor_borda, dash=(4, 2))

    def incompleta(self):
        return len(self.pontos) <= 1

# Criando o editor

class EditorDesenho:

    def __init__(self):
        # Dados da aplicação
        self.figuras = []
        self.figura_nova = None

        # Configurações atuais
        self.cor_borda = "black"
        self.cor_preenchimento = None

        # Interface 
        self.root = None
        self.frame = None
        self.canvas = None
        self.tipo_figura_var = None
        self.btn_cor = None
        self.btn_preenchimento = None

        # Fábrica de figuras
        self.fabricas = {
            "Linha": lambda x, y: Linha(x, y, self.cor_borda),
            "Rabisco": lambda x, y: Rabisco(x, y, self.cor_borda),
            "Retângulo": lambda x, y: Retangulo(x, y, self.cor_borda, self.cor_preenchimento),
            "Círculo": lambda x, y: Circulo(x, y, self.cor_borda, self.cor_preenchimento),
            "Oval": lambda x, y: Oval(x, y, self.cor_borda, self.cor_preenchimento)
        }


    def desenhar(self):
        self.canvas.delete("all")

        for figura in self.figuras:
            figura.desenhar(self.canvas)

        if self.figura_nova:
            self.figura_nova.desenhar_preview(self.canvas)

    def iniciar_figura(self, event):
        tipo = self.tipo_figura_var.get()
        self.figura_nova = self.fabricas[tipo](event.x, event.y)


    def atualizar_figura(self, event):

        if self.figura_nova is None:
            return

        self.figura_nova.atualizar(event.x, event.y)
        self.desenhar()

    def finalizar_figura(self, event):

        if self.figura_nova is None:
            return

        if not self.figura_nova.incompleta():
            self.figuras.append(self.figura_nova)

        self.figura_nova = None
        self.desenhar()

    def escolher_cor_borda(self):
        cor = colorchooser.askcolor()

        if cor[1] is not None:
            self.cor_borda = cor[1]
            self.btn_cor.config(bg=self.cor_borda)

    def escolher_cor_preenchimento(self):
        cor = colorchooser.askcolor()

        if cor[1] is not None:
            self.cor_preenchimento = cor[1]
            self.btn_preenchimento.config(bg=self.cor_preenchimento)

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

        ttk.OptionMenu(
            self.frame,
            self.tipo_figura_var,
            "Linha",
            "Linha",
            "Rabisco",
            "Retângulo",
            "Círculo",
            "Oval"
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

    def executar(self):
        self.criar_interface()
        self.root.mainloop()
        

# MAIN

if __name__ == "__main__":
    editor = EditorDesenho()
    editor.executar()