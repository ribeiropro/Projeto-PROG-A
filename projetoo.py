from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
import tkinter as tk

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova

    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor_atual)

    elif tipo_figura_var.get() == 'Rabisco':
        figura_nova = ("rabisco", [(event.x, event.y)], cor_atual)

    elif tipo_figura_var.get() == 'Retângulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y), cor_atual)


# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova

    fig, values, cor = figura_nova

    if fig == "rabisco":
        values.append((event.x, event.y))
        figura_nova = (fig, values, cor)

    elif fig == "linha":
        figura_nova = ("linha", 
                       (figura_nova[1][0], figura_nova[1][1], event.x, event.y), 
                       cor)

    elif fig == "retangulo":
        figura_nova = ("retangulo", 
                       (figura_nova[1][0], figura_nova[1][1], event.x, event.y), 
                       cor)

    desenhar_figuras()
    desenhar_figura_nova()


# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova):
        figuras.append(figura_nova)

    desenhar_figuras()


def desenhar_figuras():
    canvas.delete("all")

    for fig, values, cor in figuras:

        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill=cor)

        elif fig == "rabisco":
            canvas.create_line(values, fill=cor)

        elif fig == "retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3],
                                    outline=cor)


def desenhar_figura_nova():
    fig, values, cor = figura_nova

    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3],
                           dash=(4, 2), fill=cor)

    elif fig == "rabisco":
        canvas.create_line(values, dash=(4, 2), fill=cor)

    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3],
                                dash=(4, 2), outline=cor)


def incompleta(figura):
    fig, values, cor = figura

    if fig == "linha":
        return (values[0], values[1]) == (values[2], values[3])

    elif fig == "rabisco":
        return len(values) <= 1

    elif fig == "retangulo":
        return (values[0], values[1]) == (values[2], values[3])


#******* MAIN *******#

figuras = []
figura_nova = None


root = Tk()

frame = Frame(root)


paddings = {'padx': 5, 'pady': 5}


# label
label = ttk.Label(frame, text='Linha, Rabisco ou Retângulo:')
label.grid(column=0, row=0, sticky=W, **paddings)


# option menu
tipo_figura_var = StringVar(root)

option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Linha',
                             'Linha',
                             'Rabisco',
                             'Retângulo')

option_menu.grid(column=1, row=0, sticky=W, **paddings)


# escolher cores
cor_atual = 'black'


def escolher_cor():
    global cor_atual

    color = colorchooser.askcolor()

    print(color)

    if color[1] is not None:
        cor_atual = color[1]
        btn_cor.config(bg=cor_atual)


btn_cor = tk.Button(root,
                    text='Escolher Cor',
                    command=escolher_cor,
                    bg=cor_atual,
                    fg='white')

btn_cor.pack()


# Área de desenho
canvas = Canvas(frame,
                bg='white',
                width=600,
                height=600)

canvas.grid(column=0,
            row=1,
            columnspan=2,
            sticky=W,
            **paddings)


frame.pack()


# Eventos do mouse
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)


root.mainloop()