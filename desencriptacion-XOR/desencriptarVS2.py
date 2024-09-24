
# python script.py mensaje_cifrado.txt -l 6 -r
import re
import itertools
import time
import multiprocessing
import numpy as np
import pickle
import os
import argparse
import logging
from collections import Counter

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def xor_desencriptar_numpy(mensaje, llave):
    llave_extendida = np.tile(llave, len(mensaje) // len(llave) + 1)[:len(mensaje)]
    return np.frombuffer(mensaje, dtype=np.uint8) ^ llave_extendida

def verificar_legibilidad(texto, umbral_palabras=0.5):
    # Verificación básica de caracteres
    if not re.match(r'^[a-zA-Z0-9\s.,@\-_\/()]+$', texto):
        return False
    
    # Análisis de frecuencia de letras en español
    frecuencia_esp = {'e': 12.53, 'a': 11.53, 'o': 8.68, 'l': 8.68, 's': 7.20, 'n': 6.95, 'd': 5.86, 'r': 6.87, 'u': 3.93, 'i': 6.25, 't': 4.63, 'c': 4.14, 'p': 2.51, 'm': 3.16, 'y': 1.09, 'q': 0.88, 'b': 1.49, 'h': 1.18, 'g': 1.01, 'f': 0.69, 'v': 1.05, 'j': 0.44, 'ñ': 0.31, 'z': 0.45, 'x': 0.14, 'k': 0.01, 'w': 0.02}
    texto_limpio = ''.join(filter(str.isalpha, texto.lower()))
    contador = Counter(texto_limpio)
    total = sum(contador.values())
    
    if total == 0:
        return False
    
    score = sum(abs(frecuencia_esp.get(char, 0) - (count / total * 100)) for char, count in contador.items())
    return score < 50  # Un umbral arbitrario, ajusta según sea necesario

def probar_claves(args):
    mensaje_cifrado, rango_inicio, rango_fin, longitud_clave = args
    for llave_potencial in itertools.product(range(256), repeat=longitud_clave):
        if rango_inicio <= llave_potencial[0] < rango_fin:
            mensaje_desencriptado = xor_desencriptar_numpy(mensaje_cifrado, np.array(llave_potencial, dtype=np.uint8))
            try:
                texto_desencriptado = mensaje_desencriptado.tobytes().decode('utf-8')
                if verificar_legibilidad(texto_desencriptado):
                    return llave_potencial, texto_desencriptado
            except UnicodeDecodeError:
                continue
    return None

def guardar_progreso(progreso, archivo="progreso.pkl"):
    try:
        with open(archivo, "wb") as f:
            pickle.dump(progreso, f)
    except IOError as e:
        logging.error(f"Error al guardar el progreso: {e}")

def cargar_progreso(archivo="progreso.pkl"):
    if os.path.exists(archivo):
        try:
            with open(archivo, "rb") as f:
                return pickle.load(f)
        except (IOError, pickle.UnpicklingError) as e:
            logging.error(f"Error al cargar el progreso: {e}")
    return 0

def desencriptar_fuerza_bruta_paralelo(mensaje_cifrado, longitud_clave=4, inicio=0):
    num_procesos = multiprocessing.cpu_count()
    total_combinaciones = 256 ** longitud_clave
    chunk_size = max(1, (total_combinaciones - inicio) // (num_procesos * 100))
    
    with multiprocessing.Pool(processes=num_procesos) as pool:
        for i, resultado in enumerate(pool.imap_unordered(probar_claves, 
            [(mensaje_cifrado, inicio + i*chunk_size, min(inicio + (i+1)*chunk_size, total_combinaciones), longitud_clave) 
             for i in range(0, total_combinaciones - inicio, chunk_size)]), start=1):
            if resultado:
                pool.terminate()
                return resultado
            
            progreso_actual = inicio + i * chunk_size
            if i % 10 == 0:
                porcentaje = progreso_actual / total_combinaciones * 100
                logging.info(f"Progreso: {porcentaje:.2f}% completado")
                guardar_progreso(progreso_actual)

    logging.info("Búsqueda completa. No se encontró una clave válida.")
    return None

def main():
    parser = argparse.ArgumentParser(description="Desencriptador XOR por fuerza bruta")
    parser.add_argument("archivo", help="Archivo con el mensaje cifrado")
    parser.add_argument("-l", "--longitud", type=int, default=4, help="Longitud de la clave (default: 4)")
    parser.add_argument("-r", "--reanudar", action="store_true", help="Reanudar desde el último progreso guardado")
    args = parser.parse_args()

    try:
        with open(args.archivo, "r") as f:
            mensaje_cifrado = np.array(list(map(int, f.read().split(","))), dtype=np.uint8).tobytes()
    except IOError as e:
        logging.error(f"Error al leer el archivo: {e}")
        return

    inicio = cargar_progreso() if args.reanudar else 0
    logging.info(f"Iniciando desencriptación por fuerza bruta desde {inicio / (256**args.longitud) * 100:.2f}%...")
    
    resultado = desencriptar_fuerza_bruta_paralelo(mensaje_cifrado, longitud_clave=args.longitud, inicio=inicio)
    
    if resultado:
        llave, mensaje = resultado
        logging.info(f"Clave encontrada: {llave}")
        logging.info(f"Mensaje descifrado: {mensaje}")
    else:
        logging.info("No se encontró la clave.")

if __name__ == "__main__":
    main()