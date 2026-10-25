"""
Interfaz gráfica interactiva para visualizar el espacio de estados y el algoritmo UCS.
"""
try:
    import tkinter as tk
    from tkinter import ttk
except Exception:  # Entorno sin soporte gráfico (headless / terminal)
    tk = None
    ttk = None

from aspiradora.core.agente import NOMBRES_ACCION
from aspiradora.environment.mundo import MundoAspiradora

# Disposición igual a la Figura 3.3 del espacio de estados (Russell & Norvig)
POSICIONES = {
    'A-SS': (330, 80),  'B-SS': (600, 80),
    'A-LS': (110, 270), 'B-LS': (350, 270), 'A-SL': (580, 270), 'B-SL': (820, 270),
    'A-LL': (330, 460), 'B-LL': (600, 460),
}
CAJA_W, CAJA_H = 150, 60

C_SOLUCION = '#ffd54f'
C_ACTUAL = '#ff9a3c'
C_EXPLORADO = '#b7e4b0'
C_FRONTERA = '#b3d4fc'
C_VACIO = '#ffffff'


class AppAspiradora(tk.Tk if tk else object):
    def __init__(self):
        if not tk:
            raise RuntimeError("tkinter no está disponible en este entorno.")
        super().__init__()
        self.title("Mundo de la aspiradora - Búsqueda de costo uniforme (UCS)")
        self.geometry("1380x760")
        self.mundo = MundoAspiradora()
        self.pasos, self.solucion, self.agente = [], None, None
        self.idx = 0
        self._after = None
        self._construir_controles()
        self._construir_cuerpo()
        self.resolver()

    # -- Construcción de la ventana -------------------------------------------
    def _construir_controles(self):
        barra = ttk.Frame(self, padding=6)
        barra.pack(fill='x')
        ttk.Label(barra, text="Estado inicial:").pack(side='left')
        self.var_inicial = tk.StringVar(value='A-SS')
        ttk.Combobox(
            barra,
            textvariable=self.var_inicial,
            state='readonly',
            width=7,
            values=[e.nombre for e in self.mundo.estados]
        ).pack(side='left', padx=(2, 12))

        self.var_costes = {}
        for acc in ('I', 'D', 'A'):
            ttk.Label(barra, text=f"Costo {NOMBRES_ACCION[acc]}:").pack(side='left')
            v = tk.IntVar(value=1)
            self.var_costes[acc] = v
            ttk.Spinbox(barra, from_=1, to=20, width=4, textvariable=v).pack(side='left', padx=(2, 10))

        ttk.Button(barra, text="Resolver / Reiniciar", command=self.resolver).pack(side='left', padx=4)
        ttk.Button(barra, text="<< Anterior", command=self.anterior).pack(side='left', padx=2)
        ttk.Button(barra, text="Siguiente >>", command=self.siguiente).pack(side='left', padx=2)
        ttk.Button(barra, text="Ir al final", command=self.al_final).pack(side='left', padx=2)
        self.btn_play = ttk.Button(barra, text="Reproducir", command=self.alternar_auto)
        self.btn_play.pack(side='left', padx=2)
        self.lbl_paso = ttk.Label(barra, text="", font=('Segoe UI', 10, 'bold'))
        self.lbl_paso.pack(side='right', padx=8)

        info = ttk.Label(
            self,
            padding=(8, 0),
            text=(
                "Formato de estado: [posición]-[A][B]  (S = sucio, L = limpio).  "
                "Acciones: I = Izquierda, D = Derecha, A = Aspirar.  "
                "Meta: A y B limpios.  Empate de costo: sale el primero insertado en la frontera."
            )
        )
        info.pack(fill='x')

    def _construir_cuerpo(self):
        cuerpo = ttk.Frame(self)
        cuerpo.pack(fill='both', expand=True, padx=6, pady=6)

        self.canvas = tk.Canvas(
            cuerpo,
            width=930,
            height=570,
            bg='white',
            highlightthickness=1,
            highlightbackground='#999'
        )
        self.canvas.pack(side='left', anchor='n')

        marco = ttk.Frame(cuerpo)
        marco.pack(side='left', fill='both', expand=True, padx=(8, 0))
        ttk.Label(
            marco,
            text="Paso a paso (búsqueda de costo uniforme)",
            font=('Segoe UI', 10, 'bold')
        ).pack(anchor='w')

        self.txt = tk.Text(marco, wrap='word', font=('Consolas', 10), width=60)
        sb = ttk.Scrollbar(marco, command=self.txt.yview)
        self.txt.configure(yscrollcommand=sb.set)
        sb.pack(side='right', fill='y')
        self.txt.pack(side='left', fill='both', expand=True)
        self.txt.tag_configure('ultimo', background='#fff2c4')
        self.txt.tag_configure('final', background='#d7f5d0', font=('Consolas', 10, 'bold'))

    # -- Lógica de control ----------------------------------------------------
    def resolver(self):
        self._detener_auto()
        costes = {acc: max(1, self._leer(v)) for acc, v in self.var_costes.items()}
        self.agente, self.solucion, self.pasos = self.mundo.resolver(self.var_inicial.get(), costes)
        self.idx = 0
        self.render()

    @staticmethod
    def _leer(var):
        try:
            return int(var.get())
        except Exception:
            return 1

    def siguiente(self):
        if self.idx < len(self.pasos) - 1:
            self.idx += 1
            self.render()
        else:
            self._detener_auto()

    def anterior(self):
        self._detener_auto()
        if self.idx > 0:
            self.idx -= 1
            self.render()

    def al_final(self):
        self._detener_auto()
        self.idx = len(self.pasos) - 1
        self.render()

    def alternar_auto(self):
        if self._after:
            self._detener_auto()
        else:
            if self.idx >= len(self.pasos) - 1:
                self.idx = 0
                self.render()
            self.btn_play.configure(text="Pausar")
            self._tick()

    def _tick(self):
        if self.idx < len(self.pasos) - 1:
            self.idx += 1
            self.render()
            self._after = self.after(1300, self._tick)
        else:
            self._detener_auto()

    def _detener_auto(self):
        if self._after:
            self.after_cancel(self._after)
            self._after = None
        self.btn_play.configure(text="Reproducir")

    # -- Dibujo ---------------------------------------------------------------
    def render(self):
        paso = self.pasos[self.idx]
        self.lbl_paso.configure(text=f"Paso {self.idx + 1} de {len(self.pasos)}")

        # Bitácora de texto hasta el paso actual
        self.txt.configure(state='normal')
        self.txt.delete('1.0', 'end')
        for i, p in enumerate(self.pasos[:self.idx + 1]):
            etiqueta = None
            if i == self.idx:
                etiqueta = 'final' if p['tipo'] == 'objetivo' else 'ultimo'
            self.txt.insert('end', p['texto'] + "\n\n", etiqueta)
        self.txt.see('end')
        self.txt.configure(state='disabled')

        self._dibujar_grafo(paso)

    def _dibujar_grafo(self, paso):
        c = self.canvas
        c.delete('all')
        final = paso['tipo'] == 'objetivo'

        sol_estados, sol_aristas = set(), set()
        if final:
            nodo = paso['nodo']
            while nodo:
                sol_estados.add(nodo.estado.nombre)
                if nodo.padre:
                    sol_aristas.add((nodo.padre.estado.nombre, nodo.accion.nombre, nodo.estado.nombre))
                nodo = nodo.padre

        explorados = {e.nombre: coste for e, coste in paso['explorados']}
        frontera = {}
        for n in paso['frontera']:
            frontera[n.estado.nombre] = min(frontera.get(n.estado.nombre, 10 ** 9), n.coste)
        actual = paso['nodo'].estado.nombre if paso['tipo'] != 'fracaso' else None

        # Aristas (se omiten los bucles I en A, D en B y Aspirar sobre limpio)
        for origen, accs in self.mundo.viajes.items():
            for acc, destino in accs.items():
                if destino.nombre == origen:
                    continue
                en_sol = (origen, acc, destino.nombre) in sol_aristas
                self._dibujar_arista(POSICIONES[origen], POSICIONES[destino.nombre], acc, en_sol)

        # Estados
        for e in self.mundo.estados:
            if e.nombre in sol_estados:
                color = C_SOLUCION
            elif e.nombre == actual:
                color = C_ACTUAL
            elif e.nombre in explorados:
                color = C_EXPLORADO
            elif e.nombre in frontera:
                color = C_FRONTERA
            else:
                color = C_VACIO
            etiqueta = None
            if e.nombre in explorados:
                etiqueta = f"g = {explorados[e.nombre]} (explorado)"
            elif e.nombre in frontera:
                etiqueta = f"g = {frontera[e.nombre]} (frontera)"
            es_inicio = e is self.pasos[0]['nodo'].estado
            self._dibujar_estado(e, *POSICIONES[e.nombre], color, es_inicio, etiqueta)

        self._dibujar_leyenda()

    def _dibujar_arista(self, p1, p2, acc, resaltada):
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        largo = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / largo, dy / largo

        def corte(ax, ay):
            tx = (CAJA_W / 2) / abs(ax) if abs(ax) > 1e-9 else 1e9
            ty = (CAJA_H / 2) / abs(ay) if abs(ay) > 1e-9 else 1e9
            return min(tx, ty) + 4

        t = corte(ux, uy)
        ox, oy = -uy * 8, ux * 8  # Separa las flechas de ida y vuelta
        x1, y1 = p1[0] + ux * t + ox, p1[1] + uy * t + oy
        x2, y2 = p2[0] - ux * t + ox, p2[1] - uy * t + oy
        color = '#d32f2f' if resaltada else '#444444'
        self.canvas.create_line(
            x1, y1, x2, y2,
            arrow='last', fill=color,
            width=4 if resaltada else 1.3,
            arrowshape=(10, 12, 5)
        )
        self.canvas.create_text(
            (x1 + x2) / 2 + ox * 1.6,
            (y1 + y2) / 2 + oy * 1.6,
            text=acc,
            fill=color,
            font=('Segoe UI', 11, 'bold')
        )

    def _dibujar_estado(self, e, cx, cy, color, es_inicio, etiqueta):
        c = self.canvas
        x0, y0 = cx - CAJA_W / 2, cy - CAJA_H / 2
        c.create_rectangle(
            x0, y0, x0 + CAJA_W, y0 + CAJA_H,
            fill=color,
            outline='#1565c0' if es_inicio else 'black',
            width=4 if es_inicio else 2
        )
        c.create_line(cx, y0, cx, y0 + CAJA_H)
        for i, (letra, sucio) in enumerate((('A', e.sucio_a), ('B', e.sucio_b))):
            cel_x = x0 + i * CAJA_W / 2
            c.create_text(cel_x + 5, y0 + 3, text=letra, anchor='nw', font=('Segoe UI', 8, 'bold'))
            if sucio:
                for dx, dy in ((12, 46), (26, 52), (42, 46), (22, 38), (56, 50)):
                    c.create_oval(
                        cel_x + dx - 3, y0 + dy - 3, cel_x + dx + 3, y0 + dy + 3,
                        fill='#a0522d', outline='#6b3410'
                    )
            if e.posicion == letra:
                c.create_rectangle(
                    cel_x + 30, y0 + 8, cel_x + 68, y0 + 30,
                    fill='#a0125e', outline='#5a0a35'
                )
                c.create_text(cel_x + 49, y0 + 19, text='V', fill='white', font=('Segoe UI', 10, 'bold'))
        c.create_text(cx, y0 + CAJA_H + 11, text=e.nombre, font=('Segoe UI', 10, 'bold'))
        if etiqueta:
            c.create_text(cx, y0 - 10, text=etiqueta, font=('Segoe UI', 8), fill='#333')

    def _dibujar_leyenda(self):
        c = self.canvas
        items = [
            (C_ACTUAL, "Nodo explorado ahora"),
            (C_EXPLORADO, "Explorados"),
            (C_FRONTERA, "En la frontera"),
            (C_SOLUCION, "Ruta óptima")
        ]
        x = 10
        for color, texto in items:
            c.create_rectangle(x, 548, x + 16, 564, fill=color, outline='black')
            c.create_text(x + 22, 556, text=texto, anchor='w', font=('Segoe UI', 9))
            x += 24 + 8 * len(texto)
        c.create_text(
            10, 536,
            anchor='w',
            font=('Segoe UI', 8),
            fill='#555',
            text=(
                "V = aspiradora, puntos marrones = suciedad, contorno azul = estado inicial. "
                "g = costo acumulado. Los bucles no se dibujan (se descartan por explorados)."
            )
        )
