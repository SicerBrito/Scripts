# Solicitar al usuario la ruta de la carpeta
$carpeta = Read-Host "Ingrese la ruta de la carpeta que desea listar"

# Comprobar si la carpeta existe
if (Test-Path $carpeta -PathType Container) {
    # Obtener la lista de archivos en la carpeta
    $archivos = Get-ChildItem $carpeta

    # Comprobar si la carpeta está vacía
    if ($archivos.Count -eq 0) {
        Write-Host "La carpeta está vacía."
    } else {
        Write-Host "Archivos en la carpeta:"
        # Recorrer la lista de archivos y mostrar detalles
        foreach ($archivo in $archivos) {
            Write-Host "Nombre: $($archivo.Name)"
            Write-Host "Tamano: $($archivo.Length) bytes"
            Write-Host "Ultima modificacion: $($archivo.LastWriteTime)"
            Write-Host "-----------------------"
        }
    }
} else {
    Write-Host "La carpeta especificada no existe."
}
