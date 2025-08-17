@echo off
echo Verification du System Monitor...

:: Tester si le serveur est deja en cours
curl -s http://127.0.0.1:5001/api/status >nul 2>&1
if %errorlevel% == 0 (
    echo System Monitor deja en cours d'execution sur le port 5001
    pause
    exit /b 0
)

echo Demarrage du System Monitor...
cd /d "%~dp0extensions\System_monitor"
start "System Monitor Server" cmd /k "python ancrage_sys_mon.py"

echo Attente du demarrage du serveur...
timeout /t 3 /nobreak >nul

:: Verifier que le serveur a demarre
curl -s http://127.0.0.1:5001/api/status >nul 2>&1
if %errorlevel% == 0 (
    echo System Monitor demarre avec succes!
) else (
    echo Echec du demarrage du System Monitor
)

pause