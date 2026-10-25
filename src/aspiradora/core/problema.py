"""
Definición formal de un problema de búsqueda en espacio de estados.
"""
from typing import Dict, List, Optional, Any


class Problema:
    def __init__(
        self,
        estado_inicial: Any,
        estados_objetivos: List[Any],
        acciones: Dict[str, Dict[str, Any]],
        costes: Optional[Dict[str, Dict[str, int]]] = None
    ):
        self.estado_inicial = estado_inicial
        self.estados_objetivos = estados_objetivos
        self.acciones = acciones
        self.costes = costes
        self.infinito = 99999
        if not self.costes:
            self.costes = {k: {k1: 1 for k1 in v} for k, v in self.acciones.items()}

    def __str__(self) -> str:
        return f"Estado Inicial: {self.estado_inicial.nombre} -> Objetivos: {[str(e) for e in self.estados_objetivos]}"

    def es_objetivo(self, estado: Any) -> bool:
        return estado in self.estados_objetivos

    def resultado(self, estado: Any, accion: Any) -> Optional[Any]:
        if estado.nombre not in self.acciones:
            return None
        acciones_estado = self.acciones[estado.nombre]
        if accion.nombre not in acciones_estado:
            return None
        return acciones_estado[accion.nombre]

    def coste_accion(self, estado: Any, accion: Any) -> int:
        if estado.nombre not in self.costes:
            return self.infinito
        costes_estado = self.costes[estado.nombre]
        if accion.nombre not in costes_estado:
            return self.infinito
        return costes_estado[accion.nombre]

    def coste_camino(self, nodo: Any) -> int:
        total = 0
        while nodo.padre:
            total += self.coste_accion(nodo.padre.estado, nodo.accion)
            nodo = nodo.padre
        return total
