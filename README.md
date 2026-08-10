# 

## Descripcion
Proyecto Python con entorno virtual aislado y mejores practicas de desarrollo.

## Requisitos
- Python 3.9+
- pip

## Configuracion del entorno

### 1. Clonar el repositorio (si aplica)
```bash
git clone <url>
cd 
```

### 2. Crear y activar entorno virtual

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\\Scripts\\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements-dev.txt
```

## Estructura del proyecto

```
/
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
find . -type d -name __pycache__ -exec rm -rf {} +
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
"# first_cloud_test" 
