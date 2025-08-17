@echo off
echo Installation des dependances...
npm install

echo Compilation de l'application...
npm run dist

echo Compilation terminee! L'installateur se trouve dans le dossier dist/
pause