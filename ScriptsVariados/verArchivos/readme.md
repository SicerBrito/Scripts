# Documentación: Explorador de Carpetas con Búsqueda Mejorada en PowerShell

Autor: Sicer Andres Brito Gutierrez

## Archivo de referencia
`ExploraradorCarpetas.ps1` (nombre sugerido)

## Descripción
Este script de PowerShell, creado por Sicer Andres Brito Gutierrez, desarrolla una interfaz gráfica de usuario (GUI) para explorar el sistema de archivos con funcionalidades de búsqueda mejoradas. Permite a los usuarios navegar por carpetas, ver detalles de archivos y carpetas, y realizar búsquedas en la estructura de directorios.

## Requisitos
- Windows PowerShell 5.1 o superior
- Permisos para ejecutar scripts de PowerShell en el sistema

## Funcionalidades principales

### 1. Exploración de carpetas
- Muestra una estructura de árbol de carpetas y archivos.
- Carga el contenido de las carpetas de forma dinámica al expandirlas.
- Diferencia visualmente entre carpetas y archivos mediante iconos.

### 2. Búsqueda
- Permite buscar archivos y carpetas por nombre en toda la estructura cargada.
- Resalta y navega hasta los resultados encontrados.

### 3. Visualización de detalles
- Muestra información detallada del elemento seleccionado, incluyendo:
  - Ruta completa
  - Tipo (archivo o carpeta)
  - Tamaño (para archivos)
  - Fecha de última modificación

### 4. Selección de carpeta raíz
- Permite al usuario seleccionar la carpeta raíz para explorar.

## Funciones principales

### `Get-FolderContent`
Obtiene el contenido de una carpeta y lo agrega al TreeView.

#### Parámetros
- `FolderPath`: Ruta de la carpeta a explorar.
- `TreeView`: Objeto TreeView donde se agregarán los elementos.
- `ParentNode`: Nodo padre en el TreeView (opcional).

### `Search-TreeView`
Busca nodos en el TreeView que coincidan con el término de búsqueda.

#### Parámetros
- `TreeView`: Objeto TreeView donde realizar la búsqueda.
- `SearchTerm`: Término a buscar.

## Instrucciones de uso

1. Ejecute el script en PowerShell ISE o en una consola de PowerShell con permisos de ejecución de scripts.
2. En la interfaz gráfica que se abre:
   a. Haga clic en "Seleccionar Carpeta" para elegir la carpeta raíz a explorar.
   b. Use el TreeView para navegar por la estructura de carpetas.
   c. Haga clic en archivos o carpetas para ver sus detalles en el panel inferior.
   d. Use el cuadro de búsqueda y el botón "Buscar" para encontrar elementos específicos.

## Elementos de la interfaz

1. **Botón "Seleccionar Carpeta"**: Abre un diálogo para seleccionar la carpeta raíz.
2. **Panel de búsqueda**: 
   - Cuadro de texto para ingresar términos de búsqueda.
   - Botón "Buscar" para iniciar la búsqueda.
3. **TreeView**: Muestra la estructura de carpetas y archivos.
4. **Panel de detalles**: Muestra información del elemento seleccionado.
5. **Barra de estado**: Muestra mensajes sobre la carpeta cargada y resultados de búsqueda.

## Consideraciones y limitaciones

- El rendimiento puede verse afectado en carpetas con un gran número de archivos y subcarpetas.
- La búsqueda se realiza sobre los elementos ya cargados en el TreeView.
- El script requiere permisos de lectura en las carpetas que se intentan explorar.

## Solución de problemas

- Si el script no se ejecuta, asegúrese de que la política de ejecución de PowerShell permite la ejecución de scripts.
- Si no se muestran algunas carpetas o archivos, verifique que tiene los permisos necesarios para acceder a ellos.

## Soporte

Para preguntas o problemas relacionados con este script, contacte al autor, Sicer Andres Brito Gutierrez, o al administrador del sistema responsable de los scripts de PowerShell en su organización.

---

*Nota: Utilice este script con responsabilidad y asegúrese de tener los permisos necesarios para explorar las carpetas del sistema.*
