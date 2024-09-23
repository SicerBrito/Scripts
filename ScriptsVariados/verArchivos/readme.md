# Documentación: Explorador de Carpetas con Búsqueda Mejorada

## Autor
Sicer Andrés Brito Gutiérrez

## Referencia
[Enlace al archivo del script](paste.txt)

## Descripción General
Este script de PowerShell crea una aplicación de interfaz gráfica de usuario (GUI) para explorar el sistema de archivos con funcionalidades de búsqueda mejoradas. La aplicación permite a los usuarios navegar por las carpetas, buscar archivos y carpetas, y ver detalles de los elementos seleccionados.

## Características Principales
1. Exploración de carpetas en una estructura de árbol
2. Búsqueda de archivos y carpetas
3. Visualización de detalles de archivos y carpetas
4. Carga dinámica de contenido de carpetas
5. Interfaz gráfica intuitiva

## Requisitos
- Windows PowerShell
- .NET Framework (incluido en Windows)

## Funciones Principales

### Get-FolderContent
Esta función recorre recursivamente una carpeta y agrega su contenido al TreeView.

Parámetros:
- `$FolderPath`: Ruta de la carpeta a explorar
- `$TreeView`: Objeto TreeView donde se mostrarán los resultados
- `$ParentNode`: Nodo padre en el TreeView (opcional)

### Search-TreeView
Realiza una búsqueda en el TreeView basada en un término de búsqueda.

Parámetros:
- `$TreeView`: Objeto TreeView donde se realizará la búsqueda
- `$SearchTerm`: Término de búsqueda

### Eventos Principales
- `BeforeExpand`: Carga el contenido de una carpeta cuando se expande en el TreeView
- `AfterSelect`: Muestra los detalles del elemento seleccionado
- `Click` (botón de búsqueda): Inicia la búsqueda
- `KeyPress` (caja de búsqueda): Permite iniciar la búsqueda al presionar Enter
- `Click` (botón de selección de carpeta): Abre un diálogo para seleccionar la carpeta raíz

## Interfaz de Usuario
- Panel de búsqueda con caja de texto y botón
- TreeView para mostrar la estructura de carpetas y archivos
- Panel de detalles para mostrar información del elemento seleccionado
- Barra de estado para mensajes informativos
- Botón para seleccionar la carpeta raíz

## Uso
1. Ejecute el script en PowerShell
2. Use el botón "Seleccionar Carpeta" para elegir la carpeta raíz
3. Navegue por la estructura de carpetas en el TreeView
4. Utilice la función de búsqueda para encontrar archivos o carpetas específicos
5. Seleccione un elemento para ver sus detalles en el panel inferior

## Soporte
Para soporte o consultas, contacte al autor:
Discord: SicerBrito#1610

## Nota de Responsabilidad
Este script se proporciona tal cual, sin garantías de ningún tipo. El autor no se hace responsable de cualquier daño o uso indebido que pueda resultar de la utilización de este script. Se insta a los usuarios a utilizarlo de manera responsable y ética.