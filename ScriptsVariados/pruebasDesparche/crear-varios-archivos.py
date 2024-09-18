import os
import time
import random
import string

def mostrar_mensaje():
    print("Este es un VIRUS SIMULADO con fines educativos. No causa daño real.")

def simular_propagacion():
    print("Simulando propagación del virus...")
    for i in range(10):
        # Generar un nombre aleatorio para el archivo
        letras = string.ascii_letters
        nombre_archivo = ''.join(random.choice(letras) for i in range(10))

        # Crear un archivo con el nombre aleatorio
        open(nombre_archivo + '.txt', 'a').close()

        # Esperar un tiempo aleatorio entre 0.1 y 0.5 segundos antes de crear el siguiente archivo
        time.sleep(random.uniform(0.1, 0.5))

if __name__ == "__main__":
    mostrar_mensaje()
    simular_propagacion()
