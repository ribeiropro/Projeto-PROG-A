from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
import tkinter as tk

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova

    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor_atual_borda, cor_atual_preenchimento)

    elif tipo_figura_var.get() == 'Rabisco':
        figura_nova = ("rabisco", [(event.x, event.y)], cor_atual_borda, cor_atual_preenchimento)

    elif tipo_figura_var.get() == 'Retângulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y), cor_atual_borda, cor_atual_preenchimento)

    elif tipo_figura_var.get() == 'Círculo':
        figura_nova = ("circulo", (event.x, event.y, event.x, event.y), cor_atual_borda, cor_atual_preenchimento)

    elif tipo_figura_var.get() == 'Oval':
        figura_nova = ("oval", (event.x, event.y, event.x, event.y), cor_atual_borda, cor_atual_preenchimento)

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova

    fig, values, corborda, corpreencher = figura_nova

    if fig == "rabisco":
        values.append((event.x, event.y))
        figura_nova = (fig, values, corborda, corpreencher)

    elif fig == "linha":
        figura_nova = ("linha", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), corborda, corpreencher)

    elif fig == "retangulo":
        figura_nova = ("retangulo", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), corborda, corpreencher)

    elif fig == "circulo":
        figura_nova = ("circulo", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), corborda, corpreencher)
    elif fig == "oval":
        figura_nova = ("oval", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), corborda, corpreencher)

    desenhar_figuras()
    desenhar_figura_nova()


# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova):
        figuras.append(figura_nova)

    desenhar_figuras()


def desenhar_figuras():
    canvas.delete("all")

    for fig, values, corborda, corpreencher in figuras:

        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill=corborda)

        elif fig == "rabisco":
            canvas.create_line(values, fill=corborda)

        elif fig == "retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline=corborda, fill=corpreencher)

        elif fig == "circulo":
            raio = ((values[0] - values[2])**2 + (values[1] - values[3])**2) ** 0.5
            canvas.create_oval(values[0]-raio, values[1]-raio, values[0]+raio, values[1]+raio, outline=corborda, fill=corpreencher)

        elif fig == "oval":
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=corborda, fill=corpreencher)

def desenhar_figura_nova():
    fig, values, corborda, corpreencher = figura_nova

    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2), fill=corborda)

    elif fig == "rabisco":
        canvas.create_line(values, dash=(4, 2), fill=corborda)

    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2), outline=corborda, fill=corpreencher)

    elif fig == "circulo":
        raio = ((values[0] - values[2])**2 + (values[1] - values[3])**2) ** 0.5
        canvas.create_oval(values[0]-raio, values[1]-raio, values[0]+raio, values[1]+raio, dash=(4, 2), outline=corborda, fill=corpreencher)

    elif fig == "oval":
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2), outline=corborda, fill=corpreencher)

def incompleta(figura):
    fig, values, corborda, corpreencher = figura

    if fig == "linha":
        return (values[0], values[1]) == (values[2], values[3])

    elif fig == "rabisco":
        return len(values) <= 1

    elif fig == "retangulo":
        return (values[0], values[1]) == (values[2], values[3])

    elif fig == "circulo":
        return (values[0], values[1]) == (values[2], values[3])

    elif fig == "oval":
        return (values[0], values[1]) == (values[2], values[3])

#******* MAIN *******#

figuras = []
figura_nova = None


root = Tk()

frame = Frame(root)


paddings = {'padx': 5, 'pady': 5}


# label
label = ttk.Label(frame, text='Escolha uma figura:')
label.grid(column=0, row=0, sticky=W, **paddings)


# option menu
tipo_figura_var = StringVar(root)

option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Linha',
                             'Linha',
                             'Rabisco',
                             'Retângulo',
                             'Círculo',
                             'Oval')

option_menu.grid(column=1, row=0, sticky=W, **paddings)


# escolher cor da borda
cor_atual_borda = 'black'

def escolher_cor_borda():
    global cor_atual_borda

    color = colorchooser.askcolor()

    print(color)

    if color[1] is not None:
        cor_atual_borda = color[1]
        btn_cor.config(bg=cor_atual_borda)

# escolher cor do preenchimento
cor_atual_preenchimento = None

def escolher_cor_preenchimento():
    global cor_atual_preenchimento

    color_b = colorchooser.askcolor()

    print(color_b)

    if color_b[1] is not None:
        cor_atual_preenchimento = color_b[1]
        btn_preenchimento.config(bg=cor_atual_preenchimento)


btn_cor = tk.Button(frame, text='Cor da Borda', command=escolher_cor_borda, bg=cor_atual_borda, fg='white')
btn_cor.grid(column=0, row=1, sticky=W, **paddings)

btn_preenchimento = tk.Button(frame, text= 'Cor de Preenchimento', command=escolher_cor_preenchimento, bg=cor_atual_preenchimento, fg='black')
btn_preenchimento.grid(column=1, row=1, sticky=W, **paddings)


# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=2, columnspan=2, sticky=W, **paddings)


frame.pack()


# Eventos do mouse
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)


root.mainloop()