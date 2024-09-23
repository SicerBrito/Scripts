# Mensaje cifrado
mensaje_cifrado = [44, 1, 29, 28, 9, 13, 21, 20, 14, 1, 2, 85, 32, 17, 16, 27, 74, 32, 24, 16, 13, 11, 81, 36, 31, 13, 31, 1, 15, 22, 30, 89, 74, 12, 16, 6, 74, 8, 30, 18, 24, 5, 21, 26, 74, 0, 20, 6, 9, 13, 23, 7, 11, 22, 81, 16, 6, 68, 28, 16, 4, 23, 16, 31, 15, 74, 81, 85, 43, 12, 30, 7, 11, 72, 81, 5, 11, 22, 16, 85, 27, 17, 20, 85, 35, 10, 2, 28, 28, 1, 81, 7, 15, 7, 30, 27, 5, 30, 18, 20, 74, 16, 4, 85, 6, 11, 22, 7, 5, 72, 81, 6, 31, 6, 20, 85, 15, 8, 81, 22, 5, 0, 20, 85, 9, 11, 31, 85, 15, 8, 81, 4, 31, 1, 81, 7, 15, 23, 30, 25, 28, 13, 2, 1, 15, 68, 20, 6, 30, 1, 81, 16, 0, 1, 3, 22, 3, 7, 24, 26, 74, 1, 31, 85, 45, 13, 5, 61, 31, 6, 94, 50, 3, 16, 61, 20, 8, 68, 8, 85, 9, 11, 28, 5, 11, 22, 5, 16, 74, 1, 29, 85, 15, 10, 29, 20, 9, 1, 81, 20, 74, 23, 30, 5, 5, 22, 5, 16, 42, 13, 31, 6, 3, 18, 20, 91, 9, 8, 95]

# Importar regex para poder trabajar con expresiones regulares y ver su legibilidad 
import re
regex_legible = re.compile(r'^[a-zA-Z0-9\s.,@\-_\/]+$')

def xor_desencriptar(mensaje, llave):
    mensaje_desencriptado = []
    for i in range(len(mensaje)):
        mensaje_desencriptado.append(mensaje[i] ^ llave[i % len(llave)]) #operación XOR
    return mensaje_desencriptado

def verificar_legibilidad(mensaje):
    """
    Verifica si un mensaje es legible según ciertos criterios definidos por una expresión regular.
    
    Args:
        mensaje (list): La lista de números que representan el mensaje desencriptado.
    
    Returns:
        bool: True si el mensaje es legible, False de lo contrario.
    """
    texto = ''.join(chr(caracter) for caracter in mensaje)
# Permite verificar si es legible
    return regex_legible.match(texto) is not None

def desencriptar_code(mensaje_cifrado):
    """
    Realiza un ataque de fuerza bruta para descifrar un mensaje cifrado utilizando todas las posibles combinaciones de llaves.
    
    Args:
        mensaje_cifrado (list): La lista de números que representan el mensaje cifrado.
    """
    # Bucles para buscar la llave
    for a in range(97, 123):  # Rango de 'a' a 'z' en ASCII
        for b in range(97, 123):
            for c in range(97, 123):
                for d in range(97, 123):
                    llave_potencial = [a, b, c, d]
                    mensaje_desencriptado = xor_desencriptar(mensaje_cifrado, llave_potencial)
                    if verificar_legibilidad(mensaje_desencriptado):
                        texto_desencriptado = ''.join(chr(caracter) for caracter in mensaje_desencriptado)
                        print("Clave:", ''.join(chr(caracter) for caracter in llave_potencial))
                        print("Mensaje descifrado:", texto_desencriptado)
                        return

# Ejecutr
desencriptar_code(mensaje_cifrado)
