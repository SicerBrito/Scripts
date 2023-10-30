# Obtener la ruta de la carpeta que deseas listar
$carpeta = "C:\Ruta\A\Tu\Carpeta"

# Obtener la lista de archivos en la carpeta
$archivos = Get-ChildItem $carpeta

# Recorrer la lista de archivos y mostrar sus nombres
foreach ($archivo in $archivos) {
    Write-Host "Nombre del archivo: $($archivo.Name)"
}
