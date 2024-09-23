# Documentación: Copiador de Archivos Multihilo

## Autor
Sicer Andrés Brito Gutiérrez

## Referencia
[Enlace al archivo del script](paste.txt)

## Descripción General
Este script de Python implementa un copiador de archivos multihilo que permite copiar carpetas específicas del directorio de inicio del usuario a una ubicación de destino. Ofrece opciones para ignorar ciertos patrones de archivo, comprimir los archivos copiados y simular el proceso sin realizar cambios reales.

## Características Principales
1. Copia multihilo para mejorar el rendimiento
2. Opción para comprimir archivos durante la copia
3. Modo de simulación para previsualizar operaciones
4. Barra de progreso simple para seguimiento visual
5. Registro detallado de operaciones y errores
6. Soporte para patrones de ignorado de archivos
7. Personalización de carpetas a copiar y destino

## Requisitos
- Python 3.x
- Bibliotecas estándar de Python (no se requieren instalaciones adicionales)

## Funciones Principales

### setup_logging(script_dir)
Configura el sistema de registro para el script.

### copiar_archivo(s, d, compress=False, simulate=False)
Copia un archivo individual, con opciones para compresión y simulación.

### simple_progress_bar(iteration, total, ...)
Muestra una barra de progreso simple en la consola.

### copiar_directorio(src, dst, ignore_patterns=None, compress=False, simulate=False)
Copia un directorio completo utilizando múltiples hilos.

### main(carpetas=None, ignore_patterns=None, dst_base=None, compress=False, simulate=False)
Función principal que orquesta el proceso de copia.

## Uso
El script se puede ejecutar desde la línea de comandos con varias opciones:

```
python script.py [--carpetas CARPETA1 CARPETA2 ...] [--ignore PATRON1 PATRON2 ...] [--dst DESTINO] [--compress] [--simulate]
```

### Argumentos:
- `--carpetas`: Lista de carpetas para copiar (opcional, por defecto usa una lista predefinida)
- `--ignore`: Patrones de archivos a ignorar (opcional)
- `--dst`: Directorio base de destino (opcional, por defecto usa el directorio del script)
- `--compress`: Activa la compresión de archivos copiados
- `--simulate`: Activa el modo de simulación sin realizar cambios reales

### Ejemplos de uso:
1. Copiar carpetas por defecto:
   ```
   python script.py
   ```

2. Copiar carpetas específicas:
   ```
   python script.py --carpetas Desktop Documents
   ```

3. Ignorar ciertos tipos de archivo:
   ```
   python script.py --ignore "*.tmp" "*.log"
   ```

4. Copiar y comprimir:
   ```
   python script.py --compress
   ```

5. Simular la copia:
   ```
   python script.py --simulate
   ```

## Comportamiento por Defecto
Si no se especifican carpetas, el script intentará copiar las siguientes carpetas del perfil del usuario:
"Desktop", "Escritorio", "Pictures", "Imágenes", "Documents", "Documentos", "Music", "Musica", "Videos", "Downloads", "Descargas"

## Registro de Operaciones
Todas las operaciones y errores se registran en el archivo `file_copier.log` en el mismo directorio que el script.

## Soporte
Para soporte o consultas, contacte al autor:
Discord: SicerBrito#1610

## Nota de Responsabilidad
Este script se proporciona tal cual, sin garantías de ningún tipo. El autor no se hace responsable de cualquier daño o pérdida de datos que pueda resultar de la utilización de este script. Se recomienda encarecidamente a los usuarios que realicen copias de seguridad de sus datos importantes antes de usar esta herramienta y que verifiquen cuidadosamente los resultados de la operación de copia. Utilice el modo de simulación para comprender el comportamiento del script antes de realizar operaciones reales.