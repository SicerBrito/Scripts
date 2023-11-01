import tkinter as tk
import random
import threading
import time
from tkinter import messagebox

class VentanaError(tk.Tk):
    def __init__(self, cantidad_mensajes=15):
        super().__init__()

        # Configuración de la ventana de error
        self.attributes('-alpha', 0.8)  # Configurar transparencia de la ventana
        self.overrideredirect(True)     # Ocultar la barra de título y la ventana
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))  # Tamaño de pantalla completa

        self.cantidad_mensajes = cantidad_mensajes
        self.crear_mensajes()

    def crear_mensajes(self):
        # Método para crear mensajes de error falsos
        for _ in range(self.cantidad_mensajes):
            random_text = "Este es un mensaje de error falso"
            self.mostrar_alerta(random_text)
            time.sleep(0.1)  # Intervalo de tiempo antes de crear el siguiente mensaje (en segundos)

    def mostrar_alerta(self, message):
        # Método para mostrar una alerta de error falso
        messagebox.showerror("Error Falso", message)

    def mostrar_broma(self):
        # Método para mostrar una alerta de broma
        messagebox.showinfo("¡Es una Broma!", "¡Es solo una broma!\nHaz clic para cerrar.")  # Mensaje informativo
        self.destroy()  # Cerrar la ventana al hacer clic en la alerta de broma

if __name__ == "__main__":
    ventana_error = VentanaError()  # Crear la ventana de error
    ventana_error.mostrar_broma()    # Mostrar la alerta de broma
    ventana_error.mainloop()         # Iniciar el bucle principal de tkinter
