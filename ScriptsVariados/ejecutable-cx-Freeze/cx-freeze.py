# Instrucciones para crear un ejecutable con cx_Freeze

# 1. Instala cx_Freeze:
# pip install cx_Freeze

# 2. Crea un archivo setup.py en el mismo directorio que tu script principal:

from cx_Freeze import setup, Executable

setup(
    name = "FileCopiadorAvanzadoCXFreeze",
    version = "1.0",
    description = "Copiador de archivos avanzado",
    executables = [Executable("clonar-informacion-version-final.py", base = "Console")],
    options = {
        "build_exe": {
            "packages": ["os", "shutil", "pathlib", "logging", "argparse", "time", "multiprocessing", "zipfile"],
            "include_files": []
        }
    }
)

# 3. Ejecuta el siguiente comando en la línea de comandos:
# python setup.py build

# Esto creará una carpeta 'build' con el ejecutable y sus dependencias.

# 4. Distribuye la carpeta 'build' completa a los usuarios finales.

# Nota: Asegúrate de reemplazar "tu_script_principal.py" con el nombre real de tu archivo Python.