from modelo.figura import Figura

class Poligono(Figura):
    def __init__(self, x, y, cor_borda, cor_preenchimento):
        super().__init__(x, y, cor_borda, cor_preenchimento)
        self.pontos = [(x, y)]

    def atualizar(self, x, y):
        if len(self.pontos) == 1:
            self.pontos.append((x, y))
        else:
            self.pontos[-1] = (x, y)

    def adicionar_ponto(self, x, y):
        self.pontos.append((x, y))

    def desenhar(self, canvas):
        canvas.create_polygon(self.pontos, outline=self.cor_borda, fill=self.cor_preenchimento if self.cor_preenchimento else "")

    def desenhar_preview(self, canvas):
        canvas.create_polygon(self.pontos, outline=self.cor_borda, fill=self.cor_preenchimento if self.cor_preenchimento else "", dash=(4, 2))

    def incompleta(self):
        return len(self.pontos) < 3