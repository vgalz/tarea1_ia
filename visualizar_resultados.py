import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# para poder graficar la información exportada al CSV por benchmark.py

ALGORITMOS_ORDEN = ('bfs', 'dfs', 'astar', 'greedy', 'genetico')
NOMBRES_ALGORITMOS = {
    'bfs': 'BFS',
    'dfs': 'DFS',
    'astar': 'A*',
    'greedy': 'Greedy',
    'genetico': 'Genetico',
}
COLORES_ALGORITMOS = {
    'bfs': '#2563eb',
    'dfs': '#16a34a',
    'astar': '#dc2626',
    'greedy': '#d97706',
    'genetico': '#7c3aed',
}


def cargar_resultados(ruta):
    with open(ruta, newline='', encoding='utf-8') as archivo:
        resultados = list(csv.DictReader(archivo))
    if not resultados:
        raise ValueError('El CSV no contiene resultados.')
    campos_requeridos = {
        'escenario',
        'algoritmo',
        'supervivencia_media',
        'tiempo_media',
        'tiempo_desviacion_estandar',
        'tiempo_minimo',
        'tiempo_maximo',
    }
    faltantes = campos_requeridos - set(resultados[0])
    if faltantes:
        raise ValueError(f'Faltan columnas en el CSV: {sorted(faltantes)}')
    for resultado in resultados:
        for campo in campos_requeridos - {'escenario', 'algoritmo'}:
            resultado[campo] = float(resultado[campo])
    return resultados


def _ordenar_algoritmos(resultados):
    disponibles = {resultado['algoritmo'] for resultado in resultados}
    ordenados = [algoritmo for algoritmo in ALGORITMOS_ORDEN if algoritmo in disponibles]
    ordenados.extend(sorted(disponibles - set(ordenados)))
    return ordenados


def crear_figura(resultados):
    escenarios = []
    for resultado in resultados:
        if resultado['escenario'] not in escenarios:
            escenarios.append(resultado['escenario'])
    algoritmos = _ordenar_algoritmos(resultados)
    por_combinacion = {
        (resultado['escenario'], resultado['algoritmo']): resultado
        for resultado in resultados
    }

    figura, ejes = plt.subplots(
        nrows=len(escenarios),
        ncols=2,
        figsize=(14, max(4.5, 4.2 * len(escenarios))),
        squeeze=False,
        constrained_layout=True,
    )
    posiciones = np.arange(len(algoritmos))
    etiquetas = [NOMBRES_ALGORITMOS.get(algoritmo, algoritmo) for algoritmo in algoritmos]

    for indice, escenario in enumerate(escenarios):
        datos = [por_combinacion[(escenario, algoritmo)] for algoritmo in algoritmos]
        supervivencia = [dato['supervivencia_media'] * 100 for dato in datos]
        tiempos = [dato['tiempo_media'] for dato in datos]
        desviaciones = [dato['tiempo_desviacion_estandar'] for dato in datos]
        minimos = [dato['tiempo_minimo'] for dato in datos]
        maximos = [dato['tiempo_maximo'] for dato in datos]
        colores = [COLORES_ALGORITMOS.get(algoritmo, '#475569') for algoritmo in algoritmos]

        eje_supervivencia = ejes[indice][0]
        eje_supervivencia.bar(posiciones, supervivencia, color=colores)
        eje_supervivencia.set_title(f'{escenario.capitalize()}: tasa de supervivencia')
        eje_supervivencia.set_ylabel('Supervivencia (%)')
        eje_supervivencia.set_ylim(0, 100)
        eje_supervivencia.set_xticks(posiciones, etiquetas)
        eje_supervivencia.grid(axis='y', alpha=0.25)
        for posicion, valor in zip(posiciones, supervivencia):
            eje_supervivencia.text(
                posicion,
                min(valor + 3, 97),
                f'{valor:.1f}%',
                ha='center',
                va='bottom',
                fontsize=9,
            )

        eje_tiempo = ejes[indice][1]
        eje_tiempo.bar(
            posiciones,
            tiempos,
            color=colores,
            alpha=0.85,
            label='Media',
        )
        eje_tiempo.errorbar(
            posiciones,
            tiempos,
            yerr=desviaciones,
            fmt='none',
            ecolor='#111827',
            capsize=5,
            label='Desviacion estandar',
        )
        for posicion, minimo, maximo in zip(posiciones, minimos, maximos):
            eje_tiempo.vlines(posicion, minimo, maximo, color='#111827', linewidth=2)
            eje_tiempo.scatter(
                [posicion, posicion],
                [minimo, maximo],
                color='#111827',
                s=18,
                zorder=3,
            )
        eje_tiempo.set_title(f'{escenario.capitalize()}: tiempo de despeje')
        eje_tiempo.set_ylabel('Turnos')
        eje_tiempo.set_xticks(posiciones, etiquetas)
        eje_tiempo.grid(axis='y', alpha=0.25)
        if indice == 0:
            eje_tiempo.legend(loc='upper right')

    figura.suptitle('Benchmark de evacuacion por escenario y algoritmo', fontsize=16)
    return figura


def generar_graficos(ruta_csv='resultados_benchmark.csv', ruta_salida='resultados_benchmark.png'):
    resultados = cargar_resultados(ruta_csv)
    figura = crear_figura(resultados)
    figura.savefig(ruta_salida, dpi=180, bbox_inches='tight')
    return Path(ruta_salida)


def main():
    parser = argparse.ArgumentParser(
        description='Genera graficos desde resultados_benchmark.csv.'
    )
    parser.add_argument(
        '--csv',
        default='resultados_benchmark.csv',
        help='Ruta del CSV generado por benchmark.py.',
    )
    parser.add_argument(
        '--salida',
        default='resultados_benchmark.png',
        help='Ruta de la imagen PNG de salida.',
    )
    parser.add_argument(
        '--mostrar',
        action='store_true',
        help='Muestra la figura ademas de guardarla.',
    )
    args = parser.parse_args()
    resultados = cargar_resultados(args.csv)
    figura = crear_figura(resultados)
    figura.savefig(args.salida, dpi=180, bbox_inches='tight')
    print(f'Grafico guardado en {args.salida}')
    if args.mostrar:
        plt.show()
    else:
        plt.close(figura)


if __name__ == '__main__':
    main()
