@echo off
setlocal

REM Obtener el nombre del directorio actual
for %%I in ("%cd%") do set dirname=%%~nI

echo "# %dirname%" >> README.md
git init
git add .
git commit -m "first commit"
git branch -M master
git remote add origin https://github.com/amonterod/%dirname%.git
git push -u origin master
