@echo off

:: Abrir el Bloc de notas y ubicarlo a la izquierda de la pantalla
start /D "C:\Windows\System32" /B /MAX notepad.exe
start /D "C:\Windows\System32" /B /MAX https://www.ejemplo.com

:: Esperar un momento para que las aplicaciones se abran
timeout /t 5

:: Colocar el Bloc de notas a la izquierda y el navegador a la derecha
%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -WindowStyle Hidden -Command "$Shell = New-Object -ComObject Shell.Application;$Shell.TileHorizontally()"

:: Esperar hasta que se cierre el Bloc de notas (opcional)
timeout /t 8
