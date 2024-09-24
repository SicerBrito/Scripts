import os

def generar_clave(longitud=16):
    """Genera una clave aleatoria segura usando os.urandom()."""
    return os.urandom(longitud)

def cifrar_descifrar(mensaje, clave):
    """Cifra o descifra el mensaje usando XOR."""
    return bytes(b ^ clave[i % len(clave)] for i, b in enumerate(mensaje))

def main():
    mensaje_original = "Este es un mensaje secreto."
    mensaje_bytes = mensaje_original.encode('utf-8')
    
    # Generar clave
    clave = generar_clave()
    
    # Cifrado
    mensaje_cifrado = cifrar_descifrar(mensaje_bytes, clave)
    
    print(f"Mensaje original: {mensaje_original}")
    print(f"Clave (hex): {clave.hex()}")
    print(f"Mensaje cifrado (hex): {mensaje_cifrado.hex()}")
    
    # Descifrado
    mensaje_descifrado = cifrar_descifrar(mensaje_cifrado, clave)
    mensaje_descifrado_texto = mensaje_descifrado.decode('utf-8')
    
    print(f"\nMensaje descifrado: {mensaje_descifrado_texto}")
    
    # Demostración de cómo un usuario podría descifrar el mensaje
    print("\nSimulación de descifrado por el usuario:")
    print("El usuario recibe el mensaje cifrado y la clave:")
    mensaje_cifrado_recibido = mensaje_cifrado  # Simulando que el usuario recibe esto
    clave_recibida = clave  # Simulando que el usuario recibe esto
    
    mensaje_descifrado_usuario = cifrar_descifrar(mensaje_cifrado_recibido, clave_recibida)
    mensaje_descifrado_usuario_texto = mensaje_descifrado_usuario.decode('utf-8')
    
    print(f"Mensaje descifrado por el usuario: {mensaje_descifrado_usuario_texto}")

if __name__ == "__main__":
    main()