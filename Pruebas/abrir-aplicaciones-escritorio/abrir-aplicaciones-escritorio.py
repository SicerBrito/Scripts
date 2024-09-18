import os
import subprocess
import time
import pyautogui
import winreg

def get_install_location(app_name, reg_key, reg_value):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key)
        value, _ = winreg.QueryValueEx(key, reg_value)
        winreg.CloseKey(key)
        return value
    except:
        print(f"No se pudo encontrar la ubicación de instalación de {app_name}")
        return None

def open_app(app_name):
    app_paths = {
        "Docker Desktop": r"C:\Program Files\Docker\Docker\Docker Desktop.exe",
        "pgAdmin": r"C:\Program Files\pgAdmin 4\v6\runtime\pgAdmin4.exe",
        "WhatsApp": os.path.expandvars(r"%LOCALAPPDATA%\WhatsApp\WhatsApp.exe"),
        "GitHub Desktop": os.path.expandvars(r"%LOCALAPPDATA%\GitHubDesktop\GitHubDesktop.exe"),
        "Visual Studio Code": os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
        "Visual Studio": get_install_location("Visual Studio", r"SOFTWARE\Microsoft\VisualStudio\SxS\VS7", "17.0"),
        "Chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    }
    
    path = app_paths.get(app_name)
    if path and os.path.exists(path):
        subprocess.Popen(path)
        print(f"Abriendo {app_name}")
    else:
        print(f"No se pudo encontrar o abrir {app_name}")

def main():
    apps = ["Docker Desktop", "pgAdmin", "WhatsApp", "GitHub Desktop", "Visual Studio Code", "Visual Studio", "Chrome"]
    
    for app in apps:
        open_app(app)
        time.sleep(2)  # Esperar un poco entre cada apertura
    
    # Abrir el Explorador de Archivos
    subprocess.Popen("explorer.exe")
    
    # Restaurar pestañas en Chrome
    time.sleep(5)  # Esperar a que Chrome se abra completamente
    for _ in range(4):
        pyautogui.hotkey('ctrl', 'shift', 't')
        time.sleep(0.5)

if __name__ == "__main__":
    main()