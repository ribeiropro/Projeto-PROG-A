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

    def carregar_de_arquivo(self, caminho_arquivo, dicionario_classes):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados_carregados = json.load(f)

        self.figuras.clear()

        for item in dados_carregados:
            nome_classe = item["classe"]
            atributos = item["atributos"]

            if nome_classe in dicionario_classes:
                classe_alvo = dicionario_classes[nome_classe]
                nova_figura = classe_alvo.__new__(classe_alvo)

                if "pontos" in atributos:
                    atributos["pontos"] = [tuple(p) for p in atributos["pontos"]]

                nova_figura.__dict__.update(atributos)
                self.figuras.append(nova_figura)