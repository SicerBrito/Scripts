import tkinter as tk
import random
import threading
import time

class MensajeError:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root, bg='white', width=400, height=100)
        self.frame.place(relx=random.uniform(0.1, 0.9), rely=random.uniform(0.1, 0.9), anchor='center')
        self.label = tk.Label(self.frame, text="Este es un mensaje de error falso", fg='red', font=("Arial", 14))
        self.label.pack(pady=10)

        # Botón "X" para cerrar el mensaje
        self.boton_cerrar = tk.Button(self.frame, text="X", command=self.cerrar)
        self.boton_cerrar.place(relx=1.0, rely=0.0, anchor='ne')

    def cerrar(self):
        self.frame.destroy()

class VentanaError(tk.Tk):
    def __init__(self, num_mensajes=50):
        tk.Tk.__init__(self)

        # Configuración de transparencia (0 = completamente transparente, 1 = completamente opaco)
        self.attributes('-alpha', 0.8)  # Ajusta el valor a tu preferencia

        self.overrideredirect(True)  # Ocultar la barra de título y la ventana
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))  # Tamaño de pantalla completa
        self.mensajes = []

        self.hilo_creacion_mensajes = threading.Thread(target=self.crear_mensajes, args=(num_mensajes,))
        self.hilo_creacion_mensajes.start()

    def crear_mensajes(self, num_mensajes):
        for _ in range(num_mensajes):
            mensaje = MensajeError(self)
            self.mensajes.append(mensaje)
            time.sleep(3)  # Intervalo de tiempo antes de crear el siguiente mensaje (en segundos)

if __name__ == "__main__":
    ventana_error = VentanaError()
    ventana_error.mainloop()
