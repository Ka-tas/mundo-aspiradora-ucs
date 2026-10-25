# 🧹 Mundo de la Aspiradora - Búsqueda de Costo Uniforme (UCS)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI Tests](https://github.com/usuario/mundo-aspiradora-ucs/actions/workflows/ci.yml/badge.svg)](.github/workflows/ci.yml)
[![UNSAAC](https://img.shields.io/badge/UNSAAC-IA-red.svg)](https://www.unsaac.edu.pe/)

Implementación modular y visual del clásico problema de Inteligencia Artificial **"El Mundo de la Aspiradora"** (Russell & Norvig, Cap. 3) utilizando el algoritmo de **Búsqueda de Costo Uniforme** (*Uniform Cost Search - UCS*).

Incluye una **interfaz gráfica interactiva (Tkinter)** para visualizar el grafo de 8 estados, la frontera de prioridad y los nodos explorados, así como un **modo consola (CLI)** con trazabilidad paso a paso y personalización de costos de acción.

---

## 🌟 Características

- **Algoritmo UCS Completo y Óptimo:** Implementación de búsqueda por costo acumulado $g(n)$ utilizando colas de prioridad (`heapq`) y desempate FIFO por orden de inserción.
- **Espacio de 8 Estados:** Representación formal de las 2 habitaciones ($A$ y $B$) y sus estados de suciedad ($S$ y $L$).
- **Interfaz Gráfica Interactiva (Tkinter):**
  - Renderizado del grafo del espacio de estados en tiempo real (disposición Fig. 3.3).
  - Colores distintivos para el nodo actual, nodos explorados, nodos en frontera y la ruta óptima encontrada.
  - Controles de reproducción: `Siguiente`, `Anterior`, `Ir al final` y reproducción automática paso a paso.
  - Modificación interactiva de estado inicial y de los costos por acción ($I$, $D$, $A$).
- **Modo Consola (CLI) Didáctico:** Desglose textual detallado del proceso de expansión, cálculo de costos acumulados, estados descartados por repetición y reconstrucción de la solución.
- **Sin Dependencias Externas:** Construido 100% sobre la Biblioteca Estándar de Python (`tkinter`, `heapq`, `itertools`, `argparse`, `unittest`).
- **Pruebas Unitarias Integradas:** Cobertura de pruebas para el motor de búsqueda y la lógica del mundo.

---

## 📁 Estructura del Repositorio

```text
aspirador/
├── .github/
│   └── workflows/
│       └── ci.yml             # Integración continua (GitHub Actions)
├── docs/
│   ├── images/                # Capturas de pantalla y diagramas
│   │   └── .gitkeep
│   └── TEORIA_Y_MODELO.md     # Documentación teórica, grafo y análisis formal
├── src/
│   └── aspiradora/            # Paquete principal
│       ├── __init__.py
│       ├── cli.py             # Entrada CLI y parser de argumentos
│       ├── core/              # Motor genérico de búsqueda en espacio de estados
│       │   ├── __init__.py
│       │   ├── accion.py      # Clase Accion
│       │   ├── estado.py      # Clase Estado
│       │   ├── nodo.py        # Clase Nodo y expansión de caminos
│       │   ├── problema.py    # Clase Problema y cálculo de costos
│       │   └── agente.py      # AgenteBusqueda y algoritmo UCS
│       ├── environment/       # Dominio del problema
│       │   ├── __init__.py
│       │   └── mundo.py       # Definición del MundoAspiradora (8 estados)
│       └── gui/               # Interfaz gráfica
│           ├── __init__.py
│           └── app.py         # Visualizador en Tkinter y animación del grafo
├── tests/                     # Suite de pruebas unitarias
│   ├── __init__.py
│   ├── test_core.py           # Pruebas del motor UCS
│   └── test_mundo.py          # Pruebas de transiciones y objetivos del mundo
├── .gitignore                 # Configuración de exclusión para Git
├── aspiradora_ucs.py          # Wrapper compatible con ejecución directa de laboratorio
├── LICENSE                    # Licencia MIT
├── main.py                    # Punto de entrada principal
├── pyproject.toml             # Configuración moderna de empaquetado (PEP 518/621)
├── requirements.txt           # Información de requisitos de ejecución
└── requirements-dev.txt       # Requisitos opcionales para desarrollo y linting
```

---

## 🚀 Requisitos e Instalación

### Requisitos Previos
- **Python 3.8 o superior** (incluye soporte para `tkinter`).

### Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/mundo-aspiradora-ucs.git
cd mundo-aspiradora-ucs
```

*(Opcional)* Si deseas herramientas de desarrollo como `pytest` o `flake8`:
```bash
pip install -r requirements-dev.txt
```

---

## 💻 Guía de Uso

### 1. Interfaz Gráfica (Modo por defecto)
Para abrir el simulador visual con controles interactivos:
```bash
python main.py
```
*(También compatible mediante `python aspiradora_ucs.py`)*

### 2. Modo Consola (CLI)
Si estás en un servidor sin entorno gráfico o prefieres analizar el paso a paso en texto:
```bash
python main.py --sin-gui
```

#### Cambiar el Estado Inicial:
```bash
python main.py --sin-gui --inicial B-SS
```

#### Personalizar Costos de Acción:
Los costos se pasan en el orden: `Izquierda` `Derecha` `Aspirar`. Por ejemplo, asignar costo 1 a moverse y costo 5 a aspirar:
```bash
python main.py --sin-gui --inicial A-SS --costes 1 1 5
```

---

## 🧪 Ejecución de Pruebas Unitarias

El proyecto cuenta con pruebas automáticas sin necesidad de librerías externas:

```bash
# Con el módulo unittest integrado de Python:
python -m unittest discover tests

# O si tienes pytest instalado:
pytest
```

---

## 📖 Nomenclatura de Estados

Los estados se codifican en el formato `[Posición]-[A][B]`:
- **Posición de la aspiradora:** `A` o `B`.
- **Habitación A:** `S` (Sucia) o `L` (Limpia).
- **Habitación B:** `S` (Sucia) o `L` (Limpia).

*Ejemplos:*
- `A-SS`: Aspiradora en la habitación A, ambas habitaciones sucias.
- `A-LS`: Aspiradora en A, habitación A limpia y habitación B sucia.
- `B-LL`: Aspiradora en B, ambas habitaciones limpias (**Estado Objetivo / Meta**).

Para más detalles matemáticos y teóricos, consulta el archivo [TEORIA_Y_MODELO.md](docs/TEORIA_Y_MODELO.md).

---

## 🏛️ Créditos Académicos

Proyecto desarrollado en el marco del curso de **Inteligencia Artificial**, Escuela Profesional de Ingeniería Informática y de Sistemas, **Universidad Nacional de San Antonio Abad del Cusco (UNSAAC)**.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.
