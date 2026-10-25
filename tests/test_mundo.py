"""
Pruebas unitarias para el entorno MundoAspiradora.
"""
import unittest
from aspiradora.environment.mundo import MundoAspiradora


class TestMundoAspiradora(unittest.TestCase):
    def setUp(self):
        self.mundo = MundoAspiradora()

    def test_estados_totales(self):
        # Deben existir exactamente 8 estados posibles
        self.assertEqual(len(self.mundo.estados), 8)

    def test_estados_objetivo(self):
        # Los objetivos son cuando ambas habitaciones están limpias
        nombres_obj = {e.nombre for e in self.mundo.objetivos}
        self.assertEqual(nombres_obj, {"A-LL", "B-LL"})

    def test_transiciones_aspirar(self):
        # Aspirar en A-SS debe llevar a A-LS
        dest_a = self.mundo.viajes["A-SS"]["A"]
        self.assertEqual(dest_a.nombre, "A-LS")

        # Aspirar en B-SS debe llevar a B-SL
        dest_b = self.mundo.viajes["B-SS"]["A"]
        self.assertEqual(dest_b.nombre, "B-SL")

        # Aspirar en A-LL no cambia suciedad
        dest_ll = self.mundo.viajes["A-LL"]["A"]
        self.assertEqual(dest_ll.nombre, "A-LL")

    def test_transiciones_movimiento(self):
        # En A-SS, ir a Izquierda permanece en A-SS
        self.assertEqual(self.mundo.viajes["A-SS"]["I"].nombre, "A-SS")
        # En A-SS, ir a Derecha va a B-SS
        self.assertEqual(self.mundo.viajes["A-SS"]["D"].nombre, "B-SS")

    def test_solucion_costos_uniformes(self):
        # Desde A-SS con costes 1 1 1:
        # A-SS --A--> A-LS --D--> B-LS --A--> B-LL (coste 3)
        agente, solucion, pasos = self.mundo.resolver("A-SS", {'I': 1, 'D': 1, 'A': 1})
        self.assertIsNotNone(solucion)
        self.assertEqual(solucion.coste, 3)
        self.assertEqual(solucion.camino_acciones(), ['A', 'D', 'A'])
        self.assertEqual(solucion.estado.nombre, "B-LL")

    def test_solucion_estado_inicial_es_meta(self):
        # Si parte de A-LL ya es meta (coste 0, 0 acciones)
        agente, solucion, pasos = self.mundo.resolver("A-LL")
        self.assertIsNotNone(solucion)
        self.assertEqual(solucion.coste, 0)
        self.assertEqual(solucion.camino_acciones(), [])


if __name__ == '__main__':
    unittest.main()
