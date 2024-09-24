import os

def generar_clave(longitud=16):
    """Genera una clave aleatoria segura usando os.urandom()."""
    return os.urandom(longitud)

def cifrar_descifrar(mensaje, clave):
    """Cifra o descifra el mensaje usando XOR. La misma función sirve para ambos propósitos."""
    return bytes(b ^ clave[i % len(clave)] for i, b in enumerate(mensaje))

def guardar_datos(nombre_archivo, datos):
    """Guarda los datos en un archivo binario."""
    with open(nombre_archivo, "wb") as f:
        f.write(datos)

def cargar_datos(nombre_archivo):
    """Carga los datos desde un archivo binario."""
    with open(nombre_archivo, "rb") as f:
        return f.read()

def main():
    mensaje_original = "Felicidades, has logrado descifrar el mensaje. Ahora, vaya pa la cama mijo, descanse que mucha programación es mala para la salud. (Pero no para el bolsillo)"
    mensaje_bytes = mensaje_original.encode('utf-8')
    
    # Cifrado
    clave = generar_clave()
    mensaje_cifrado = cifrar_descifrar(mensaje_bytes, clave)
    
    print(f"Mensaje original: {mensaje_original}")
    print(f"Clave generada (en hexadecimal): {clave.hex()}")
    print(f"Mensaje cifrado (en hexadecimal): {mensaje_cifrado.hex()}")
    
    # Guardar el mensaje cifrado y la clave
    guardar_datos("mensaje_cifrado.bin", mensaje_cifrado)
    guardar_datos("clave.bin", clave)
    print("Mensaje cifrado guardado en 'mensaje_cifrado.bin'")
    print("Clave guardada en 'clave.bin'")
    
    # Demostración de descifrado
    clave_cargada = cargar_datos("clave.bin")
    mensaje_cifrado_cargado = cargar_datos("mensaje_cifrado.bin")
    mensaje_descifrado = cifrar_descifrar(mensaje_cifrado_cargado, clave_cargada)
    print(f"Mensaje descifrado: {mensaje_descifrado.decode('utf-8')}")

if __name__ == "__main__":
    main()