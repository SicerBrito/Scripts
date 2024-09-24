# Documentación de Automatización con Bash (Linux) y Batch (Windows)

## Autor: [Sicer Andres Brito Gutierrez](https://github.com/SicerBrito) 🧑‍💻

Esta documentación cubre la automatización realizada con Bash para sistemas Linux y su equivalente en Batch para sistemas Windows.

## 1. Permisos (Solo para Linux)

En sistemas Linux, es necesario otorgar permisos de ejecución al script antes de ejecutarlo.

### Otorgar permisos de ejecución

```bash
chmod +x init.sh
```

Este comando da permisos de ejecución al archivo `init.sh`.

### Otorgar todos los permisos (incluyendo sudo)

```bash
chmod 777 init.sh
```

Este comando otorga todos los permisos al archivo `init.sh`, incluyendo permisos de superusuario.

> **Nota**: Usar `chmod 777` puede ser un riesgo de seguridad. Úsalo con precaución y solo cuando sea absolutamente necesario.

## 2. Ejecución

### Linux

Para ejecutar el script en Linux, usa uno de estos comandos:

```bash
./init.sh
```
o
```bash
bash init.sh
```

### Windows

En Windows, los scripts batch tienen la extensión `.bat` o `.cmd`. Para ejecutar un script batch:

1. Abre el Explorador de archivos y navega hasta la ubicación del script.
2. Haz doble clic en el archivo `.bat` o `.cmd`.

Alternativamente, puedes ejecutarlo desde la línea de comandos:

```cmd
init.bat
```
o
```cmd
init.cmd
```

> **Nota**: Asegúrate de abrir la terminal o el símbolo del sistema en el directorio donde se encuentra el script, o proporciona la ruta completa al archivo.

## 3. Consejos Adicionales

- **Linux**: Puedes hacer que un script Bash sea ejecutable en cualquier lugar añadiendo su directorio al PATH o moviéndolo a un directorio que ya esté en el PATH (como `/usr/local/bin`).

- **Windows**: Puedes ejecutar scripts batch desde cualquier lugar añadiendo su directorio a la variable de entorno PATH.

- Para ambos sistemas, considera usar variables de entorno para almacenar información sensible en lugar de incluirla directamente en los scripts.

- Siempre revisa cuidadosamente los scripts antes de ejecutarlos, especialmente si requieren permisos elevados.

---

Para más información sobre scripting en Bash o Batch, consulta la documentación oficial:
- [Bash Manual](https://www.gnu.org/software/bash/manual/)
- [Windows Batch Scripting](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands)