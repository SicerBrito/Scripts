import tkinter as tk
import random

class VentanaError(tk.Tk):
    def __init__(self, num_mensajes=50):
        super().__init__()
        self.overrideredirect(True)  # Ocultar la barra de título y la ventana
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))  # Tamaño de pantalla completa
        self.configure(bg='red')  # Cambiar el fondo a rojo (opcional)
        self.attributes('-topmost', True)  # Mantener la ventana en la parte superior

        for _ in range(num_mensajes):
            self.mostrar_mensaje_error()

    def mostrar_mensaje_error(self):
        mensaje = "Este es un mensaje de error falso"
        error_frame = tk.Frame(self, bg='white', width=400, height=100)
        error_frame.place(relx=random.uniform(0.1, 0.9), rely=random.uniform(0.1, 0.9), anchor='center')
        error_label = tk.Label(error_frame, text=mensaje, fg='red', font=("Arial", 14))
        error_label.pack(pady=10)

if __name__ == "__main__":
    ventana_error = VentanaError()
    ventana_error.mainloop()
