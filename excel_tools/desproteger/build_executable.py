"""
Script para compilar Excel Tool como ejecutable
Este script automatiza la creación del .exe con PyInstaller
"""

import subprocess
import sys
import os
from pathlib import Path

def verificar_dependencias():
    """Verifica que todo esté instalado"""
    print("🔍 Verificando dependencias...")
    
    faltantes = []
    
    # Verificar PyInstaller (es un comando, no un módulo importable)
    try:
        result = subprocess.run(['pyinstaller', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ PyInstaller ({version})")
        else:
            print(f"   ❌ PyInstaller")
            faltantes.append('PyInstaller')
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print(f"   ❌ PyInstaller")
        faltantes.append('PyInstaller')
    
    # Verificar pywin32
    try:
        import win32com
        print(f"   ✅ pywin32")
    except ImportError:
        print(f"   ❌ pywin32")
        faltantes.append('pywin32')
    
    # Verificar tkinter
    try:
        import tkinter
        print(f"   ✅ tkinter (incluido en Python)")
    except ImportError:
        print(f"   ❌ tkinter (incluido en Python)")
        faltantes.append('tkinter')
    
    if faltantes:
        print(f"\n⚠️  Faltan dependencias: {', '.join(faltantes)}")
        print("\nInstálalas con:")
        if 'PyInstaller' in faltantes:
            print("   pip install pyinstaller")
        if 'pywin32' in faltantes:
            print("   pip install pywin32")
        return False
    
    print("✅ Todas las dependencias están instaladas\n")
    return True


def crear_spec_file():
    """Crea un archivo .spec personalizado para PyInstaller"""
    
    print("📝 Creando archivo de configuración (.spec)...")
    
    # Verificar si existe el ícono
    icon_path = Path("excel_tool.ico")
    icon_option = f"icon='{icon_path}'" if icon_path.exists() else "icon=None"
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['excel_tool_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['win32com.client', 'win32com.gen_py', 'pythoncom', 'pywintypes'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ExcelTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin consola (modo GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    {icon_option},
    version_file=None,
)
"""
    
    with open("ExcelTool.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec creado\n")
    return True


def compilar_ejecutable(usar_spec=True):
    """Compila el ejecutable usando PyInstaller"""
    
    print("=" * 70)
    print("🔨 COMPILANDO EJECUTABLE")
    print("=" * 70)
    print()
    
    if usar_spec and Path("ExcelTool.spec").exists():
        # Compilar usando el archivo .spec
        print("📦 Compilando con archivo .spec...\n")
        comando = ["pyinstaller", "ExcelTool.spec", "--clean"]
    else:
        # Compilar con opciones en línea de comandos
        print("📦 Compilando con opciones en línea...\n")
        
        comando = [
            "pyinstaller",
            "--name=ExcelTool",
            "--onefile",  # Un solo archivo .exe
            "--windowed",  # Sin consola
            "--clean",
            "--noconfirm"  # No preguntar, sobrescribir
        ]
        
        # Agregar ícono si existe
        if Path("excel_tool.ico").exists():
            comando.append("--icon=excel_tool.ico")
        
        # Hidden imports necesarios para win32com
        comando.extend([
            "--hidden-import=win32com.client",
            "--hidden-import=win32com.gen_py",
            "--hidden-import=pythoncom",
            "--hidden-import=pywintypes"
        ])
        
        comando.append("excel_tool_gui.py")
    
    try:
        # Ejecutar PyInstaller
        resultado = subprocess.run(comando, check=True, capture_output=False)
        
        print()
        print("=" * 70)
        print("✅ COMPILACIÓN EXITOSA")
        print("=" * 70)
        
        # Buscar el ejecutable
        exe_path = Path("dist/ExcelTool.exe")
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n📁 Ejecutable creado:")
            print(f"   Ubicación: {exe_path.absolute()}")
            print(f"   Tamaño: {size_mb:.2f} MB")
            print(f"\n💡 Puedes distribuir este archivo .exe sin necesidad de Python")
        else:
            print("\n⚠️  No se encontró el ejecutable en dist/ExcelTool.exe")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 70)
        print("❌ ERROR EN LA COMPILACIÓN")
        print("=" * 70)
        print(f"\nDetalles: {e}")
        return False


def limpiar_archivos_temporales():
    """Limpia archivos generados por PyInstaller"""
    print("\n🧹 ¿Deseas limpiar archivos temporales? (s/n): ", end="")
    respuesta = input().lower().strip()
    
    if respuesta == 's':
        print("🧹 Limpiando archivos temporales...")
        
        import shutil
        
        carpetas = ["build", "__pycache__"]
        archivos = ["ExcelTool.spec"]
        
        for carpeta in carpetas:
            if Path(carpeta).exists():
                shutil.rmtree(carpeta)
                print(f"   ✅ Eliminado: {carpeta}/")
        
        for archivo in archivos:
            if Path(archivo).exists():
                os.remove(archivo)
                print(f"   ✅ Eliminado: {archivo}")
        
        print("✅ Limpieza completada")


def main():
    print("=" * 70)
    print("🚀 COMPILADOR DE EXCEL TOOL")
    print("=" * 70)
    print()
    
    # Verificar que existe el archivo principal
    if not Path("excel_tool_gui.py").exists():
        print("❌ Error: No se encuentra 'excel_tool_gui.py'")
        print("   Asegúrate de que este script esté en la misma carpeta")
        input("\nPresiona Enter para salir...")
        return
    
    # Paso 1: Verificar dependencias
    if not verificar_dependencias():
        input("\nPresiona Enter para salir...")
        return
    
    # Paso 2: Crear archivo .spec
    print("¿Deseas crear un archivo .spec personalizado? (s/n): ", end="")
    respuesta = input().lower().strip()
    usar_spec = respuesta == 's'
    
    if usar_spec:
        crear_spec_file()
    
    print()
    
    # Paso 3: Compilar
    print("🚀 Iniciando compilación...")
    print("   (Esto puede tardar varios minutos)\n")
    
    if compilar_ejecutable(usar_spec):
        # Paso 4: Limpiar (opcional)
        limpiar_archivos_temporales()
        
        print("\n" + "=" * 70)
        print("✅ PROCESO COMPLETADO")
        print("=" * 70)
        print("\n💡 Instrucciones:")
        print("   1. El ejecutable está en: dist/ExcelTool.exe")
        print("   2. Puedes moverlo a cualquier carpeta")
        print("   3. No necesita Python instalado para funcionar")
        print("   4. Distribúyelo libremente")
    else:
        print("\n⚠️  La compilación falló. Revisa los errores arriba.")
    
    input("\nPresiona Enter para salir...")


if __name__ == "__main__":
    main()