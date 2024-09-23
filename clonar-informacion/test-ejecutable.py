import subprocess
import os

# Ruta al ejecutable (ajusta esto a tu ruta real)
executable_path = r"C:\Users\ING_LICITACIONES\Desktop\Sicer\Pruebas\Scripts\ScriptsVariados\clonar-informacion\build\exe.win-amd64-3.12"

# Ejecuta el programa y captura la salida
try:
    result = subprocess.run([executable_path], capture_output=True, text=True, timeout=10)
    print("Salida estándar:", result.stdout)
    print("Salida de error:", result.stderr)
except subprocess.TimeoutExpired:
    print("El programa se ejecutó por más de 10 segundos sin terminar.")
except Exception as e:
    print(f"Ocurrió un error al ejecutar el programa: {e}")

# Pausa para que puedas ver el resultado
input("Presiona Enter para cerrar...")
