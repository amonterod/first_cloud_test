@echo off
REM Script de activacion rapida del entorno
call .venv\Scripts\deactivate.bat
echo Entorno virtual desactivado
python --version
where python