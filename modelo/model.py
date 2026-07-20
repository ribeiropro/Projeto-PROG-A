from modelo.figura import Figura
import json

class ModeloDesenho:
    def __init__(self):
        self.figuras = []
        self.figura_nova = None
        self.cor_borda = "black"
        self.cor_preenchimento = None

    def salvar_para_arquivo(self, caminho_arquivo):
        dados_salvaveis = []

        for fig in self.figuras:
            dados_salvaveis.append({"classe": fig.__class__.__name__, "atributos": fig.__dict__})

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_salvaveis, f, indent=4)