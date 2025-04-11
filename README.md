# Simuladores de Autómatas y Máquina de Turing

Este repositorio contiene simuladores interactivos desarrollados con Python y Tkinter, diseñados para representar visualmente el funcionamiento de distintos modelos de cómputo:

- 🧐 **Máquina de Turing**
- 🔀 **Autómata Finito No Determinista (AFND / NFA)**
- ✅ **Autómata Finito Determinista (AFD / DFA)**

## 📚 Descripción de los Programas

### 1. Simulador de Máquina de Turing
Permite simular paso a paso una máquina de Turing simple. Cuenta con una cinta de entrada, visualización del cabezal de lectura/escritura y una tabla de transiciones.

**Características:**
- Simulación paso a paso.
- Visualización de la cinta y el estado actual.
- Tabla dinámica de transiciones.

### 2. Simulador de Autómata Finito No Determinista (AFND)
Simula un AFND con posibilidad de retroceder y avanzar paso a paso. Muestra los conjuntos de estados alcanzados en cada paso, incluyendo transiciones epsilon.

**Características:**
- Soporte para transiciones ε.
- Visualización de estados alcanzados.
- Botones para avanzar y retroceder.
- Tabla de pasos con transiciones utilizadas.

### 3. Simulador de Autómata Finito Determinista (AFD)
Representa un AFD que reconoce cadenas que contienen al menos una vez el patrón "01".

**Características:**
- Reconocimiento de cadenas que contienen "01" en cualquier posición.
- Visualización de la cinta de entrada con separación de símbolos.
- Resaltado dinámico del símbolo actual.
- Estado actual mostrado en cada paso.
- Tabla de transiciones extendida con columnas: Estado, Símbolo, Nuevo Estado, Escritura, Movimiento.

---

## 🛠️ Requisitos

- Python 3.x
- Librería estándar `tkinter` (incluida por defecto en Python)

---

## ▶️ Cómo ejecutar

Ejecutá cualquiera de los archivos `.py` en tu entorno local con Python:

```bash
python simulador_turing.py
python simulador_nfa.py
python simulador_dfa.py
python simulador_dfa_patron01.py
```

---

## 📚 Créditos Académicos

Este conjunto de simuladores fue desarrollado como trabajo práctico para la materia **Teoría de la Computación** de la carrera **Ingeniería en Sistemas**.

**Autores:**
- Ignacio Parra
- Santiago Guglielmone
- Gonzalo Mata

---

## 📩 Contacto

Para consultas o sugerencias, podés comunicarte con cualquiera de los autores.

