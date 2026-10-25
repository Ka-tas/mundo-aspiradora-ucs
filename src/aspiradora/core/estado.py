"""
Representación de un estado en el espacio de búsqueda.
"""
from typing import List, Optional, Any


class Estado:
    def __init__(
        self,
        nombre: str,
        acciones: List[Any],
        posicion: Optional[str] = None,
        sucio_a: Optional[bool] = None,
        sucio_b: Optional[bool] = None
    ):
        self.nombre = nombre
        self.acciones = acciones
        # Datos propios del dominio de la aspiradora (usados para visualización)
        self.posicion = posicion
        self.sucio_a = sucio_a
        self.sucio_b = sucio_b

    def __str__(self) -> str:
        return self.nombre

    def __repr__(self) -> str:
        return f"Estado({self.nombre!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Estado):
            return self.nombre == other.nombre
        return False

    def __hash__(self) -> int:
        return hash(self.nombre)
