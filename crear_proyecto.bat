set PYTHONUTF8=1
python init_python_project.py %1
copy deactivate.bat %1
del .vscode\\launch.json
copy launch.json .vscode\\