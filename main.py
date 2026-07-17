from tkinter import Tk
from controller import EditorController

if __name__ == "__main__":
    root = Tk()
    root.title("Editor de Desenhos")
    controlador = EditorController(root)
    controlador.inicializar()
    root.mainloop()