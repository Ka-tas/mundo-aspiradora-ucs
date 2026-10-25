"""
Pruebas unitarias para el motor de búsqueda central (core).
"""
import unittest
from aspiradora.core.accion import Accion
from aspiradora.core.estado import Estado
from aspiradora.core.problema import Problema
from aspiradora.core.nodo import Nodo
from aspiradora.core.agente import AgenteBusqueda


class TestCore(unittest.TestCase):
    def test_accion_igualdad_y_hash(self):
        a1 = Accion("I")
        a2 = Accion("I")
        a3 = Accion("D")
        self.assertEqual(a1, a2)
        self.assertNotEqual(a1, a3)
        self.assertEqual(hash(a1), hash(a2))

    def test_estado_igualdad_y_hash(self):
        e1 = Estado("A-SS", [])
        e2 = Estado("A-SS", [])
        e3 = Estado("B-LL", [])
        self.assertEqual(e1, e2)
        self.assertNotEqual(e1, e3)
        self.assertEqual(hash(e1), hash(e2))

    def test_nodo_ruta_y_costo(self):
        e1 = Estado("A", [])
        e2 = Estado("B", [])
        acc = Accion("D")

        n1 = Nodo(e1)
        n2 = Nodo(e2, accion=acc, padre=n1)
        n2.coste = 5

        self.assertEqual([e.nombre for e in n2.camino_estados()], ["A", "B"])
        self.assertEqual(n2.camino_acciones(), ["D"])
        self.assertEqual(n2.coste, 5)

    def test_problema_y_ucs_simple(self):
        # Grafo simple:
        # S --A(coste 5)--> G
        # S --B(coste 1)--> M --C(coste 2)--> G
        # UCS debe elegir S -> M -> G con costo total 3 en vez de camino directo S -> G con costo 5.
        s = Estado("S", [])
        m = Estado("M", [])
        g = Estado("G", [])

        acciones = {
            "S": {"A": g, "B": m},
            "M": {"C": g},
            "G": {},
        }
        costes = {
            "S": {"A": 5, "B": 1},
            "M": {"C": 2},
            "G": {},
        }

        agente = AgenteBusqueda(s, [g], acciones, costes)
        solucion, pasos = agente.costo_uniforme()

        self.assertIsNotNone(solucion)
        self.assertEqual(solucion.coste, 3)
        self.assertEqual([e.nombre for e in solucion.camino_estados()], ["S", "M", "G"])
        self.assertEqual(solucion.camino_acciones(), ["B", "C"])


if __name__ == '__main__':
    unittest.main()
