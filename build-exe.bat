@echo off
echo Installation des dependances...
npm install

echo Compilation de l'executable portable...
npm run build-exe

echo Compilation terminee! L'executable se trouve dans le dossier dist/
pause