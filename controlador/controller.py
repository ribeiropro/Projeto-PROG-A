from tkinter import colorchooser, messagebox
import model as modelo
from view import EditorView

class EditorController:
    def __init__(self, root):
        self.root = root
        self.modelo = modelo.ModeloDesenho()
        self.view = EditorView(self.root, self)

        self.fabricas = {
            "Linha": lambda x, y: modelo.Linha(x, y, self.modelo.cor_borda),
            "Rabisco": lambda x, y: modelo.Rabisco(x, y, self.modelo.cor_borda),
            "Retângulo": lambda x, y: modelo.Retangulo(x, y, self.modelo.cor_borda, self.modelo.cor_preenchimento),
            "Círculo": lambda x, y: modelo.Circulo(x, y, self.modelo.cor_borda, self.modelo.cor_preenchimento),
            "Oval": lambda x, y: modelo.Oval(x, y, self.modelo.cor_borda, self.modelo.cor_preenchimento),
            "Poligono": lambda x, y: modelo.Poligono(x, y, self.modelo.cor_borda, self.modelo.cor_preenchimento)
        }

    def inicializar(self):
        self.view.criar_interface(self.modelo.cor_borda)

    def renderizar_tela(self):
        self.view.desenhar(self.modelo)

    def iniciar_figura(self, event):
        tipo = self.view.tipo_figura_var.get()

        if tipo == "Poligono":
            self.view.canvas.bind("<Motion>", self.atualizar_poligono)

            if self.modelo.figura_nova is None:
                self.modelo.figura_nova = modelo.Poligono(
                    event.x, event.y, self.modelo.cor_borda, self.modelo.cor_preenchimento
                )
            else:
                self.modelo.figura_nova.adicionar_ponto(event.x, event.y)
        else:
            self.view.canvas.unbind("<Motion>")
            self.modelo.figura_nova = self.fabricas[tipo](event.x, event.y)

        self.renderizar_tela()

    def atualizar_figura(self, event):
        if self.modelo.figura_nova is None:
            return

        self.modelo.figura_nova.atualizar(event.x, event.y)
        self.renderizar_tela()

    def atualizar_poligono(self, event):
        if isinstance(self.modelo.figura_nova, modelo.Poligono):
            self.modelo.figura_nova.atualizar(event.x, event.y)
            self.renderizar_tela()

    def finalizar_figura(self, event):
        if self.modelo.figura_nova is None:
            return

        if isinstance(self.modelo.figura_nova, modelo.Poligono):
            return

        if not self.modelo.figura_nova.incompleta():
            self.modelo.figuras.append(self.modelo.figura_nova)

        self.modelo.figura_nova = None
        self.renderizar_tela()

    def finalizar_poligono(self, event):
        if not isinstance(self.modelo.figura_nova, modelo.Poligono):
            return

        self.modelo.figura_nova.pontos.pop()

        if not self.modelo.figura_nova.incompleta():
            self.modelo.figuras.append(self.modelo.figura_nova)

        self.modelo.figura_nova = None
        self.renderizar_tela()

    def escolher_cor_borda(self):
        cor = colorchooser.askcolor()
        if cor[1] is not None:
            self.modelo.cor_borda = cor[1]
            self.view.btn_cor.config(bg=self.modelo.cor_borda)

    def escolher_cor_preenchimento(self):
        cor = colorchooser.askcolor()
        if cor[1] is not None:
            self.modelo.cor_preenchimento = cor[1]
            self.view.btn_preenchimento.config(bg=self.modelo.cor_preenchimento)

    def instrucao_poligono(self, *args):
        if self.view.tipo_figura_var.get() == "Poligono":
            if not self.modelo.mensagem_poligono_mostrada:
                messagebox.showinfo(
                    "Poligono", 
                    "Botão Esquerdo: Adicionar vértices.\nBotão Direito: Finalizar o polígono."
                )
                self.modelo.mensagem_poligono_mostrada = True