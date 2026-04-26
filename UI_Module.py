import tkinter as ui_module
import random

def SETUP_WORLD(X_SIZE, Y_SIZE):
    # --// Create window, drawable area within window,
    # --// Then add canvas into window then display
    window = ui_module.Tk()
    canvas = ui_module.Canvas(window, width=X_SIZE, height=Y_SIZE, bg='black')
    canvas.pack()
    return canvas, window

def CREATE_LABEL(canvas, adornee, label_text, label_color):
    x1, y1, x2, y2 = canvas.coords(adornee.canvasID)
    x = (x1 + x2) / 2
    y = y1 - 20
    text_label = canvas.create_text(x, y, text= label_text, fill= label_color, font=("Arial", 15))
    return text_label

def CLEAR_LABELS(canvas, label_table):
    for label in label_table:
        canvas.delete(label)



