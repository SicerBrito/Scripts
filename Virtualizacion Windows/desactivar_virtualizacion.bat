@echo off
echo ============================================
echo Desactivando Hyper-V, WSL2 y el hipervisor...
echo ============================================

dism.exe /Online /Disable-Feature:Microsoft-Hyper-V-All
dism.exe /Online /Disable-Feature:VirtualMachinePlatform
dism.exe /Online /Disable-Feature:Microsoft-Windows-Subsystem-Linux
dism.exe /Online /Disable-Feature:HypervisorPlatform

echo.
echo Deshabilitando hipervisor...
bcdedit /set hypervisorlaunchtype off

echo.
echo Proceso completado. Reinicia el equipo para aplicar los cambios.
pause
