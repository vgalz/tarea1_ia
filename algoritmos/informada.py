import heapq
from itertools import count

from algoritmos.no_informada import (
	costo_transito,
	_reconstruir_ruta,
	_vecinos_transitables,
)


def distancia_manhattan(posicion, objetivo):
	return abs(posicion[0] - objetivo[0]) + abs(posicion[1] - objetivo[1])


def a_estrella(mapa, inicio, objetivo):
	"""Encuentra una ruta de costo minimo con la heuristica Manhattan."""
	contador = count()
	frontera = [(distancia_manhattan(inicio, objetivo), 0, next(contador), inicio)]
	predecesores = {inicio: None}
	costos = {inicio: 0}

	while frontera:
		_, costo_actual, _, actual = heapq.heappop(frontera)
		if costo_actual != costos[actual]:
			continue
		if actual == objetivo:
			return _reconstruir_ruta(predecesores, inicio, objetivo)

		for vecino in _vecinos_transitables(mapa, actual):
			nuevo_costo = costo_actual + costo_transito(mapa, vecino)
			if nuevo_costo < costos.get(vecino, float('inf')):
				costos[vecino] = nuevo_costo
				predecesores[vecino] = actual
				prioridad = nuevo_costo + distancia_manhattan(vecino, objetivo)
				heapq.heappush(
					frontera,
					(prioridad, nuevo_costo, next(contador), vecino),
				)

	return None


def greedy_best_first(mapa, inicio, objetivo):
	"""Encuentra una ruta priorizando la heuristica Manhattan."""
	contador = count()
	frontera = [(distancia_manhattan(inicio, objetivo), next(contador), inicio)]
	predecesores = {inicio: None}

	while frontera:
		_, _, actual = heapq.heappop(frontera)
		if actual == objetivo:
			return _reconstruir_ruta(predecesores, inicio, objetivo)

		for vecino in _vecinos_transitables(mapa, actual):
			if vecino not in predecesores:
				predecesores[vecino] = actual
				prioridad = distancia_manhattan(vecino, objetivo)
				heapq.heappush(frontera, (prioridad, next(contador), vecino))

	return None


astar = a_estrella
greedy = greedy_best_first
