from dataclasses import dataclass

from algoritmos import obtener_algoritmo
from algoritmos.genetico import AlgoritmoGenetico


@dataclass
class AgenteSimulacion:
    id: int
    fila: int
    columna: int
    estado: str = 'vivo'
    turno_escape: int | None = None

    @property
    def posicion(self):
        return (self.fila, self.columna)


def _crear_agentes(mapa): # crea un agente por cada 's' en el mapa
    agentes = []
    siguiente_id = 1
    for fila in range(mapa.filas):
        for columna in range(mapa.columnas):
            if mapa.matriz[fila][columna].estado == 's':
                agentes.append(AgenteSimulacion(siguiente_id, fila, columna))
                siguiente_id += 1
    return agentes


def _actualizar_ocupacion(mapa, agentes): # actualiza la ocupacion de cada celda en el mapa
    for fila in mapa.matriz:
        for celda in fila:
            celda.ocupacion = 0
    for agente in agentes:
        if agente.estado == 'vivo':
            mapa.matriz[agente.fila][agente.columna].ocupacion += 1


def _marcar_bajas_por_fuego(mapa, agentes): # marca como 'muerto' a los agentes que se encuentren en celdas en fuego
    for agente in agentes:
        if (
            agente.estado == 'vivo'
            and mapa.matriz[agente.fila][agente.columna].estado == 'f'
        ):
            agente.estado = 'muerto'

def _proponer_destinos(mapa, agentes, objetivo, buscar): # crea un diccionario para cada agente con su propuesta de movimiento hacia el objetivo usando el algoritmo de busqueda
    propuestas = {}
    for agente in agentes:
        if agente.estado != 'vivo':
            continue
        ruta = buscar(mapa, agente.posicion, objetivo)
        propuestas[agente.id] = ruta[0] if ruta else agente.posicion
    return propuestas


def _ruta_genetica(mapa, inicio, objetivo): # usa el algoritmo genetico para encontrar una ruta desde inicio hasta objetivo
    genetico = AlgoritmoGenetico(
        mapa=mapa,
        inicio=inicio,
        objetivo=objetivo,
        tam_poblacion=40,
        longitud_adn=20,
    )
    mejor_individuo = genetico.evolucionar(generaciones=20, verbose=False) # evoluciona 20 generaciones para encontrar la mejor ruta
    movimientos = {
        0: (-1, 0),
        1: (1, 0),
        2: (0, -1),
        3: (0, 1),
        4: (0, 0),
    }
    fila, columna = inicio
    ruta = []
    for gen in mejor_individuo.adn: # recorre cada gen del adn de la mejor bacteria y calcula la nueva posicion en el mapa
        delta_fila, delta_columna = movimientos[gen]
        nueva_posicion = (fila + delta_fila, columna + delta_columna)
        if not (
            0 <= nueva_posicion[0] < mapa.filas
            and 0 <= nueva_posicion[1] < mapa.columnas
        ):
            continue
        if mapa.matriz[nueva_posicion[0]][nueva_posicion[1]].estado in ('m', 'f'):
            continue
        fila, columna = nueva_posicion
        ruta.append(nueva_posicion)
        if nueva_posicion == objetivo:
            break
    return ruta


def _resolver_movimientos(agentes, propuestas):
    # resuelve los movimientos de los agentes según las propuestas
    por_destino = {}
    for agente in agentes:
        if agente.estado == 'vivo':
            destino = propuestas.get(agente.id, agente.posicion)
            por_destino.setdefault(destino, []).append(agente)

    destinos_aprobados = {}
    for destino, candidatos in por_destino.items():
        ganador = min(candidatos, key=lambda agente: agente.id)
        destinos_aprobados[ganador.id] = destino

    posiciones_actuales = {
        agente.id: agente.posicion
        for agente in agentes
        if agente.estado == 'vivo'
    }
    for agente in agentes:
        destino = destinos_aprobados.get(agente.id, agente.posicion)
        ocupante = next(
            (
                agente_id
                for agente_id, posicion in posiciones_actuales.items()
                if posicion == destino
            ),
            None,
        )
        if ocupante is None or ocupante == agente.id:
            continue
        if destinos_aprobados.get(ocupante) == agente.posicion:
            destinos_aprobados[agente.id] = agente.posicion
            destinos_aprobados[ocupante] = posiciones_actuales[ocupante]

    for agente in agentes:
        if agente.estado != 'vivo':
            continue
        destino = destinos_aprobados.get(agente.id, agente.posicion)
        agente.fila, agente.columna = destino


def ejecutar_episodio(mapa, algoritmo, k_turnos_fuego=2, max_turnos=200):
    # ejecuta un episodio reproducible sin salida por consola ni pausas.
    agentes = _crear_agentes(mapa)
    objetivos = [
        (fila, columna)
        for fila in range(mapa.filas)
        for columna in range(mapa.columnas)
        if mapa.matriz[fila][columna].estado == 'g'
    ]
    if not agentes or len(objetivos) != 1:
        raise ValueError('El mapa debe tener agentes y exactamente una salida.')

    objetivo = objetivos[0]
    buscar = (
        None
        if algoritmo.lower() == 'genetico'
        else obtener_algoritmo(algoritmo)
    )
    turno = 0
    _marcar_bajas_por_fuego(mapa, agentes)

    while any(agente.estado == 'vivo' for agente in agentes) and turno < max_turnos:
        turno += 1
        _actualizar_ocupacion(mapa, agentes)

        if buscar is None:
            propuestas = {
                agente.id: (
                    _ruta_genetica(mapa, agente.posicion, objetivo)[:1] or [
                        agente.posicion
                    ]
                )[0]
                for agente in agentes
                if agente.estado == 'vivo'
            }
        else:
            propuestas = _proponer_destinos(mapa, agentes, objetivo, buscar)
        _resolver_movimientos(agentes, propuestas)
        _actualizar_ocupacion(mapa, agentes)

        for agente in agentes:
            if agente.estado != 'vivo':
                continue
            if agente.posicion == objetivo:
                agente.estado = 'escapo'
                agente.turno_escape = turno

        if turno % k_turnos_fuego == 0:
            mapa.propagar_fuego()
            _marcar_bajas_por_fuego(mapa, agentes)

    escapados = [agente for agente in agentes if agente.estado == 'escapo']
    muertos = [agente for agente in agentes if agente.estado == 'muerto']
    tiempo_despeje = max(
        (agente.turno_escape for agente in escapados),
        default=max_turnos,
    )
    total = len(agentes)

    # resultados del episodio
    return {
        'algoritmo': algoritmo,
        'agentes_iniciales': total,
        'escapados': len(escapados),
        'muertos': len(muertos),
        'vivos': total - len(escapados) - len(muertos),
        'tasa_supervivencia': len(escapados) / total if total else 0.0,
        'tiempo_despeje': tiempo_despeje,
        'turnos_ejecutados': turno,
    }
