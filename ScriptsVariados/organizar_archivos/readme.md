# Documentación: Organizador de Archivos en Python

Autor: Sicer Andres Brito Gutierrez

## Archivo de referencia
`organizador_archivos.py`

## Descripción
Este script de Python implementa un Organizador de Archivos con una interfaz gráfica de usuario (GUI) y opciones de línea de comandos. Permite organizar archivos en carpetas basándose en sus extensiones, con opciones para procesamiento recursivo, simulación de operaciones y deshacer cambios.

## Requisitos
- Python 3.x
- Bibliotecas estándar de Python (os, shutil, argparse, logging, json, tkinter)

## Funcionalidades principales

1. **Organización de archivos**: Mueve archivos a carpetas específicas basándose en sus extensiones.
2. **Configuración personalizable**: Utiliza un archivo JSON para definir reglas de organización.
3. **Modo recursivo**: Opción para organizar archivos en subdirectorios.
4. **Modo de simulación**: Permite visualizar cambios sin realizar movimientos reales de archivos.
5. **Función de deshacer**: Capacidad para revertir la organización realizada.
6. **Interfaz gráfica**: GUI intuitiva para facilitar el uso.
7. **Interfaz de línea de comandos**: Opción para uso en scripts o automatizaciones.
8. **Registro de operaciones**: Mantiene un log detallado de todas las acciones realizadas.

## Clase principal: OrganizadorArchivos

### Métodos principales

#### `__init__(self)`
Inicializa el organizador, configura el logging y carga la configuración.

#### `cargar_config(self)`
Carga la configuración desde `config.json` o crea una configuración por defecto.

#### `guardar_config(self)`
Guarda la configuración actual en `config.json`.

#### `organizar_archivos(self, directorio, recursivo=False, simular=False)`
Organiza los archivos en el directorio especificado.

#### `procesar_archivo(self, root, archivo, simular)`
Procesa un archivo individual, moviéndolo a la carpeta correspondiente.

#### `deshacer_organizacion(self)`
Revierte las operaciones de organización realizadas.

#### `interfaz_grafica(self)`
Crea y muestra la interfaz gráfica de usuario.

## Interfaz gráfica

La GUI incluye:
- Campo para seleccionar el directorio a organizar
- Opciones para modo recursivo y simulación
- Botones para organizar y deshacer
- Área de log para mostrar las operaciones realizadas

## Uso por línea de comandos

```
python organizador_archivos.py [directorio] [-r] [-s] [-c]
```

Opciones:
- `directorio`: Directorio a organizar (opcional, por defecto es el directorio actual)
- `-r`, `--recursivo`: Organizar subdirectorios recursivamente
- `-s`, `--simular`: Simular la organización sin mover archivos
- `-c`, `--consola`: Usar interfaz de línea de comandos en lugar de GUI

## Configuración

El archivo `config.json` contiene las reglas de organización. Cada entrada asocia una extensión de archivo con una carpeta destino.

Ejemplo:
```json
{
    "reglas": {
        "txt": "Documentos/Texto",
        "jpg": "Imágenes",
        "mp3": "Audio"
    }
}
```

## Registro de operaciones

El script mantiene un log detallado en `organizador_archivos.log`, que incluye todas las operaciones realizadas.

## Consideraciones y limitaciones

- El script requiere permisos de lectura y escritura en los directorios que se intentan organizar.
- La función de deshacer solo funciona para la sesión actual y se pierde al cerrar el programa.
- El rendimiento puede verse afectado en directorios con un gran número de archivos.

## Solución de problemas

- Si el script no se ejecuta, verifique que tiene instalado Python 3.x y las bibliotecas necesarias.
- Si no se pueden mover algunos archivos, asegúrese de tener los permisos necesarios en el sistema de archivos.
- Para problemas con la configuración, elimine el archivo `config.json` y reinicie el script para crear una nueva configuración por defecto.

## Soporte

Para preguntas o problemas relacionados con este script, contacte al autor, Sicer Andres Brito Gutierrez.

---

*Nota: Utilice este script con responsabilidad y asegúrese de tener copias de seguridad de sus archivos importantes antes de organizar.*