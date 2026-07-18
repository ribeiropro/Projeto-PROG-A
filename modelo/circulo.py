from modelo.figura import Figura

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
