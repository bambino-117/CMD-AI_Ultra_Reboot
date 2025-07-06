@echo off
echo 🪟 CMD-AI Ultra Reboot - Compilation Windows
echo ==========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non trouvé ! Installez Python depuis python.org
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.

REM Installer les dépendances
echo 📦 Installation des dépendances...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erreur installation dépendances
    pause
    exit /b 1
)

echo 📦 Installation PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ❌ Erreur installation PyInstaller
    pause
    exit /b 1
)

echo ✅ Dépendances installées
echo.

REM Tester l'application
echo 🧪 Test de l'application...
python -c "import tkinter, PIL, requests, psutil, pygments; print('✅ Modules OK')"
if errorlevel 1 (
    echo ❌ Erreur modules Python
    pause
    exit /b 1
)

echo.

REM Compilation
echo 🔨 Compilation de l'exécutable...
pyinstaller --onefile --windowed --name CMD-AI_Ultra_Reboot --icon ressources/icons/CMD-AI_Ultra_main.ico --add-data "ressources;ressources" --add-data "extensions;extensions" main.py

if errorlevel 1 (
    echo ❌ Erreur de compilation
    pause
    exit /b 1
)

echo.

REM Vérification
if exist "dist\CMD-AI_Ultra_Reboot.exe" (
    echo ✅ Compilation réussie !
    echo 📍 Exécutable : dist\CMD-AI_Ultra_Reboot.exe
    
    REM Afficher la taille
    for %%I in (dist\CMD-AI_Ultra_Reboot.exe) do echo 📏 Taille : %%~zI octets
    
    echo.
    echo 🎉 Compilation terminée avec succès !
    echo.
    echo 🚀 Pour tester : dist\CMD-AI_Ultra_Reboot.exe
    echo 📦 Pour distribuer : Copiez le dossier dist\
    
) else (
    echo ❌ Exécutable non trouvé
    echo 🔍 Vérifiez les erreurs ci-dessus
)

echo.
pause