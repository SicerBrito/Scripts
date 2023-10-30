# Solicitar al usuario el nombre de la carpeta
$nombreCarpeta = Read-Host "Ingrese el nombre de la carpeta que desea listar"

# Construir la ruta completa de la carpeta
$carpeta = Join-Path $env:USERPROFILE $nombreCarpeta

# Comprobar si la carpeta existe
if (Test-Path $carpeta -PathType Container) {
    # Obtener la lista de archivos en la carpeta
    $archivos = Get-ChildItem $carpeta

    # Comprobar si la carpeta está vacía
    if ($archivos.Count -eq 0) {
        Write-Host "La carpeta está vacia."
    } else {
        Write-Host "Archivos en la carpeta:"
        # Recorrer la lista de archivos y mostrar detalles
        foreach ($archivo in $archivos) {
            $tamanoMB = [math]::Round(($archivo.Length / 1MB), 2)
            Write-Host "Nombre: $($archivo.Name)"
            Write-Host "Tamano: $tamanoMB MB"
            Write-Host "Ultima modificacion: $($archivo.LastWriteTime)"
            Write-Host "-----------------------"
        }
    }
} else {
    Write-Host "La carpeta especificada no existe."
}
