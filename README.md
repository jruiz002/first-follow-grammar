# Proyecto FIRST y FOLLOW - Arquitectura Pipeline

Este proyecto implementa los algoritmos de **FIRST** y **FOLLOW** para gramáticas libres de contexto (CFG), utilizando una arquitectura basada en **Pipeline** (tubería). Esta misma arquitectura se puede integrar fácilmente o servir de base para futuros analizadores sintácticos (Parsers LL(1), SLR, etc.).

## 🏗 Arquitectura del Sistema

La arquitectura está diseñada para que cada módulo tenga una única responsabilidad. Cada etapa del pipeline procesa la información y genera una estructura de datos que es consumida por el siguiente módulo.

```text
[Archivo de Gramática] 
        │
        ▼
 1. Lector de Gramática (grammar_reader.py)
        │ - Limpia comentarios y espacios extra.
        ▼
[Líneas de texto en crudo]
        │
        ▼
 2. Parser de Gramática (grammar_parser.py)
        │ - Identifica No-Terminales, Terminales y Producciones.
        ▼
[Objeto Grammar (Estructura de Datos)]
        │
        ├──────────────────────────┐
        ▼                          │
 3. Conjuntos FIRST (first.py)     │
        │ - Algoritmo FIRST.       │
        ▼                          │
[Diccionario FIRST]                │
        │                          │
        ▼                          ▼
 4. Conjuntos FOLLOW (follow.py) ◄─┘
        │ - Calcula FOLLOW usando la Gramática y el FIRST.
        ▼
[Diccionario FOLLOW]
```

## 🧩 Descripción de cada Módulo

### 1. `grammar_reader.py` (Lector)
- **Propósito:** Leer el archivo `.txt` que contiene la gramática.
- **Entrada:** Ruta al archivo de texto.
- **Salida:** Una lista de cadenas de texto (líneas válidas), sin comentarios ni líneas en blanco.
- **Responsabilidad:** Abstraer el acceso al sistema de archivos y limpiar el input inicial.

### 2. `grammar_parser.py` (Parser Interno)
- **Propósito:** Convertir el texto plano de la gramática en una estructura de datos formal en Python.
- **Entrada:** Lista de cadenas producida por el lector.
- **Salida:** Un objeto `Grammar` que contiene:
  - Símbolo inicial.
  - Conjunto de Terminales y No-Terminales.
  - Diccionario de producciones (`A -> ['B', 'C'] | ['d']`).
- **Responsabilidad:** Identificar la sintaxis de las reglas (ej: separar el lado izquierdo del lado derecho de la producción, manejar el operador `|`).

### 3. `first.py` (Algoritmo FIRST)
- **Propósito:** Calcular el conjunto FIRST para todos los símbolos (y cadenas de símbolos) de la gramática.
- **Entrada:** El objeto `Grammar` generado por el parser.
- **Salida:** Un diccionario que mapea cada Símbolo a su respectivo conjunto FIRST.
- **Responsabilidad:** Aplicar correctamente las reglas de derivación de épsilon (`ε`) y los símbolos terminales iniciales de manera recursiva o iterativa.

### 4. `follow.py` (Algoritmo FOLLOW)
- **Propósito:** Calcular el conjunto FOLLOW exclusivamente para los símbolos No-Terminales.
- **Entrada:** 
  - El objeto `Grammar`.
  - El diccionario `FIRST` (calculado en el paso anterior).
- **Salida:** Un diccionario que mapea cada Símbolo No-Terminal a su conjunto FOLLOW.
- **Responsabilidad:** Aplicar las reglas de subconjuntos, manejo del símbolo de fin de cadena (`$`) en el símbolo inicial, y propagación del FOLLOW cuando hay derivaciones hacia `ε`.

### 5. `main.py` (El Orquestador)
- **Propósito:** Unir todas las piezas.
- **Flujo:** Toma la ruta del archivo, invoca al lector, pasa el resultado al parser, invoca la generación de FIRST y finalmente la de FOLLOW, e imprime los resultados en formato legible.

## 🚀 ¿Por qué esta arquitectura?

1. **Reusabilidad:** Si mañana la gramática no viene de un TXT sino de un JSON o de tu propio *Lexer*, solo cambias el `grammar_reader.py`. Todo lo demás queda intacto.
2. **Desacoplamiento:** El cálculo de `FIRST` no sabe ni le importa cómo se leyó el archivo. Solo espera un objeto `Grammar` bien formado.
3. **Escalabilidad:** Esta es la antesala exacta de un Parser LL(1). Solo faltaría añadir un `parsing_table.py` que consuma `FIRST` y `FOLLOW` para generar la tabla predictiva de análisis sintáctico.

## 📝 Formato del Input (grammar.txt)
Las reglas deben definirse de la siguiente manera:
- Lado izquierdo separado del derecho por `->`.
- Diferentes producciones del mismo lado izquierdo separadas por `|` o en líneas nuevas.
- Épsilon se representa con el símbolo `e` o literal `epsilon`.
- Cada símbolo en el lado derecho separado por un espacio.

Ejemplo:
```text
S -> A B c
A -> a | e
B -> b
```
