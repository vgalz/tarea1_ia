from algoritmos.informada import a_estrella, greedy_best_first
from algoritmos.no_informada import bfs, dfs


ALGORITMOS_BUSQUEDA = {
	'bfs': bfs,
	'dfs': dfs,
	'astar': a_estrella,
	'greedy': greedy_best_first,
}


def obtener_algoritmo(nombre):
	try:
		return ALGORITMOS_BUSQUEDA[nombre.lower()]
	except KeyError as error:
		disponibles = ', '.join(sorted(ALGORITMOS_BUSQUEDA))
		raise ValueError(
			f"Algoritmo desconocido: {nombre}. Disponibles: {disponibles}"
		) from error
