import tkinter as tk
from tkinter import messagebox

def mostrar_ventana_error():
    ventana = tk.Tk()
    ventana.overrideredirect(True)  # Ocultar la barra de título y la ventana
    ventana.geometry("1x1+0+0")  # Colocar la ventana fuera de la pantalla
    ventana.attributes('-topmost', True)  # Mantener la ventana en la parte superior

    for _ in range(50):
        ventana.attributes("-disabled", True)  # Desactivar la ventana
        messagebox.showerror("Error Falso", "Este es un mensaje de error falso.")
        ventana.update_idletasks()
        ventana.attributes("-disabled", False)  # Habilitar la ventana

    ventana.destroy()

mostrar_ventana_error()
