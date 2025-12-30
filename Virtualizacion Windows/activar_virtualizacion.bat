@echo off
echo ============================================
echo Activando Hyper-V, WSL2 y el hipervisor...
echo ============================================

dism.exe /Online /Enable-Feature:Microsoft-Hyper-V-All /All
dism.exe /Online /Enable-Feature:VirtualMachinePlatform /All
dism.exe /Online /Enable-Feature:Microsoft-Windows-Subsystem-Linux /All
dism.exe /Online /Enable-Feature:HypervisorPlatform /All

echo.
echo Habilitando hipervisor...
bcdedit /set hypervisorlaunchtype auto

echo.
echo Proceso completado. Reinicia el equipo para aplicar los cambios.
pause
