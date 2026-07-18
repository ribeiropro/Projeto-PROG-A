from modelo.figura import Figura

class Rabisco(Figura):
    def __init__(self, x, y, cor_borda):
        super().__init__(x, y, cor_borda)
        self.pontos = [(x, y)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))

    def desenhar(self, canvas):
        if len(self.pontos) > 1:
            canvas.create_line(self.pontos, fill=self.cor_borda)

    def desenhar_preview(self, canvas):
        if len(self.pontos) > 1:
            canvas.create_line(self.pontos, fill=self.cor_borda, dash=(4, 2))

    def incompleta(self):
        return len(self.pontos) <= 1