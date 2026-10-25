"""
Línea de comandos e invocador de la aplicación.
"""
import argparse
from typing import Dict
from aspiradora.core.agente import NOMBRES_ACCION
from aspiradora.environment.mundo import MundoAspiradora

try:
    import tkinter as tk
    from aspiradora.gui.app import AppAspiradora
except Exception:
    tk = None
    AppAspiradora = None


def imprimir_consola(inicial: str, costes: Dict[str, int]) -> None:
    mundo = MundoAspiradora()
    agente, solucion, pasos = mundo.resolver(inicial, costes)
    print(f"Problema: {agente.problema}")
    print("Costos: " + ", ".join(f"{NOMBRES_ACCION[a]}={v}" for a, v in costes.items()))
    print()
    for p in pasos:
        print(p['texto'])
        print()
    print("=== Detalle de la solucion ===")
    agente.mostrar_solucion(solucion)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Mundo de la aspiradora con búsqueda de costo uniforme (UCS)"
    )
    parser.add_argument('--sin-gui', action='store_true', help="imprimir el paso a paso en consola")
    parser.add_argument('--inicial', default='A-SS', help="estado inicial, p. ej. A-SS, B-SL")
    parser.add_argument(
        '--costes',
        nargs=3,
        type=int,
        default=[1, 1, 1],
        metavar=('I', 'D', 'A'),
        help="costos de Izquierda, Derecha y Aspirar (por defecto: 1 1 1)"
    )
    args = parser.parse_args(argv)
    costes = dict(zip(('I', 'D', 'A'), args.costes))

    if args.sin_gui or tk is None or AppAspiradora is None:
        if tk is None and not args.sin_gui:
            print("tkinter no está disponible en este entorno; ejecutando modo consola.\n")
        imprimir_consola(args.inicial, costes)
    else:
        app = AppAspiradora()
        app.mainloop()


if __name__ == '__main__':
    main()
