import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from tqdm import tqdm
import argparse

def setup_logging():
    logging.basicConfig(filename='file_copier.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def copiar_archivo(s, d):
    try:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        return None
    except Exception as e:
        return (s, d, str(e))

def copiar_directorio(src, dst, ignore_patterns=None):
    errores = []
    archivos_totales = sum([len(files) for _, _, files in os.walk(src)])
    
    with ThreadPoolExecutor() as executor:
        futuros = []
        with tqdm(total=archivos_totales, desc=f"Copiando {src.name}", unit="archivo") as pbar:
            for root, dirs, files in os.walk(src):
                for file in files:
                    s = Path(root) / file
                    d = dst / s.relative_to(src)
                    if ignore_patterns and any(s.match(pattern) for pattern in ignore_patterns):
                        continue
                    futuros.append(executor.submit(copiar_archivo, str(s), str(d)))
        
            for futuro in as_completed(futuros):
                error = futuro.result()
                if error:
                    errores.append(error)
                    logging.error(f"Error copiando {error[0]} a {error[1]}: {error[2]}")
                pbar.update(1)
    
    return errores

def main(carpetas=None, ignore_patterns=None, dst_base=None):
    setup_logging()
    user_profile = Path.home()
    carpetas_default = ["Desktop", "Escritorio", 'Pictures', 'Imágenes', 'Documents', 'Documentos', 'Music', 'Musica', 'Videos', 'Downloads', 'Descargas']
    carpetas = carpetas or carpetas_default
    dst_base = Path(dst_base) if dst_base else Path(__file__).parent

    for carpeta in carpetas:
        src = user_profile / carpeta
        dst = dst_base / f"recovery_data_{carpeta}"

        logging.info(f"Procesando: {carpeta}")
        print(f"Procesando: {carpeta}")

        if src.exists():
            errores = copiar_directorio(src, dst, ignore_patterns)
            if errores:
                logging.warning(f"Errores al copiar {carpeta}: {len(errores)} archivos no se pudieron copiar.")
                print(f"Advertencia: {len(errores)} archivos no se pudieron copiar de {carpeta}. Revise el archivo de log para más detalles.")
        else:
            logging.warning(f"La carpeta {carpeta} no existe")
            print(f"La carpeta {carpeta} no existe")

    print("Proceso completado. Revise el archivo 'file_copier.log' para más detalles.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copia carpetas del directorio de inicio del usuario.")
    parser.add_argument("--carpetas", nargs="*", help="Lista de carpetas para copiar")
    parser.add_argument("--ignore", nargs="*", help="Patrones de archivos a ignorar")
    parser.add_argument("--dst", help="Directorio base de destino")
    args = parser.parse_args()

    main(carpetas=args.carpetas, ignore_patterns=args.ignore, dst_base=args.dst)