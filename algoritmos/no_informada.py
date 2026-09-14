from collections import deque


DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def _vecinos_transitables(mapa, posicion):
	fila, columna = posicion
	for delta_fila, delta_columna in DIRECCIONES:
		nueva_fila = fila + delta_fila
		nueva_columna = columna + delta_columna
		dentro_del_mapa = (
			0 <= nueva_fila < mapa.filas
			and 0 <= nueva_columna < mapa.columnas
		)
		if not dentro_del_mapa:
			continue
		if mapa.matriz[nueva_fila][nueva_columna].estado in ('m', 'f'):
			continue
		yield (nueva_fila, nueva_columna)


def costo_transito(mapa, posicion, alpha=2.0):
	ocupacion = mapa.matriz[posicion[0]][posicion[1]].ocupacion
	return 1 + alpha * (ocupacion ** 2)


def _reconstruir_ruta(predecesores, inicio, objetivo):
	if objetivo not in predecesores:
		return None

	ruta = []
	actual = objetivo
	while actual != inicio:
		ruta.append(actual)
		actual = predecesores[actual]
	ruta.reverse()
	return ruta


def bfs(mapa, inicio, objetivo):
	"""Encuentra una ruta de menor cantidad de pasos usando BFS."""
	frontera = deque([inicio])
	predecesores = {inicio: None}

	while frontera:
		actual = frontera.popleft()
		if actual == objetivo:
			return _reconstruir_ruta(predecesores, inicio, objetivo)

		for vecino in _vecinos_transitables(mapa, actual):
			if vecino not in predecesores:
				predecesores[vecino] = actual
				frontera.append(vecino)

	return None


def dfs(mapa, inicio, objetivo):
	"""Encuentra una ruta usando búsqueda en profundidad."""
	frontera = [inicio]
	predecesores = {inicio: None}

	while frontera:
		actual = frontera.pop()
		if actual == objetivo:
			return _reconstruir_ruta(predecesores, inicio, objetivo)

		for vecino in _vecinos_transitables(mapa, actual):
			if vecino not in predecesores:
				predecesores[vecino] = actual
				frontera.append(vecino)

	return None
