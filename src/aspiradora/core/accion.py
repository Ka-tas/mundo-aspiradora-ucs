"""
Representación de una acción dentro del espacio de estados.
"""


class Accion:
    def __init__(self, nombre: str):
        self.nombre = nombre

    def __str__(self) -> str:
        return self.nombre

    def __repr__(self) -> str:
        return f"Accion({self.nombre!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Accion):
            return self.nombre == other.nombre
        return False

    def __hash__(self) -> int:
        return hash(self.nombre)
