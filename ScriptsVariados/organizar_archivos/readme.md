# Documentación: Organizador de Archivos Avanzado

## Autor
Sicer Andrés Brito Gutiérrez

## Referencia
[Enlace al archivo del script](paste.txt)

## Descripción General
Este script de Python implementa un Organizador de Archivos Avanzado con interfaz gráfica y de línea de comandos. Permite organizar archivos en carpetas específicas basadas en sus extensiones, con opciones para procesamiento recursivo y simulación.

## Características Principales
1. Interfaz gráfica de usuario (GUI) y interfaz de línea de comandos (CLI)
2. Organización de archivos basada en extensiones
3. Opción de procesamiento recursivo de subdirectorios
4. Modo de simulación para previsualizar cambios
5. Función de deshacer para revertir la organización
6. Registro de operaciones realizadas
7. Configuración personalizable mediante archivo JSON

## Requisitos
- Python 3.x
- Bibliotecas estándar de Python (no se requieren instalaciones adicionales)

## Clases y Métodos Principales

### Clase OrganizadorArchivos

#### Métodos:
- `__init__()`: Inicializa el organizador, configura el logging y carga la configuración.
- `configurar_logging()`: Configura el sistema de registro.
- `cargar_config()`: Carga la configuración desde un archivo JSON o usa una configuración por defecto.
- `guardar_config()`: Guarda la configuración actual en un archivo JSON.
- `organizar_archivos(directorio, recursivo, simular)`: Organiza los archivos en el directorio especificado.
- `procesar_archivo(root, archivo, simular)`: Procesa un archivo individual, moviéndolo a la carpeta correspondiente.
- `deshacer_organizacion()`: Revierte las operaciones de organización realizadas.
- `interfaz_grafica()`: Crea y muestra la interfaz gráfica de usuario.
- `seleccionar_directorio()`: Abre un diálogo para seleccionar el directorio a organizar.
- `ejecutar_organizacion()`: Inicia el proceso de organización desde la GUI.
- `mostrar_log()`: Muestra el registro de operaciones en la GUI.

## Uso de la Interfaz Gráfica
1. Ejecute el script en Python.
2. Use el botón "Seleccionar" para elegir el directorio a organizar.
3. Marque las opciones deseadas (Recursivo, Simular).
4. Haga clic en "Organizar" para iniciar el proceso.
5. Revise el log para ver las operaciones realizadas.
6. Use "Deshacer" si necesita revertir la organización.

## Uso de la Línea de Comandos
```
python script.py [directorio] [-r] [-s] [-c]
```
- `directorio`: Ruta del directorio a organizar (opcional, por defecto es el directorio actual)
- `-r` o `--recursivo`: Organiza subdirectorios recursivamente
- `-s` o `--simular`: Simula la organización sin mover archivos
- `-c` o `--consola`: Usa la interfaz de línea de comandos en lugar de la GUI

## Configuración
El script utiliza un archivo `config.json` para personalizar las reglas de organización. Si no existe, se crea uno con reglas predeterminadas para diversas extensiones de archivo comunes.

## Registro de Operaciones
Todas las operaciones se registran en el archivo `organizador_archivos.log`.

## Soporte
Para soporte o consultas, contacte al autor:
Discord: SicerBrito#1610

## Nota de Responsabilidad
Este script se proporciona tal cual, sin garantías de ningún tipo. El autor no se hace responsable de cualquier daño o uso indebido que pueda resultar de la utilización de este script. Se insta a los usuarios a utilizarlo de manera responsable y ética, y a realizar copias de seguridad de sus archivos antes de usar esta herramienta.