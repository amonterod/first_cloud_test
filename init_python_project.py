#!/usr/bin/env python3
"""
Script multiplataforma para crear proyectos Python con entorno virtual.
Uso: python init_python_project.py [nombre_proyecto] [opciones]
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class Colors:
    """Colores ANSI para terminal."""
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color
    
    @staticmethod
    def disable():
        """Deshabilita colores (para Windows sin soporte)."""
        Colors.GREEN = Colors.BLUE = Colors.YELLOW = Colors.RED = Colors.NC = ''


class PythonProjectInitializer:
    """Inicializador de proyectos Python con mejores practicas."""
    
    def __init__(self, project_name: str, add_docker: bool = False, 
                 add_ci: bool = False, framework: str = None):
        self.project_name = project_name
        self.project_path = Path.cwd() / project_name
        self.add_docker = add_docker
        self.add_ci = add_ci
        self.framework = framework
        self.is_windows = sys.platform.startswith('win')
        
        if self.is_windows and not os.environ.get('ANSICON'):
            Colors.disable()
    
    def print_step(self, step: int, total: int, message: str):
        """Imprime mensaje de progreso."""
        print(f"{Colors.GREEN}[{step}/{total}]{Colors.NC} {message}")
    
    def run_command(self, cmd: List[str], cwd: Path = None) -> Tuple[int, str]:
        """Ejecuta un comando y retorna codigo de salida y output."""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.project_path,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode, result.stdout + result.stderr
        except Exception as e:
            return 1, str(e)
    
    def create_directory_structure(self):
        """Crea la estructura de directorios del proyecto."""
        self.print_step(1, 8, "Creando estructura de directorios...")
        
        directories = [
            'src',
            'tests',
            'docs',
            'data',
            'scripts',
        ]
        
        self.project_path.mkdir(exist_ok=True)
        for directory in directories:
            (self.project_path / directory).mkdir(exist_ok=True)
    
    def create_virtual_environment(self):
        """Crea el entorno virtual."""
        self.print_step(2, 8, "Creando entorno virtual...")
        
        venv_path = self.project_path / '.venv'
        cmd = [sys.executable, '-m', 'venv', str(venv_path)]
        returncode, output = self.run_command(cmd, cwd=Path.cwd())
        
        if returncode != 0:
            print(f"{Colors.RED}Error creando entorno virtual:{Colors.NC} {output}")
            sys.exit(1)
    
    def get_venv_python(self) -> str:
        """Retorna la ruta al ejecutable de Python en el venv."""
        if self.is_windows:
            return str(self.project_path / '.venv' / 'Scripts' / 'python.exe')
        return str(self.project_path / '.venv' / 'bin' / 'python')
    
    def get_venv_pip(self) -> str:
        """Retorna la ruta al ejecutable de pip en el venv."""
        if self.is_windows:
            return str(self.project_path / '.venv' / 'Scripts' / 'pip.exe')
        return str(self.project_path / '.venv' / 'bin' / 'pip')
    
    def upgrade_pip(self):
        """Actualiza pip en el entorno virtual."""
        self.print_step(3, 8, "Actualizando pip...")
        
        python_exe = self.get_venv_python()
        cmd = [python_exe, '-m', 'pip', 'install', '--upgrade', 'pip', '--quiet']
        self.run_command(cmd)
    
    def create_requirements_files(self):
        """Crea archivos de requirements."""
        self.print_step(4, 8, "Creando archivos de dependencias...")
        
        # requirements.txt base
        base_requirements = "# Dependencias de produccion\n"
        
        if self.framework == 'fastapi':
            base_requirements += """fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
"""
        elif self.framework == 'flask':
            base_requirements += """Flask>=3.0.0
python-dotenv>=1.0.0
"""
        elif self.framework == 'django':
            base_requirements += """Django>=4.2.0
djangorestframework>=3.14.0
"""
        
        (self.project_path / 'requirements.txt').write_text(base_requirements)
        
        # requirements-dev.txt
        dev_requirements = """# Dependencias de desarrollo
-r requirements.txt

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.12.0

# Linting y formateo
black>=23.7.0
flake8>=6.1.0
isort>=5.12.0
pylint>=3.0.0

# Type checking
mypy>=1.5.0

# Debugging
ipdb>=0.13.13
"""
        (self.project_path / 'requirements-dev.txt').write_text(dev_requirements)
    
    def create_config_files(self):
        """Crea archivos de configuracion."""
        self.print_step(5, 8, "Creando archivos de configuracion...")
        
        # .gitignore
        gitignore = """# Entorno virtual
.venv/
venv/
ENV/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.project
.pydevproject

# Environment variables
.env
.env.local

# Datos y logs
data/
*.log
*.db
*.sqlite3

# OS
.DS_Store
Thumbs.db
Desktop.ini

# MyPy
.mypy_cache/
.dmypy.json
dmypy.json
"""
        (self.project_path / '.gitignore').write_text(gitignore)
        
        # .editorconfig
        editorconfig = """root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.py]
indent_style = space
indent_size = 4
max_line_length = 88

[*.{yml,yaml,json}]
indent_style = space
indent_size = 2

[Makefile]
indent_style = tab
"""
        (self.project_path / '.editorconfig').write_text(editorconfig)
        
        # pyproject.toml
        pyproject = f"""[tool.black]
line-length = 88
target-version = ['py311']
include = '\\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-v --cov=src --cov-report=html --cov-report=term"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", ".venv/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]

[project]
name = "{self.project_name}"
version = "0.1.0"
description = "Proyecto Python"
requires-python = ">=3.9"
"""
        (self.project_path / 'pyproject.toml').write_text(pyproject)
    
    def create_vscode_config(self):
        """Crea configuracion de VSCode."""
        self.print_step(6, 8, "Creando configuracion de VSCode...")
        
        vscode_dir = self.project_path / '.vscode'
        vscode_dir.mkdir(exist_ok=True)
        
        python_path = "${workspaceFolder}/.venv/Scripts/python.exe" if self.is_windows else "${workspaceFolder}/.venv/bin/python"
        
        settings = f"""{{
    "python.defaultInterpreterPath": "{python_path}",
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true,
    
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests",
        "-v"
    ],
    
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--max-line-length=88",
        "--extend-ignore=E203,W503"
    ],
    "python.linting.pylintEnabled": false,
    
    "python.formatting.provider": "black",
    "[python]": {{
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {{
            "source.organizeImports": true
        }},
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.rulers": [88]
    }},
    
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    
    "files.exclude": {{
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true
    }},
    
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {{
        "source.organizeImports": true
    }}
}}
"""
        (vscode_dir / 'settings.json').write_text(settings)
        
        launch = """{{
    "version": "0.2.0",
    "configurations": [
        {{
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${{file}}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {{
                "PYTHONPATH": "${{workspaceFolder}}/src"
            }}
        }},
        {{
            "name": "Python: Debug Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "tests/",
                "-v",
                "-s"
            ],
            "console": "integratedTerminal",
            "justMyCode": false
        }}
    ]
}}
"""
        (vscode_dir / 'launch.json').write_text(launch)
        
        extensions = """{{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "ms-python.isort",
        "ms-python.flake8",
        "editorconfig.editorconfig",
        "streetsidesoftware.code-spell-checker"
    ]
}}
"""
        (vscode_dir / 'extensions.json').write_text(extensions)
    
    def create_source_files(self):
        """Crea archivos de codigo fuente de ejemplo."""
        self.print_step(7, 8, "Creando archivos de codigo de ejemplo...")
        
        # src/__init__.py
        (self.project_path / 'src' / '__init__.py').write_text(
            '"""Paquete principal del proyecto."""\n__version__ = "0.1.0"\n'
        )
        
        # src/main.py
        if self.framework == 'fastapi':
            main_content = '''"""Aplicacion FastAPI."""
from fastapi import FastAPI

app = FastAPI(title="Mi API", version="0.1.0")


@app.get("/")
async def read_root():
    """Endpoint raiz."""
    return {"message": "¡Hola, FastAPI!"}


@app.get("/health")
async def health_check():
    """Health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        elif self.framework == 'flask':
            main_content = '''"""Aplicacion Flask."""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    """Ruta principal."""
    return jsonify({"message": "¡Hola, Flask!"})


@app.route('/health')
def health():
    """Health check."""
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
        else:
            main_content = '''"""Modulo principal de la aplicacion."""


def saludar(nombre: str) -> str:
    """
    Retorna un saludo personalizado.
    
    Args:
        nombre: Nombre de la persona a saludar
        
    Returns:
        Mensaje de saludo
        
    Examples:
        >>> saludar("Python")
        '¡Hola, Python!'
    """
    if not nombre:
        raise ValueError("El nombre no puede estar vacio")
    return f"¡Hola, {nombre}!"


def main() -> None:
    """Funcion principal."""
    print(saludar("Mundo"))


if __name__ == "__main__":
    main()
'''
        
        (self.project_path / 'src' / 'main.py').write_text(main_content)
        
        # tests/__init__.py
        (self.project_path / 'tests' / '__init__.py').write_text(
            '"""Tests del proyecto."""\n'
        )
        
        # tests/test_main.py
        test_content = '''"""Tests para el modulo main."""
import sys
from pathlib import Path

# Añadir src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from main import saludar


def test_saludar_basico():
    """Test basico de la funcion saludar."""
    resultado = saludar("Python")
    assert resultado == "¡Hola, Python!"
    assert isinstance(resultado, str)


def test_saludar_vacio():
    """Test con nombre vacio."""
    with pytest.raises(ValueError, match="no puede estar vacio"):
        saludar("")


def test_saludar_diferentes_nombres():
    """Test con diferentes nombres."""
    nombres = ["Alice", "Bob", "Charlie"]
    for nombre in nombres:
        resultado = saludar(nombre)
        assert nombre in resultado
'''
        (self.project_path / 'tests' / 'test_main.py').write_text(test_content)
        
        # README.md
        activate_cmd_linux = "source .venv/bin/activate"
        activate_cmd_windows = ".venv\\\\Scripts\\\\activate"
        
        readme = f"""# {self.project_name}

## Descripcion
Proyecto Python con entorno virtual aislado y mejores practicas de desarrollo.

## Requisitos
- Python 3.9+
- pip

## Configuracion del entorno

### 1. Clonar el repositorio (si aplica)
```bash
git clone <url>
cd {self.project_name}
```

### 2. Crear y activar entorno virtual

**Linux/Mac:**
```bash
python3 -m venv .venv
{activate_cmd_linux}
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
{activate_cmd_windows}
```

### 3. Instalar dependencias

```bash
pip install -r requirements-dev.txt
```

## Estructura del proyecto

```
{self.project_name}/
├── src/                    # Codigo fuente
│   ├── __init__.py
│   └── main.py
├── tests/                  # Tests unitarios
│   ├── __init__.py
│   └── test_main.py
├── docs/                   # Documentacion
├── data/                   # Datos (ignorado en git)
├── scripts/                # Scripts auxiliares
├── .venv/                  # Entorno virtual
├── .vscode/                # Configuracion VSCode
├── requirements.txt        # Dependencias produccion
├── requirements-dev.txt    # Dependencias desarrollo
├── pyproject.toml          # Configuracion del proyecto
├── .gitignore
├── .editorconfig
└── README.md
```

## Desarrollo

### Ejecutar la aplicacion
```bash
python src/main.py
```

### Ejecutar tests
```bash
pytest tests/
```

### Ejecutar tests con cobertura
```bash
pytest tests/ --cov=src --cov-report=html
```

### Formatear codigo
```bash
black src/ tests/
isort src/ tests/
```

### Linting
```bash
flake8 src/ tests/
```

### Type checking
```bash
mypy src/
```

## VSCode

Este proyecto esta configurado para VSCode con:
- Deteccion automatica del entorno virtual
- Formateo automatico al guardar (Black)
- Organizacion automatica de imports (isort)
- Configuracion de debugging
- Extensiones recomendadas

Simplemente abre el proyecto con `code .` y VSCode detectara todo automaticamente.

## Comandos utiles

```bash
# Actualizar dependencias
pip freeze > requirements.txt

# Agregar nueva dependencia
pip install <paquete>
echo "<paquete>>=<version>" >> requirements.txt

# Limpiar archivos compilados
find . -type d -name __pycache__ -exec rm -rf {{}} +
find . -type f -name "*.pyc" -delete

# Ejecutar todos los checks
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/ && pytest
```

## Contribuir

1. Crear una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
2. Commit tus cambios: `git commit -am 'Agrega nueva funcionalidad'`
3. Push a la rama: `git push origin feature/nueva-funcionalidad`
4. Crear un Pull Request

## Licencia

MIT
"""
        (self.project_path / 'README.md').write_text(readme)
    
    def create_additional_files(self):
        """Crea archivos adicionales segun opciones."""
        self.print_step(8, 8, "Creando archivos adicionales...")
        
        # Makefile
        makefile = """# Makefile para tareas comunes

.PHONY: help install test lint format clean run

help:
\t@echo "Comandos disponibles:"
\t@echo "  install    - Instalar dependencias"
\t@echo "  test       - Ejecutar tests"
\t@echo "  lint       - Ejecutar linters"
\t@echo "  format     - Formatear codigo"
\t@echo "  clean      - Limpiar archivos temporales"
\t@echo "  run        - Ejecutar aplicacion"

install:
\tpip install -r requirements-dev.txt

test:
\tpytest tests/ -v --cov=src --cov-report=html

lint:
\tflake8 src/ tests/
\tmypy src/

format:
\tblack src/ tests/
\tisort src/ tests/

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {} +
\tfind . -type f -name "*.pyc" -delete
\trm -rf .pytest_cache .mypy_cache htmlcov .coverage

run:
\tpython src/main.py
"""
        (self.project_path / 'Makefile').write_text(makefile)
        
        # Script de activacion
        if self.is_windows:
            activate_script = """@echo off
REM Script de activacion rapida del entorno
call .venv\\Scripts\\activate.bat
echo Entorno virtual activado
python --version
"""
            (self.project_path / 'activate.bat').write_text(activate_script)
        else:
            activate_script = """#!/bin/bash
# Script de activacion rapida del entorno
source .venv/bin/activate
echo "✓ Entorno virtual activado"
echo "Python: $(which python)"
echo "Version: $(python --version)"
"""
            activate_file = self.project_path / 'activate.sh'
            activate_file.write_text(activate_script)
            activate_file.chmod(0o755)
        
        if self.add_docker:
            self._create_docker_files()
        
        if self.add_ci:
            self._create_ci_files()
    
    def _create_docker_files(self):
        """Crea archivos de Docker."""
        dockerfile = f"""FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo fuente
COPY src/ ./src/

# Crear usuario no-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "src/main.py"]
"""
        (self.project_path / 'Dockerfile').write_text(dockerfile)
        
        dockerignore = """# Python
__pycache__/
*.py[cod]
.venv/
*.egg-info/

# Tests
tests/
.pytest_cache/
.coverage

# Git
.git/
.gitignore

# IDE
.vscode/
.idea/

# Docs
docs/

# Data
data/
"""
        (self.project_path / '.dockerignore').write_text(dockerignore)
        
        docker_compose = f"""version: '3.8'

services:
  app:
    build: .
    container_name: {self.project_name}
    volumes:
      - ./src:/app/src
    environment:
      - PYTHONUNBUFFERED=1
    ports:
      - "8000:8000"
"""
        (self.project_path / 'docker-compose.yml').write_text(docker_compose)
    
    def _create_ci_files(self):
        """Crea archivos de CI/CD."""
        github_dir = self.project_path / '.github' / 'workflows'
        github_dir.mkdir(parents=True, exist_ok=True)
        
        ci_yaml = """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    
    - name: Lint with flake8
      run: |
        flake8 src/ tests/
    
    - name: Type check with mypy
      run: |
        mypy src/
    
    - name: Test with pytest
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
"""
        (github_dir / 'ci.yml').write_text(ci_yaml)
    
    def install_dependencies(self, install: bool = True):
        """Instala las dependencias del proyecto."""
        if not install:
            return
        
        print(f"\n{Colors.YELLOW}¿Deseas instalar las dependencias de desarrollo ahora? (s/n){Colors.NC}")
        respuesta = input().strip().lower()
        
        if respuesta in ['s', 'y', 'yes', 'si', 'si']:
            print(f"{Colors.GREEN}Instalando dependencias...{Colors.NC}")
            pip_exe = self.get_venv_pip()
            cmd = [pip_exe, 'install', '--trusted-host', 'pypi.org', '--trusted-host', 'files.pythonhosted.org', '-r', 'requirements-dev.txt']
            returncode, output = self.run_command(cmd)
            
            if returncode == 0:
                print(f"{Colors.GREEN}✓ Dependencias instaladas correctamente{Colors.NC}")
            else:
                print(f"{Colors.RED}Error instalando dependencias:{Colors.NC} {output}")
    
    def print_summary(self):
        """Imprime resumen final."""
        print(f"\n{Colors.GREEN}{'='*60}{Colors.NC}")
        print(f"{Colors.GREEN}✓ Proyecto '{self.project_name}' creado exitosamente{Colors.NC}")
        print(f"{Colors.GREEN}{'='*60}{Colors.NC}\n")
        
        print("Pasos siguientes:")
        print(f"  1. {Colors.BLUE}cd {self.project_name}{Colors.NC}")
        print(f"  2. {Colors.BLUE}code .{Colors.NC} (para abrir en VSCode)")
        print("  3. VSCode detectara automaticamente el entorno .venv")
        
        if self.is_windows:
            print(f"  4. O activa manualmente: {Colors.BLUE}.venv\\Scripts\\activate{Colors.NC}\n")
        else:
            print(f"  4. O activa manualmente: {Colors.BLUE}source .venv/bin/activate{Colors.NC}\n")
        
        print("Comandos utiles:")
        print(f"  • {Colors.BLUE}pytest tests/{Colors.NC} - Ejecutar tests")
        print(f"  • {Colors.BLUE}black src/{Colors.NC} - Formatear codigo")
        print(f"  • {Colors.BLUE}flake8 src/{Colors.NC} - Linting")
        print(f"  • {Colors.BLUE}make help{Colors.NC} - Ver todos los comandos disponibles\n")
        
        if self.add_docker:
            print("Docker habilitado:")
            print(f"  • {Colors.BLUE}docker-compose up{Colors.NC} - Ejecutar en contenedor\n")
    
    def initialize(self, install_deps: bool = True):
        """Ejecuta todo el proceso de inicializacion."""
        try:
            print(f"\n{Colors.BLUE}=== Inicializando proyecto Python: {self.project_name} ==={Colors.NC}\n")
            
            self.create_directory_structure()
            self.create_virtual_environment()
            self.upgrade_pip()
            self.create_requirements_files()
            self.create_config_files()
            self.create_vscode_config()
            self.create_source_files()
            self.create_additional_files()
            
            if install_deps:
                self.install_dependencies(install=True)
            
            self.print_summary()
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Operacion cancelada por el usuario{Colors.NC}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.RED}Error durante la inicializacion:{Colors.NC} {e}")
            sys.exit(1)


def main():
    """Funcion principal."""
    parser = argparse.ArgumentParser(
        description='Inicializa un proyecto Python con mejores practicas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python init_python_project.py mi_proyecto
  python init_python_project.py mi_api --framework fastapi --docker
  python init_python_project.py mi_app --framework flask --ci --no-install
        """
    )
    
    parser.add_argument(
        'project_name',
        nargs='?',
        default='',
        help='Nombre del proyecto (default: vacio)'
    )
    parser.add_argument(
        '--framework',
        choices=['fastapi', 'flask', 'django'],
        help='Framework web a usar'
    )
    parser.add_argument(
        '--docker',
        action='store_true',
        help='Incluir archivos de Docker'
    )
    parser.add_argument(
        '--ci',
        action='store_true',
        help='Incluir configuracion de CI/CD (GitHub Actions)'
    )
    parser.add_argument(
        '--no-install',
        action='store_true',
        help='No instalar dependencias automaticamente'
    )
    
    args = parser.parse_args()
    
    initializer = PythonProjectInitializer(
        project_name=args.project_name,
        add_docker=args.docker,
        add_ci=args.ci,
        framework=args.framework
    )
    
    initializer.initialize(install_deps=not args.no_install)


if __name__ == '__main__':
    main()
