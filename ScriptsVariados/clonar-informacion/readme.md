# Documentación del Script de Copia de Archivos

Autor: Sicer Andres Brito Gutierrez

## Archivo de referencia
`clonar-informacion-version-final.py`

## Descripción General

Este script es una herramienta de línea de comandos diseñada para copiar o simular la copia de directorios específicos del perfil de usuario a un destino designado. Ofrece funcionalidades como compresión de archivos, ignorar patrones específicos y simulación de operaciones.

## Características Principales

1. Copia múltiples directorios del perfil de usuario.
2. Opción para comprimir archivos durante la copia.
3. Capacidad para ignorar archivos basados en patrones.
4. Modo de simulación para previsualizar operaciones sin realizar cambios.
5. Manejo de errores y logging detallado.
6. Barra de progreso en tiempo real.
7. Procesamiento multihilo para mejorar el rendimiento.

## Requisitos

- Python 3.6+
- Bibliotecas estándar de Python (no se requieren instalaciones adicionales)

## Uso

```
python script_name.py [--carpetas CARPETAS [CARPETAS ...]] [--ignore IGNORE [IGNORE ...]] 
                      [--dst DST] [--compress] [--simulate]
```

### Argumentos

- `--carpetas`: Lista opcional de carpetas para copiar. Si no se especifica, se usará una lista predeterminada.
- `--ignore`: Patrones de archivos a ignorar durante la copia.
- `--dst`: Directorio base de destino para las copias.
- `--compress`: Activa la compresión de archivos copiados.
- `--simulate`: Realiza una simulación sin efectuar cambios reales.

## Estructura del Código

### Funciones Principales

1. `setup_logging(script_dir)`: Configura el sistema de logging.
2. `copiar_archivo(s, d, compress=False, simulate=False)`: Copia un archivo individual.
3. `simple_progress_bar(...)`: Muestra una barra de progreso en la consola.
4. `copiar_directorio(src, dst, ignore_patterns=None, compress=False, simulate=False)`: Gestiona la copia de un directorio completo.
5. `main(...)`: Función principal que coordina todo el proceso.

### Flujo de Ejecución

1. Parseo de argumentos de línea de comandos.
2. Configuración del logging.
3. Determinación de las carpetas a copiar.
4. Iteración sobre cada carpeta:
   - Verificación de existencia.
   - Copia o simulación de copia.
   - Manejo de errores.
5. Resumen final del proceso.

## Detalles de Implementación

### Manejo de Errores
- Utiliza un sistema de logging para registrar errores y advertencias.
- Los errores durante la copia de archivos individuales no detienen el proceso completo.

### Optimización de Rendimiento
- Emplea `ThreadPoolExecutor` para copiar archivos en paralelo.
- El número de trabajadores se ajusta automáticamente al número de núcleos de CPU.

### Flexibilidad
- Permite especificar carpetas personalizadas o usar una lista predeterminada.
- Ofrece opciones para ignorar ciertos archivos y comprimir durante la copia.

### Feedback al Usuario
- Muestra una barra de progreso en tiempo real.
- Proporciona resúmenes de errores y tiempo total de ejecución.

## Mejores Prácticas Implementadas

1. **Uso de `pathlib`**: Mejora la portabilidad y legibilidad del manejo de rutas.
2. **Manejo de excepciones**: Captura y registra errores sin interrumpir el proceso principal.
3. **Configuración flexible**: Permite personalizar el comportamiento a través de argumentos de línea de comandos.
4. **Simulación**: Opción para probar el script sin realizar cambios reales.
5. **Logging**: Registro detallado de operaciones y errores para facilitar el debugging.

## Conclusión

Este script proporciona una solución robusta y flexible para la copia de directorios de usuario, con características avanzadas como compresión, simulación y manejo de errores. Su diseño modular y uso de prácticas de programación modernas lo hacen fácil de mantener y extender.

## Soporte
Para preguntas o problemas relacionados con este script, contacta al autor: Sicer Andres Brito Gutierrez.

---

*Nota: Utilice este script con responsabilidad y asegúrese de tener los permisos necesarios para copiar las carpetas del sistema.*