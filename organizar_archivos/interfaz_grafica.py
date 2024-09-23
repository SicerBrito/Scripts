import os
import shutil
import argparse
import logging
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

class OrganizadorArchivos:
    def __init__(self):
        self.operaciones = []
        self.configurar_logging()
        self.cargar_config()

    def configurar_logging(self):
        logging.basicConfig(filename='organizador_archivos.log', level=logging.INFO,
                            format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    def cargar_config(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
                "reglas": {
                    # Documentos
                    "txt": "Documentos/Texto",
                    "pdf": "Documentos/PDF",
                    "doc": "Documentos/Word",
                    "docx": "Documentos/Word",
                    "rtf": "Documentos/Word",
                    "xls": "Documentos/Excel",
                    "xlsx": "Documentos/Excel",
                    "csv": "Documentos/Excel",
                    "ppt": "Documentos/PowerPoint",
                    "pptx": "Documentos/PowerPoint",
                    
                    # Imágenes
                    "jpg": "Imágenes",
                    "jpeg": "Imágenes",
                    "png": "Imágenes",
                    "gif": "Imágenes",
                    "bmp": "Imágenes",
                    "tiff": "Imágenes",

                    # Iconos
                    "ico": "Iconos",

                    # Audio
                    "mp3": "Audio",
                    "wav": "Audio",
                    "flac": "Audio",
                    "m4a": "Audio",
                    
                    # Video
                    "mp4": "Video",
                    "avi": "Video",
                    "mkv": "Video",
                    "mov": "Video",
                    
                    # Comprimidos
                    "zip": "Comprimidos",
                    "rar": "Comprimidos",
                    "7z": "Comprimidos",
                    "tar": "Comprimidos",
                    "gz": "Comprimidos",
                    
                    # Instaladores y Aplicaciones
                    "exe": "Aplicaciones/Instaladores",
                    "msi": "Aplicaciones/Instaladores",
                    "app": "Aplicaciones/Instaladores",
                    "dmg": "Aplicaciones/Instaladores",
                    
                    # Accesos directos
                    "lnk": "Accesos Directos",
                    "url": "Accesos Directos",
                    
                    # Código
                    "py": "Código/Python",
                    "java": "Código/Java",
                    "cpp": "Código/C++",
                    "css": "Código/C#",
                    "html": "Código/Web",
                    "css": "Código/Web",
                    "js": "Código/Web",
                    
                    # Otros tipos comunes
                    "iso": "Imágenes de Disco",
                    "torrent": "Torrents"
                }
            }

    def guardar_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def organizar_archivos(self, directorio, recursivo=False, simular=False):
        for root, dirs, files in os.walk(directorio):
            for archivo in files:
                self.procesar_archivo(root, archivo, simular)
            if not recursivo:
                break

    def procesar_archivo(self, root, archivo, simular):
        ruta_completa = os.path.join(root, archivo)
        extension = os.path.splitext(archivo)[1][1:].lower()
        carpeta_destino = self.config["reglas"].get(extension, "Otros")
        
        destino = os.path.join(root, carpeta_destino, archivo)
        if not simular:
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            if os.path.exists(destino):
                base, ext = os.path.splitext(destino)
                counter = 1
                while os.path.exists(f"{base}_{counter}{ext}"):
                    counter += 1
                destino = f"{base}_{counter}{ext}"
            shutil.move(ruta_completa, destino)
            self.operaciones.append((ruta_completa, destino))
        
        logging.info(f"{'Simulado: ' if simular else ''}Movido {archivo} a {carpeta_destino}")

    def deshacer_organizacion(self):
        for origen, destino in reversed(self.operaciones):
            shutil.move(destino, origen)
            logging.info(f"Deshecho: Movido {os.path.basename(destino)} de vuelta a {origen}")
        self.operaciones.clear()

    def interfaz_grafica(self):
        root = tk.Tk()
        root.title("Organizador de Archivos")
        root.geometry("600x400")
        root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Directory selection
        dir_frame = ttk.Frame(main_frame)
        dir_frame.pack(fill=tk.X, pady=5)

        self.entry_dir = ttk.Entry(dir_frame, width=50)
        self.entry_dir.pack(side=tk.LEFT, expand=True, fill=tk.X)

        select_btn = ttk.Button(dir_frame, text="Seleccionar", command=self.seleccionar_directorio)
        select_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Options
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=5)

        self.var_recursivo = tk.BooleanVar()
        recursivo_check = ttk.Checkbutton(options_frame, text="Recursivo", variable=self.var_recursivo)
        recursivo_check.pack(side=tk.LEFT, padx=(0, 10))

        self.var_simular = tk.BooleanVar()
        simular_check = ttk.Checkbutton(options_frame, text="Simular", variable=self.var_simular)
        simular_check.pack(side=tk.LEFT)

        # Action buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        organizar_btn = ttk.Button(btn_frame, text="Organizar", command=self.ejecutar_organizacion)
        organizar_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        deshacer_btn = ttk.Button(btn_frame, text="Deshacer", command=self.deshacer_organizacion)
        deshacer_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))

        # Log display
        log_frame = ttk.LabelFrame(main_frame, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.log_text = ScrolledText(log_frame, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        root.mainloop()

    def seleccionar_directorio(self):
        directorio = filedialog.askdirectory()
        if directorio:
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, directorio)

    def ejecutar_organizacion(self):
        directorio = self.entry_dir.get()
        recursivo = self.var_recursivo.get()
        simular = self.var_simular.get()
        self.organizar_archivos(directorio, recursivo, simular)
        messagebox.showinfo("Completado", "Organización de archivos completada.")
        self.mostrar_log()

    def mostrar_log(self):
        with open('organizador_archivos.log', 'r') as log_file:
            log_content = log_file.read()
            self.log_text.delete('1.0', tk.END)
            self.log_text.insert(tk.END, log_content)
            self.log_text.see(tk.END)

def main():
    parser = argparse.ArgumentParser(description="Organizador de archivos avanzado")
    parser.add_argument("directorio", nargs="?", default=".", help="Directorio a organizar")
    parser.add_argument("-r", "--recursivo", action="store_true", help="Organizar subdirectorios recursivamente")
    parser.add_argument("-s", "--simular", action="store_true", help="Simular la organización sin mover archivos")
    parser.add_argument("-c", "--consola", action="store_true", help="Usar interfaz de línea de comandos")
    args = parser.parse_args()

    organizador = OrganizadorArchivos()

    if args.consola:
        organizador.organizar_archivos(args.directorio, args.recursivo, args.simular)
    else:
        organizador.interfaz_grafica()

if __name__ == "__main__":
    main()