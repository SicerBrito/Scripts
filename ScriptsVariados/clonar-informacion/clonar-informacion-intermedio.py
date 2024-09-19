# No funciona correctamente. La idea es que el proceso sea mas rapido mediante sub procesos

import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def copiar_archivo(s, d):
    try:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        return None
    except Exception as e:
        return (s, d, str(e))

def copiar_directorio(src, dst):
    errores = []
    with ThreadPoolExecutor() as executor:
        futuros = []
        for root, dirs, files in os.walk(src):
            for file in files:
                s = os.path.join(root, file)
                d = os.path.join(dst, os.path.relpath(s, src))
                futuros.append(executor.submit(copiar_archivo, s, d))
        
        for futuro in as_completed(futuros):
            error = futuro.result()
            if error:
                errores.append(error)
    
    return errores

def main():
    user_profile = Path.home()
    carpetas = ["Desktop", "Escritorio", 'Pictures', 'Imágenes', 'Documents', 'Documentos', 'Music', 'Musica', 'Videos', 'Downloads', 'Descargas']

    for carpeta in carpetas:
        src = user_profile / carpeta
        dst = Path(__file__).parent / f"recovery_data_{carpeta}"

        print(f"Procesando: {carpeta}")

        if os.path.exists(src):
            errores = copiar_directorio(src, dst)
            if errores:
                print(f"Error al copiar {carpeta}: {errores}")
        else:
            print(f"La carpeta {carpeta} no existe")

if __name__ == "__main__":
    main()

