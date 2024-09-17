import os
import shutil

def organizar_archivos(directorio):
    # Obtener la lista de archivos en el directorio
    archivos = os.listdir(directorio)
    
    for archivo in archivos:
        # Ignorar directorios y el propio script
        if os.path.isfile(os.path.join(directorio, archivo)) and archivo != os.path.basename(__file__):
            # Obtener la extensión del archivo
            extension = os.path.splitext(archivo)[1][1:].lower()
            
            # Si no hay extensión, usar 'sin_extension' como carpeta
            if extension == "":
                extension = "sin_extension"
            
            # Crear un directorio para la extensión si no existe
            if not os.path.exists(os.path.join(directorio, extension)):
                os.makedirs(os.path.join(directorio, extension))
            
            # Mover el archivo al directorio correspondiente
            origen = os.path.join(directorio, archivo)
            destino = os.path.join(directorio, extension, archivo)
            shutil.move(origen, destino)
            print(f"Movido: {archivo} -> {extension}/")

# Obtener el directorio actual donde se encuentra el script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

print(f"Organizando archivos en: {directorio_actual}")
organizar_archivos(directorio_actual)

print("Organización completada.")