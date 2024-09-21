# La mejor version hasta el momento
import os
import shutil
from pathlib import Path

def copiar_directorio(src, dst):
    errores = []
    try:
        if os.path.isdir(src):
            if not os.path.exists(dst):
                os.makedirs(dst)
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                try:
                    if os.path.isdir(s):
                        copiar_directorio(s, d)
                    else:
                        shutil.copy2(s, d)
                except Exception as e:
                    errores.append((s, d, str(e)))
        else:
            shutil.copy2(src, dst)
    except Exception as e:
        errores.append((src, dst, str(e)))
    return errores

def main():
    user_profile = Path.home()
    carpetas = ["Documents", "Downloads", "Desktop", "Music", "Videos", "Pictures"]

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
