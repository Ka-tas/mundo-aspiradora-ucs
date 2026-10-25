"""
UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO
INGENIERIA INFORMATICA Y DE SISTEMAS - INTELIGENCIA ARTIFICIAL

Problema: EL MUNDO DE LA ASPIRADORA (dos ambientes, A y B)
Estrategia: BUSQUEDA DE COSTO UNIFORME (UCS - Uniform Cost Search)

Punto de entrada compatible con la versión original de laboratorio.
Uso:
    python aspiradora_ucs.py                      -> abre la interfaz grafica
    python aspiradora_ucs.py --sin-gui            -> imprime el paso a paso en consola
    python aspiradora_ucs.py --sin-gui --inicial B-SS --costes 1 1 2
        (costes en el orden: Izquierda Derecha Aspirar)
"""
import sys
from pathlib import Path

# Añadir 'src' a sys.path
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from aspiradora.cli import main

if __name__ == '__main__':
    main()
