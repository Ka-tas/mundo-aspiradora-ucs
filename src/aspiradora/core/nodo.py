"""
Nodo de búsqueda en el árbol/grafo de exploración.
"""
from typing import List, Optional, Any
from aspiradora.core.accion import Accion


class Nodo:
    def __init__(
        self,
        estado: Any,
        accion: Optional[Accion] = None,
        acciones: Optional[Any] = None,
        padre: Optional['Nodo'] = None
    ):
        self.estado = estado
        self.accion = accion
        self.acciones = acciones
        self.padre = padre
        self.hijos: List['Nodo'] = []
        self.coste = 0  # Costo acumulado g(n) desde la raíz

    def __str__(self) -> str:
        return self.estado.nombre

    def __repr__(self) -> str:
        return f"Nodo({self.estado.nombre!r}, coste={self.coste})"

    def camino_estados(self) -> List[Any]:
        nodo, ruta = self, []
        while nodo:
            ruta.append(nodo.estado)
            nodo = nodo.padre
        return ruta[::-1]

    def camino_acciones(self) -> List[str]:
        nodo, acc = self, []
        while nodo.padre:
            acc.append(nodo.accion.nombre)
            nodo = nodo.padre
        return acc[::-1]

    def expandir(self, problema) -> List['Nodo']:
        """
        Devuelve la lista de nodos hijo; el costo es acumulado (padre + acción).
        """
        self.hijos = []
        if not self.acciones:
            if self.estado.nombre not in problema.acciones:
                return self.hijos
            self.acciones = problema.acciones[self.estado.nombre]

        for nombre_accion in self.acciones.keys():
            accion_hijo = Accion(nombre_accion)
            nuevo_estado = problema.resultado(self.estado, accion_hijo)
            acciones_nuevo = problema.acciones.get(nuevo_estado.nombre, {})
            hijo = Nodo(nuevo_estado, accion_hijo, acciones_nuevo, self)
            hijo.coste = self.coste + problema.coste_accion(self.estado, accion_hijo)
            self.hijos.append(hijo)
        return self.hijos
