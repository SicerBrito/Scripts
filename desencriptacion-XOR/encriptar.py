import random

def generar_clave(longitud=4):
    return [random.randint(0, 255) for _ in range(longitud)]

def encriptar(mensaje, clave):
    return [ord(c) ^ clave[i % len(clave)] for i, c in enumerate(mensaje)]

def main():
    mensaje_deseado = "Felicidades, has logrado descifrar el mensaje. Ahora, vaya pa la cama mijo, descanse que mucha programación es mala para la salud. (Pero no para el bolsillo)"
    clave = generar_clave()
    mensaje_cifrado = encriptar(mensaje_deseado, clave)
    
    print("Mensaje original:", mensaje_deseado)
    print("Clave generada:", clave)
    print("Mensaje cifrado:", mensaje_cifrado)
    
    # Guardar el mensaje cifrado en un archivo
    with open("mensaje_cifrado.txt", "w") as f:
        f.write(",".join(map(str, mensaje_cifrado)))
    
    print("Mensaje cifrado guardado en 'mensaje_cifrado.txt'")

if __name__ == "__main__":
    main()