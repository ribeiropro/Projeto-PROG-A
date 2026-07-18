from modelo.figura import Figura

class ModeloDesenho:
    def __init__(self):
        self.figuras = []
        self.figura_nova = None
        self.cor_borda = "black"
        self.cor_preenchimento = None