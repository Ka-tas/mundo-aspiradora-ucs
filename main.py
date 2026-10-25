"""
Punto de entrada principal para el proyecto Mundo de la Aspiradora (UCS).
"""
import sys
from pathlib import Path

# Añadir 'src' a sys.path si no está presente
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from aspiradora.cli import main

if __name__ == '__main__':
    main()
