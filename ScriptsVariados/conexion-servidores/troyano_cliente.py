import socket

def crear_cliente(direccion, puerto):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((direccion, puerto))
    return cliente

def interactuar_servidor(cliente):
    while True:
        comando = input('Ingresa un comando (o "salir" para terminar): ')
        cliente.sendall(comando.encode('utf-8'))

        if comando.lower() == 'salir':
            break

        salida_bytes = cliente.recv(1024)
        salida = salida_bytes.decode('utf-8', errors='replace')
        print(salida)

    cliente.close()

if __name__ == '__main__':
    direccion = '127.0.0.1'
    puerto = 12345
    cliente = crear_cliente(direccion, puerto)
    interactuar_servidor(cliente)
