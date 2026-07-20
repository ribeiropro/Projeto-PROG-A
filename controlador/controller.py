from tkinter import colorchooser, messagebox
from tkinter import filedialog
from modelo.model import ModeloDesenho
from modelo.linha import Linha
from modelo.rabisco import Rabisco
from modelo.retangulo import Retangulo
from modelo.circulo import Circulo
from modelo.oval import Oval
from modelo.poligono import Poligono
from visao.view import EditorView
from controlador.estados import EstadoFormaComum, EstadoPoligono

class EditorController:
    def __init__(self, root):
        self.root = root
        self.modelo = ModeloDesenho()
        self.view = EditorView(self.root, self)

        self.fabricas = {
            "Linha": lambda x, y: Linha(x, y, self.modelo.cor_borda),
            "Rabisco": lambda x, y: Rabisco(x, y, self.modelo.cor_borda),
            "Retângulo": lambda x, y: Retangulo(x, y, self.modelo.cor_borda, self.modelo.cor_preenchimento),
            "Círculo": lambda x, y: Circulo(x, y, self.modelo.cor_borda, self.modelo.cor_preenchimento),
            "Oval": lambda x, y: Oval(x, y, self.modelo.cor_borda, self.modelo.cor_preenchimento),
            "Poligono": lambda x, y: Poligono(x, y, self.modelo.cor_borda, self.modelo.cor_preenchimento)
        }
        estado_forma = EstadoFormaComum()

        self.estados = {
    "Linha": estado_forma,
    "Rabisco": estado_forma,
    "Retângulo": estado_forma,
    "Círculo": estado_forma,
    "Oval": estado_forma,
    "Poligono": EstadoPoligono()
}

        self.estado_atual = self.estados["Linha"]
        
    def atualizar_estado(self, *args):
        tipo = self.view.tipo_figura_var.get()
        self.estado_atual = self.estados[tipo]

    def inicializar(self):
        self.view.criar_interface(self.modelo.cor_borda)

    def renderizar_tela(self):
        self.view.desenhar(self.modelo)

    def iniciar_figura(self, event):
        self.estado_atual.mouse_pressionado(self, event)

    def atualizar_figura(self, event):
        self.estado_atual.mouse_arrastado(self, event)

    def finalizar_figura(self, event):
        self.estado_atual.mouse_solto(self, event)

    def finalizar_poligono(self, event):
        self.estado_atual.clique_direito(self, event)

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
            if not self.view.mensagem_poligono_mostrada:
                messagebox.showinfo(
                    "Poligono", 
                    "Botão Esquerdo: Adicionar vértices.\nBotão Direito: Finalizar o polígono."
                )
                self.view.mensagem_poligono_mostrada = True

    def salvar_projeto(self):

        caminho = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("Arquivos JSON", "*.json")])
        if caminho:
            self.modelo.salvar_para_arquivo(caminho)

    def carregar_projeto(self):

        caminho = filedialog.askopenfilename(filetypes=[("Arquivos JSON", "*.json")])
        if caminho:
            dicionario_classes = {
                "Linha": Linha,
                "Rabisco": Rabisco,
                "Retangulo": Retangulo,
                "Circulo": Circulo,
                "Oval": Oval,
                "Poligono": Poligono,
            }

            self.modelo.carregar_de_arquivo(caminho, dicionario_classes)
            self.renderizar_tela()