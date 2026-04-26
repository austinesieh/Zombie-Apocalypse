import tkinter as ui_module
import random
WIDTH, HEIGHT = 1000,1000

def SETUP_WORLD(X_SIZE, Y_SIZE):
    # --// Create window, drawable area within window,
    # --// Then add canvas into window then display
    window = ui_module.Tk()
    canvas = ui_module.Canvas(window, width=X_SIZE, height=Y_SIZE, bg='black')
    canvas.pack()
    window.mainloop()


