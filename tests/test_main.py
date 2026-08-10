"""Tests para el modulo main."""
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
