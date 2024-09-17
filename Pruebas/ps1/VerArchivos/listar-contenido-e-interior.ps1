function ListarContenidoCarpeta {
    param (
        [string]$carpetaPadre,
        [string]$prefijo
    )
    
    # Obtener la lista de archivos y carpetas en la carpeta padre
    $elementos = Get-ChildItem $carpetaPadre

    foreach ($elemento in $elementos) {
        if ($elemento.PSIsContainer) {
            Write-Host "$prefijo Carpeta: $($elemento.Name)"

            # Mostrar el contenido de la carpeta
            $contenidoCarpeta = Get-ChildItem $elemento.FullName
            if ($contenidoCarpeta.Count -eq 0) {
                Write-Host "$prefijo   La carpeta está vacía."
            } else {
                Write-Host "$prefijo   Archivos en la carpeta:"
                foreach ($archivo in $contenidoCarpeta) {
                    $tamanoMB = [math]::Round(($archivo.Length / 1MB), 2)
                    Write-Host "$prefijo   Archivo: $($archivo.Name)"
                    Write-Host "$prefijo   Tamaño: $tamanoMB MB"
                    Write-Host "$prefijo   Última modificación: $($archivo.LastWriteTime)"
                    Write-Host "$prefijo   -----------------------"
                }
            }

            # Llamar recursivamente a la función para las carpetas anidadas
            ListarContenidoCarpeta -carpetaPadre $elemento.FullName -prefijo "$prefijo   "
        } else {
            $tamanoMB = [math]::Round(($elemento.Length / 1MB), 2)
            Write-Host "$prefijo Archivo: $($elemento.Name)"
            Write-Host "$prefijo Tamaño: $tamanoMB MB"
            Write-Host "$prefijo Última modificación: $($elemento.LastWriteTime)"
            Write-Host "$prefijo -----------------------"
        }
    }
}

# Solicitar al usuario el nombre de la carpeta raíz
$nombreCarpeta = Read-Host "Ingrese el nombre de la carpeta raíz que desea listar"

# Construir la ruta completa de la carpeta raíz
$carpetaRaiz = Join-Path $env:USERPROFILE $nombreCarpeta

# Comprobar si la carpeta raíz existe
if (Test-Path $carpetaRaiz -PathType Container) {
    Write-Host "Contenido de la carpeta raíz:"
    ListarContenidoCarpeta -carpetaPadre $carpetaRaiz -prefijo ""
} else {
    Write-Host "La carpeta raíz especificada no existe."
}
