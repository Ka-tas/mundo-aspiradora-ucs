"""
Mundo de la Aspiradora - Búsqueda de Costo Uniforme (UCS).
"""

__version__ = "1.0.0"

from aspiradora.core.accion import Accion
from aspiradora.core.estado import Estado
from aspiradora.core.nodo import Nodo
from aspiradora.core.problema import Problema
from aspiradora.core.agente import AgenteBusqueda, NOMBRES_ACCION
from aspiradora.environment.mundo import MundoAspiradora

__all__ = [
    "__version__",
    "Accion",
    "Estado",
    "Nodo",
    "Problema",
    "AgenteBusqueda",
    "NOMBRES_ACCION",
    "MundoAspiradora",
]
