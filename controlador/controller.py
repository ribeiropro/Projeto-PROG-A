from view import View
import model

class Controller:

    def __init__(self):
        self.view = View()

        # Dados da aplicação
        self.figuras = []
        self.figura_nova = None

        #Mensagem
        self.mensagem_poligono_mostrada = False

        # Configurações atuais
        self.cor_borda = "black"
        self.cor_preenchimento = None

        # Fábrica de figuras
        self.fabricas = {
            "Linha": lambda x, y: model.Linha(x, y, self.cor_borda),
            "Rabisco": lambda x, y: model.Rabisco(x, y, self.cor_borda),
            "Retângulo": lambda x, y: model.Retangulo(x, y, self.cor_borda, self.cor_preenchimento),
            "Círculo": lambda x, y: model.Circulo(x, y, self.cor_borda, self.cor_preenchimento),
            "Oval": lambda x, y: model.Oval(x, y, self.cor_borda, self.cor_preenchimento),
            "Poligono": lambda x, y: model.Poligono(x, y, self.cor_borda, self.cor_preenchimento)
        }


    def desenhar(self):
        self.canvas.delete("all")

        for figura in self.figuras:
            figura.desenhar(self.canvas)

        if self.figura_nova:
            self.figura_nova.desenhar_preview(self.canvas)

    def iniciar_figura(self, event):
        tipo = self.tipo_figura_var.get()

        if tipo == "Poligono":

            self.canvas.bind("<Motion>", self.atualizar_poligono)

            if self.figura_nova is None:
                self.figura_nova = model.Poligono(event.x, event.y, self.cor_borda, self.cor_preenchimento)

            else:
                self.figura_nova.adicionar_ponto(event.x, event.y)

        else:
             self.canvas.unbind("<Motion>")
             self.figura_nova = self.fabricas[tipo](event.x, event.y)

        self.desenhar()


    def atualizar_figura(self, event):

        if self.figura_nova is None:
            return

        self.figura_nova.atualizar(event.x, event.y)
        self.desenhar()

    def atualizar_poligono(self, event):
        if isinstance(self.figura_nova, model.Poligono):
            self.figura_nova.atualizar(event.x, event.y)
            self.desenhar()

    def finalizar_figura(self, event):

        if self.figura_nova is None:
            return

        if isinstance(self.figura_nova, model.Poligono):
            return

        if not self.figura_nova.incompleta():
            self.figuras.append(self.figura_nova)

        self.figura_nova = None
        self.desenhar()

    def finalizar_poligono(self, event):
        if not isinstance(self.figura_nova, model.Poligono):
            return

        self.figura_nova.pontos.pop()

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

    def instrucao_poligono(self, *args):
        if self.tipo_figura_var.get() == "Poligono":
            if not self.mensagem_poligono_mostrada:

                messagebox.showinfo("Poligono", "Botão Esquerdo: Adicionar vértices.\n Botão Direito: Finalizar o polígono.")
                self.mensagem_poligono_mostrada = True

    def executar(self):
        self.criar_interface()
        self.root.mainloop()
        