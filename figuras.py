import tkinter as tk 
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