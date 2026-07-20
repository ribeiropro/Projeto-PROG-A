from abc import ABC, abstractmethod
from modelo.linha import Linha
from modelo.rabisco import Rabisco
from modelo.retangulo import Retangulo
from modelo.circulo import Circulo
from modelo.oval import Oval
from modelo.poligono import Poligono

# Interface base para os Estados
class EstadoFerramenta(ABC):
    @abstractmethod
    def mouse_pressionado(self, controlador, event):
        pass

    @abstractmethod
    def mouse_arrastado(self, controlador, event):
        pass

    @abstractmethod
    def mouse_solto(self, controlador, event):
        pass

    @abstractmethod
    def clique_direito(self, controlador, event):
        pass

# Estado para Linha, Rabisco, Retângulo, Círculo e Oval
class EstadoFormaComum(EstadoFerramenta):
    def mouse_pressionado(self, controlador, event):
        controlador.view.canvas.unbind("<Motion>")
        tipo = controlador.view.tipo_figura_var.get()
        controlador.modelo.figura_nova = controlador.fabricas[tipo](event.x, event.y)
        controlador.renderizar_tela()

    def mouse_arrastado(self, controlador, event):
        if controlador.modelo.figura_nova:
            controlador.modelo.figura_nova.atualizar(event.x, event.y)
            controlador.renderizar_tela()

    def mouse_solto(self, controlador, event):
        if controlador.modelo.figura_nova:
            if not controlador.modelo.figura_nova.incompleta():
                controlador.modelo.figuras.append(controlador.modelo.figura_nova)
            controlador.modelo.figura_nova = None
            controlador.renderizar_tela()

    def clique_direito(self, controlador, event):
        pass  # Formas comuns não reagem ao botão direito

# Estado específico para o Polígono
class EstadoPoligono(EstadoFerramenta):
    def mouse_pressionado(self, controlador, event):
        # Passa a escutar o movimento do mouse para o preview dinâmico
        controlador.view.canvas.bind("<Motion>", controlador.atualizar_figura)
        
        if controlador.modelo.figura_nova is None:
            controlador.modelo.figura_nova = Poligono(
                event.x, event.y, controlador.modelo.cor_borda, controlador.modelo.cor_preenchimento
            )
        else:
            controlador.modelo.figura_nova.adicionar_ponto(event.x, event.y)
        controlador.renderizar_tela()

    def mouse_arrastado(self, controlador, event):
        # O polígono precisa atualizar o ponto flutuante enquanto arrasta ou move
        if controlador.modelo.figura_nova:
            controlador.modelo.figura_nova.atualizar(event.x, event.y)
            controlador.renderizar_tela()

    def mouse_solto(self, controlador, event):
        pass  # O Polígono só termina com o botão direito

    def clique_direito(self, controlador, event):
        if isinstance(controlador.modelo.figura_nova, Poligono):
            controlador.view.canvas.unbind("<Motion>")
            controlador.modelo.figura_nova.pontos.pop()  # Remove o ponto flutuante extra
            
            if not controlador.modelo.figura_nova.incompleta():
                controlador.modelo.figuras.append(controlador.modelo.figura_nova)
            
            controlador.modelo.figura_nova = None
            controlador.renderizar_tela()