import os
import shutil

home_folder = os.path.expanduser('~')
folder404 = "404NotFoundMyFriend"

# Reemplaza las barras diagonales invertidas por barras diagonales normales
newhome = home_folder.replace('\\', '/') + '/'
rutaActual = os.path.abspath(os.getcwd()).replace('\\', '/')

# Lista de nombres de carpetas objetivo
carpetas_objetivo = ['Pictures', 'Imágenes', 'Documents', 'Documentos', 'Music', 'Musica', 'Videos', 'Downloads', 'Descargas']

if __name__ == '__main__':
    for filename in os.listdir(newhome):
        print(f'Procesando: {filename}')
        if filename in carpetas_objetivo:
            source_folder = os.path.join(newhome, filename)
            target_folder = os.path.join(rutaActual, f'recovery_data_{filename}')

            if os.path.exists(source_folder):
                try:
                    shutil.copytree(source_folder, target_folder)
                    print(f'Copiando {filename} a {target_folder}')
                except PermissionError as e:
                    print(f'Error de permiso al copiar {filename}: {e}')
                except Exception as e:
                    print(f'Error al copiar {filename}: {e}')
            else:
                print(f'{filename} no encontrado en {newhome}')
