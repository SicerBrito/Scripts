import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import argparse
import time
import multiprocessing
import zipfile

def setup_logging(script_dir):
    log_file = script_dir / 'file_copier.log'
    logging.basicConfig(filename=str(log_file), level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def copiar_archivo(s, d, compress=False, simulate=False):
    try:
        if simulate:
            return None
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if compress:
            with zipfile.ZipFile(f"{d}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(s, Path(s).name)
        else:
            shutil.copy2(s, d)
        return None
    except Exception as e:
        return (s, d, str(e))

def simple_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total: 
        print()

def copiar_directorio(src, dst, ignore_patterns=None, compress=False, simulate=False):
    errores = []
    archivos_totales = sum([len(files) for _, _, files in os.walk(src)])
    archivos_copiados = 0

    max_workers = multiprocessing.cpu_count()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futuros = []
        for root, dirs, files in os.walk(src):
            for file in files:
                s = Path(root) / file
                d = dst / s.relative_to(src)
                if ignore_patterns and any(s.match(pattern) for pattern in ignore_patterns):
                    continue
                futuros.append(executor.submit(copiar_archivo, str(s), str(d), compress, simulate))
        
        for futuro in as_completed(futuros):
            error = futuro.result()
            if error:
                errores.append(error)
                logging.error(f"Error copiando {error[0]} a {error[1]}: {error[2]}")
            archivos_copiados += 1
            if archivos_copiados % 100 == 0 or archivos_copiados == archivos_totales:
                simple_progress_bar(archivos_copiados, archivos_totales, prefix=f"{'Simulando' if simulate else 'Copiando'} {src.name}", suffix='Completado', length=30)
    
    return errores

def main(carpetas=None, ignore_patterns=None, dst_base=None, compress=False, simulate=False):
    script_dir = Path(__file__).parent
    setup_logging(script_dir)
    
    user_profile = Path.home()
    carpetas_default = ["Desktop", "Escritorio", 'Pictures', 'Imágenes', 'Documents', 'Documentos', 'Music', 'Musica', 'Videos', 'Downloads', 'Descargas']
    carpetas = carpetas or carpetas_default
    dst_base = Path(dst_base) if dst_base else script_dir

    start_time = time.time()

    for carpeta in carpetas:
        src = user_profile / carpeta
        dst = dst_base / f"recovery_data_{carpeta}"

        logging.info(f"{'Simulando' if simulate else 'Procesando'}: {carpeta}")
        print(f"{'Simulando' if simulate else 'Procesando'}: {carpeta}")

        if src.exists():
            errores = copiar_directorio(src, dst, ignore_patterns, compress, simulate)
            if errores:
                logging.warning(f"Errores al {'simular' if simulate else 'copiar'} {carpeta}: {len(errores)} archivos no se pudieron procesar.")
                print(f"Advertencia: {len(errores)} archivos no se pudieron procesar de {carpeta}. Revise el archivo de log para más detalles.")
        else:
            logging.warning(f"La carpeta {carpeta} no existe")
            print(f"La carpeta {carpeta} no existe")

    end_time = time.time()
    duration = end_time - start_time
    print(f"Proceso completado en {duration:.2f} segundos.")
    print(f"Archivo de log creado en: {script_dir / 'file_copier.log'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copia carpetas del directorio de inicio del usuario.")
    parser.add_argument("--carpetas", nargs="*", help="Lista de carpetas para copiar")
    parser.add_argument("--ignore", nargs="*", help="Patrones de archivos a ignorar")
    parser.add_argument("--dst", help="Directorio base de destino")
    parser.add_argument("--compress", action="store_true", help="Comprimir archivos copiados")
    parser.add_argument("--simulate", action="store_true", help="Simular la copia sin realizar cambios")
    args = parser.parse_args()

    main(carpetas=args.carpetas, ignore_patterns=args.ignore, dst_base=args.dst, compress=args.compress, simulate=args.simulate)