import re
import itertools
import time
import multiprocessing
import numpy as np
import pickle
import os

def xor_desencriptar_numpy(mensaje, llave):
    llave_extendida = np.tile(llave, len(mensaje) // len(llave) + 1)[:len(mensaje)]
    return np.frombuffer(mensaje, dtype=np.uint8) ^ llave_extendida

def verificar_legibilidad(texto):
    return re.match(r'^[a-zA-Z0-9\s.,@\-_\/()]+$', texto) is not None

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

def guardar_progreso(progreso):
    with open("progreso.pkl", "wb") as f:
        pickle.dump(progreso, f)

def cargar_progreso():
    if os.path.exists("progreso.pkl"):
        with open("progreso.pkl", "rb") as f:
            return pickle.load(f)
    return 0

def desencriptar_fuerza_bruta_paralelo(mensaje_cifrado, longitud_clave=4, inicio=0):
    num_procesos = multiprocessing.cpu_count()
    total_combinaciones = 256 ** longitud_clave
    chunk_size = (total_combinaciones - inicio) // (num_procesos * 100)  # Ajustado para más actualizaciones frecuentes
    
    with multiprocessing.Pool(processes=num_procesos) as pool:
        for i, resultado in enumerate(pool.imap_unordered(probar_claves, 
            [(mensaje_cifrado, inicio + i*chunk_size, inicio + (i+1)*chunk_size, longitud_clave) 
             for i in range(num_procesos * 100)]), start=1):
            if resultado:
                pool.terminate()
                return resultado
            
            progreso_actual = inicio + i * chunk_size
            if i % 10 == 0:  # Actualizar progreso cada 10 chunks
                print(f"\rProgreso: {progreso_actual / total_combinaciones * 100:.2f}% completado", end="", flush=True)
                guardar_progreso(progreso_actual)

    print("\nBúsqueda completa. No se encontró una clave válida.")
    return None

def main():
    with open("mensaje_cifrado.txt", "r") as f:
        mensaje_cifrado = np.array(list(map(int, f.read().split(","))), dtype=np.uint8).tobytes()

    inicio = cargar_progreso()
    print(f"Iniciando desencriptación por fuerza bruta desde {inicio / (256**4) * 100:.2f}%...")
    
    resultado = desencriptar_fuerza_bruta_paralelo(mensaje_cifrado, inicio=inicio)
    
    if resultado:
        llave, mensaje = resultado
        print("\nClave encontrada:", llave)
        print("Mensaje descifrado:", mensaje)
    else:
        print("\nNo se encontró la clave.")

if __name__ == "__main__":
    main()