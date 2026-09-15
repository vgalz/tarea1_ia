import csv
import argparse
import statistics
from entorno.escenarios import crear_mapa, nombres_escenarios
from entorno.simulador import ejecutar_episodio

# archivo que ejecuta benchmark de todos los algoritmos y escenarios, y guarda un resumen en CSV

ALGORITMOS = ('bfs', 'dfs', 'astar', 'greedy', 'genetico')


def _estadisticas(valores):
    return {
        'media': statistics.mean(valores),
        'desviacion_estandar': statistics.stdev(valores) if len(valores) > 1 else 0.0,
        'minimo': min(valores),
        'maximo': max(valores),
    }


def ejecutar_benchmark(
    iteraciones=200, # 200 iteraciones, aunque pueden ser menos
    max_turnos=200,
    semilla=0,
    escenarios=None,
    algoritmos=None,
    # parametros geneticos
    genetico_poblacion=20,
    genetico_generaciones=5,
    genetico_longitud_adn=20,
    mostrar_progreso=False,
):
    # ejecuta todas las combinaciones y devuelve una fila resumen por combinacion.
    escenarios = tuple(escenarios or nombres_escenarios())
    algoritmos = tuple(algoritmos or ALGORITMOS)
    if iteraciones < 1:
        raise ValueError('iteraciones debe ser mayor que cero.')

    resultados = []
    total_combinaciones = len(escenarios) * len(algoritmos)
    combinacion_actual = 0
    # itera sobre todos los escenarios y algoritmos, ejecutando el episodio varias veces para cada combinacion
    for nombre_escenario in escenarios:
        for nombre_algoritmo in algoritmos:
            combinacion_actual += 1
            if mostrar_progreso: # muestra el progreso de la ejecucion
                print(
                    f'[{combinacion_actual}/{total_combinaciones}] '
                    f'{nombre_escenario} / {nombre_algoritmo}',
                    flush=True,
                )
            episodios = []
            for iteracion in range(iteraciones):
                mapa = crear_mapa(nombre_escenario, seed=semilla + iteracion)
                episodios.append(
                    ejecutar_episodio(
                        mapa,
                        nombre_algoritmo,
                        max_turnos=max_turnos,
                        genetico_poblacion=genetico_poblacion,
                        genetico_generaciones=genetico_generaciones,
                        genetico_longitud_adn=genetico_longitud_adn,
                    )
                )

            tiempos = [episodio['tiempo_despeje'] for episodio in episodios]
            supervivencias = [
                episodio['tasa_supervivencia'] for episodio in episodios
            ]
            tiempo = _estadisticas(tiempos)
            resultados.append(
                {
                    'escenario': nombre_escenario,
                    'algoritmo': nombre_algoritmo,
                    'iteraciones': iteraciones,
                    'supervivencia_media': statistics.mean(supervivencias),
                    'tiempo_media': tiempo['media'],
                    'tiempo_desviacion_estandar': tiempo['desviacion_estandar'],
                    'tiempo_minimo': tiempo['minimo'],
                    'tiempo_maximo': tiempo['maximo'],
                }
            )
    return resultados


def guardar_csv(resultados, ruta): # se guarda un resumen de resultados en un archivo csv ubicado en la ruta
    if not resultados:
        raise ValueError('No hay resultados para guardar.')
    campos = list(resultados[0])
    with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(resultados)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ejecuta el benchmark de evacuacion.')
    parser.add_argument(
        '--iteraciones',
        type=int,
        default=10,
        help='Iteraciones por combinacion (por defecto: 10; recomendado: 200).',
    )
    parser.add_argument(
        '--max-turnos',
        type=int,
        default=100,
        help='Limite de turnos por episodio (por defecto: 100).',
    )
    parser.add_argument(
        '--semilla',
        type=int,
        default=0,
        help='Semilla inicial para los mapas.',
    )
    args = parser.parse_args()
    resumen = ejecutar_benchmark(
        iteraciones=args.iteraciones,
        max_turnos=args.max_turnos,
        semilla=args.semilla,
        mostrar_progreso=True,
    )
    guardar_csv(resumen, 'resultados_benchmark.csv')
    print(f'Se guardaron {len(resumen)} combinaciones en resultados_benchmark.csv')
