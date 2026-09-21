# Escape de la Torre - Tarea 1 de IA
### Victor Galaz Garrido - 2024431005

## Resumen
Esta tarea implementa un sistema de evacuación en una grilla con fuego, congestionamiento y múltiples estrategias de búsqueda. Se comparan algoritmos de búsqueda no informada, búsqueda informada y genéticos para evaluar supervivencia y tiempo de despeje en escenarios con distinta dificultad.

## Requisitos
- Python 3.10 o superior
- matplotlib
- numpy

Instalar dependencias:
```powershell
pip install -r requirements.txt
```

## Ejecución
1. Abrir una terminal en la raíz del proyecto.
2. Ejecutar:
   `python main.py`
3. Para resultados experimentales:
   `python benchmark.py --iteraciones x --max-turnos x --semilla 0`

### Benchmark recomendado
- Ejecución completa:
  `python benchmark.py --iteraciones 200 --max-turnos 200 --semilla 0`
- El comando genera un archivo CSV llamado resultados_benchmark.csv con las métricas por escenario y algoritmo.
- Naturalmente, este método demora más tiempo que la ejecución rápida, aunque tampoco debería ser demasiado (menos de un minuto).

### Visualizacion de resultados
Una vez creado el CSV, generar el grafico comparativo con:
```powershell
python visualizar_resultados.py
```
Se crea `resultados_benchmark.png` con dos paneles por escenario:
- tasa media de supervivencia por algoritmo;
- tiempo medio de despeje, desviacion estandar y rango minimo-maximo.

## Algoritmos implementados
- Búsqueda no informada: BFS, DFS
- Búsqueda informada: A*, Greedy Best-First Search
- Algoritmo Genético

## Escenarios del entorno
- Cuello: pasillo estrecho y alta congestión
- Laberinto: rutas con cruces y bloques intermedios
- Abierto: mayor libertad de movimiento y menos obstrucción

## Métricas evaluadas
- Tasa de supervivencia
- Tiempo de despeje promedio, desviación estándar, mínimo y máximo
- Resultados por escenario y algoritmo

## Notas
- El fuego se propaga de forma determinista según una semilla, de manera reproducible.
- La ocupación de cada celda penaliza el costo real del tránsito.
- Los movimientos simultáneos evitan ocupación duplicada por dos agentes en la misma celda.
- Los algoritmos de búsqueda comparten una interfaz común para facilitar comparación.

- Se implementaron soluciones propias para BFS, DFS y Greedy, reutilizadas de trabajos anteriores pero adaptadas al contexto de esta tarea.
- A*, simulador y benchmarks se generan con apoyo de inteligencia artificial generativa (GPT-5.6 Luna). 
- El algoritmo genético es una implementación en conjunto con compañeros del curso, antes de saber que la tarea era de entrega individual.