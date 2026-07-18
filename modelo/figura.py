from abc import ABC, abstractmethod

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
