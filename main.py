import sys
import os

pasta_atual = os.path.dirname(__file__)
sys.path.append(os.path.join(pasta_atual, "controlador"))
sys.path.append(os.path.join(pasta_atual, "visao"))
sys.path.append(os.path.join(pasta_atual, "modelo"))

from tkinter import Tk
from controller import EditorController

if __name__ == "__main__":
    root = Tk()
    root.title("Editor de Desenhos")
    controlador = EditorController(root)
    controlador.inicializar()
    root.mainloop()