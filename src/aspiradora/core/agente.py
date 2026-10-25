"""
Agente de búsqueda que implementa Búsqueda de Costo Uniforme (UCS).
"""
import heapq
import itertools
from typing import Dict, List, Optional, Tuple, Any
from aspiradora.core.nodo import Nodo
from aspiradora.core.problema import Problema

NOMBRES_ACCION = {'I': 'Izquierda', 'D': 'Derecha', 'A': 'Aspirar'}


class AgenteBusqueda:
    def __init__(
        self,
        estado_inicial: Any,
        estados_objetivo: List[Any],
        acciones: Dict[str, Dict[str, Any]],
        costes: Optional[Dict[str, Dict[str, int]]] = None
    ):
        self.estado_inicial = estado_inicial
        self.estados_objetivo = estados_objetivo
        self.acciones = acciones
        self.costes = costes
        self.problema = Problema(estado_inicial, estados_objetivo, acciones, costes)

    def crear_nodo_raiz(self) -> Nodo:
        estado_raiz = self.problema.estado_inicial
        acciones_raiz = self.problema.acciones.get(estado_raiz.nombre, {})
        return Nodo(estado_raiz, None, acciones_raiz, None)

    # -- Utilidades de formato (estilo pizarrón) --------------------------------
    @staticmethod
    def ruta(nodo: Nodo) -> str:
        return '->'.join(str(e) for e in nodo.camino_estados())

    def _txt_nodo(self, nodo: Nodo) -> str:
        return f"({nodo.estado}, {nodo.coste}, {self.ruta(nodo)})"

    def _txt_frontera(self, frontera: list) -> str:
        items = sorted(frontera)  # (coste, orden_de_insercion, nodo)
        return "F[" + ", ".join(self._txt_nodo(n) for _, _, n in items) + "]"

    @staticmethod
    def _txt_explorados(explorados: list) -> str:
        return "{" + ", ".join(str(e) for e, _ in explorados) + "}"

    # -- Búsqueda de costo uniforme (UCS) --------------------------------------
    def costo_uniforme(self) -> Tuple[Optional[Nodo], List[Dict[str, Any]]]:
        """
        Ejecuta Búsqueda de Costo Uniforme (Dijkstra en espacio de estados).

        Devuelve:
            (nodo_solucion | None, pasos)
            'pasos' es una lista de diccionarios con el paso a paso, instantáneas
            de frontera y explorados para la bitácora y la GUI.
        """
        raiz = self.crear_nodo_raiz()
        orden = itertools.count()          # Desempate FIFO: primero insertado
        frontera = []                      # Cola de prioridad ascendente por costo acumulado
        heapq.heappush(frontera, (raiz.coste, next(orden), raiz))
        explorados = []                    # Lista (estado, costo) en orden
        set_explorados = set()
        pasos = []

        def snap_frontera():
            return [n for _, _, n in sorted(frontera)]

        pasos.append({
            'num': 1, 'tipo': 'inicio', 'nodo': raiz, 'hijos': [],
            'frontera': snap_frontera(), 'explorados': [],
            'texto': f"1) Inicio, {self._txt_frontera(frontera)}, explorados {{}}",
        })
        num = 1

        while frontera:
            num += 1
            _, _, nodo = heapq.heappop(frontera)

            # Nodo repetido: ya se exploró con un costo menor o igual
            if nodo.estado in set_explorados:
                pasos.append({
                    'num': num, 'tipo': 'repetido', 'nodo': nodo, 'hijos': [],
                    'frontera': snap_frontera(), 'explorados': list(explorados),
                    'texto': f"{num}) Explorar {self._txt_nodo(nodo)}. Ya fue explorado: no se toma en cuenta.\n   {self._txt_frontera(frontera)}",
                })
                continue

            # Prueba objetivo al momento de explorar (garantiza optimalidad)
            if self.problema.es_objetivo(nodo.estado):
                pasos.append({
                    'num': num, 'tipo': 'objetivo', 'nodo': nodo, 'hijos': [],
                    'frontera': snap_frontera(), 'explorados': list(explorados),
                    'texto': (f"{num}) Explorar {self._txt_nodo(nodo)}. ¿Es objetivo? Si => Finaliza.\n"
                              f"   La ruta optima encontrada por costo uniforme es:\n"
                              f"   {self.ruta(nodo)} con costo de {nodo.coste}\n"
                              f"   Acciones: {', '.join(nodo.camino_acciones()) or '(ninguna)'}"),
                })
                return nodo, pasos

            explorados.append((nodo.estado, nodo.coste))
            set_explorados.add(nodo.estado)

            lineas = [f"{num}) Explorar {self._txt_nodo(nodo)}. ¿Es objetivo? No, explorados {self._txt_explorados(explorados)}"]
            hijos_info = []
            hijos = nodo.expandir(self.problema)
            lineas.append(f"   Expandir {nodo.estado}. Sus hijos son {', '.join(str(h.estado) for h in hijos)}. Calcular costo acumulado:")

            for h in hijos:
                c = self.problema.coste_accion(nodo.estado, h.accion)
                if h.estado in set_explorados:
                    lineas.append(f"   - {nodo.estado} --{h.accion}--> {h.estado}: {h.estado} ya fue explorado, se descarta")
                    hijos_info.append((h, False))
                else:
                    lineas.append(f"   - {nodo.estado} --{h.accion}--> {h.estado}: costo acumulado {nodo.coste}+{c} = {h.coste}, {self.ruta(h)}")
                    heapq.heappush(frontera, (h.coste, next(orden), h))
                    hijos_info.append((h, True))

            lineas.append("   Agregar a la frontera ordenada por costo.")
            lineas.append("   " + self._txt_frontera(frontera))
            pasos.append({
                'num': num, 'tipo': 'explorar', 'nodo': nodo, 'hijos': hijos_info,
                'frontera': snap_frontera(), 'explorados': list(explorados),
                'texto': "\n".join(lineas),
            })

        pasos.append({
            'num': num + 1, 'tipo': 'fracaso', 'nodo': raiz, 'hijos': [],
            'frontera': [], 'explorados': list(explorados),
            'texto': f"{num + 1}) La frontera esta vacia: no existe solucion.",
        })
        return None, pasos

    def mostrar_solucion(self, objetivo: Optional[Nodo] = None):
        if not objetivo:
            print('No hay solucion')
            return
        self._mostrar_nodo_padre(objetivo)

    def _mostrar_nodo_padre(self, nodo: Nodo):
        if nodo.padre:
            self._mostrar_nodo_padre(nodo.padre)
            print()
            print('--------------------------------')
            print('Se partio del estado: ', nodo.padre.estado.nombre)
            print('Se realizo la accion: ', NOMBRES_ACCION.get(nodo.accion.nombre, nodo.accion.nombre))
            print('Se llego al estado:   ', nodo.estado.nombre)
