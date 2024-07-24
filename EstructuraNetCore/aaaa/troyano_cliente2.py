import socket
import ssl

def crear_cliente(direccion, puerto):
    contexto = ssl.create_default_context()
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_conexion = contexto.wrap_socket(cliente, server_hostname=direccion)
    cliente_conexion.connect((direccion, puerto))
    return cliente_conexion

def interactuar_servidor(cliente):
    while True:
        comando = input('Ingresa un comando (o "salir" para terminar): ')
        cliente.sendall(comando.encode('utf-8'))

        if comando.lower() == 'salir':
            break
        elif comando.lower().startswith("subir "):
            _, nombre_archivo = comando.split()
            try:
                with open(nombre_archivo, 'rb') as f:
                    contenido = f.read()
                cliente.sendall(f"subir {nombre_archivo} {len(contenido)}".encode('utf-8'))
                cliente.sendall(contenido)
            except FileNotFoundError:
                print(f"Error: El archivo {nombre_archivo} no existe.")
                continue
        elif comando.lower().startswith("descargar "):
            _, nombre_archivo = comando.split()
            cliente.sendall(comando.encode('utf-8'))
            respuesta = cliente.recv(4096).decode('utf-8', errors='replace')
            if respuesta.startswith("tamano "):
                _, tamano = respuesta.split()
                tamano = int(tamano)
                with open(nombre_archivo, 'wb') as f:
                    while tamano > 0:
                        datos = cliente.recv(min(4096, tamano))
                        f.write(datos)
                        tamano -= len(datos)
                print(f"Archivo {nombre_archivo} descargado correctamente.")
            else:
                print(respuesta)
        else:
            salida_bytes = cliente.recv(4096)
            salida = salida_bytes.decode('utf-8', errors='replace')
            print(salida)

    cliente.close()

if __name__ == '__main__':
    direccion = '127.0.0.1'
    puerto = 12345
    cliente = crear_cliente(direccion, puerto)
    interactuar_servidor(cliente)
