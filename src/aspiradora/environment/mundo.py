"""
Modelado del entorno 'Mundo de la Aspiradora' de dos habitaciones (A y B).
"""
from typing import Dict, List, Optional, Tuple, Any
from aspiradora.core.accion import Accion
from aspiradora.core.estado import Estado
from aspiradora.core.agente import AgenteBusqueda
from aspiradora.core.nodo import Nodo


class MundoAspiradora:
    """
    Representa el problema clásico de la aspiradora de 2 habitaciones (A y B).
    Espacio de estados: 2 posiciones x 2^2 estados de suciedad = 8 estados posibles.
    Acciones:
      - 'I': Izquierda
      - 'D': Derecha
      - 'A': Aspirar
    """
    def __init__(self):
        self.nombre = 'Mundo de la aspiradora'
        accI, accD, accA = Accion('I'), Accion('D'), Accion('A')

        # 2 x 2^2 = 8 estados posibles
        self.estados: List[Estado] = []
        por_nombre: Dict[str, Estado] = {}

        def nombre_de(pos: str, sa: bool, sb: bool) -> str:
            return f"{pos}-{'S' if sa else 'L'}{'S' if sb else 'L'}"

        for pos in ('A', 'B'):
            for sa in (True, False):
                for sb in (True, False):
                    nom = nombre_de(pos, sa, sb)
                    e = Estado(nom, [accI, accD, accA], pos, sa, sb)
                    self.estados.append(e)
                    por_nombre[nom] = e

        # Función sucesor: Izquierda, Derecha y Aspirar desde cada estado
        self.viajes: Dict[str, Dict[str, Estado]] = {}
        for e in self.estados:
            aspirado_a = False if e.posicion == 'A' else e.sucio_a
            aspirado_b = False if e.posicion == 'B' else e.sucio_b
            self.viajes[e.nombre] = {
                'I': por_nombre[nombre_de('A', bool(e.sucio_a), bool(e.sucio_b))],
                'D': por_nombre[nombre_de('B', bool(e.sucio_a), bool(e.sucio_b))],
                'A': por_nombre[nombre_de(e.posicion, aspirado_a, aspirado_b)],
            }

        self.por_nombre = por_nombre
        # Test objetivo: ambas habitaciones limpias (A-LL o B-LL)
        self.objetivos = [e for e in self.estados if not e.sucio_a and not e.sucio_b]

    def __str__(self) -> str:
        return self.nombre

    def resolver(
        self,
        nombre_inicial: str,
        costes_accion: Optional[Dict[str, int]] = None
    ) -> Tuple[AgenteBusqueda, Optional[Nodo], List[Dict[str, Any]]]:
        """
        costes_accion: {'I': c1, 'D': c2, 'A': c3}; por defecto todos 1.
        """
        costes_accion = costes_accion or {'I': 1, 'D': 1, 'A': 1}
        costes = {
            nom: {acc: costes_accion[acc] for acc in accs}
            for nom, accs in self.viajes.items()
        }
        if nombre_inicial not in self.por_nombre:
            raise ValueError(f"Estado inicial inválido: '{nombre_inicial}'. Válidos: {list(self.por_nombre.keys())}")

        estado_inicial = self.por_nombre[nombre_inicial]
        agente = AgenteBusqueda(estado_inicial, self.objetivos, self.viajes, costes)
        solucion, pasos = agente.costo_uniforme()
        return agente, solucion, pasos
