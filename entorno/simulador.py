from collections import Counter
from dataclasses import dataclass

from algoritmos import obtener_algoritmo


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


def _crear_agentes(mapa):
    agentes = []
    siguiente_id = 1
    for fila in range(mapa.filas):
        for columna in range(mapa.columnas):
            if mapa.matriz[fila][columna].estado == 's':
                agentes.append(AgenteSimulacion(siguiente_id, fila, columna))
                siguiente_id += 1
    return agentes


def _actualizar_ocupacion(mapa, agentes):
    for fila in mapa.matriz:
        for celda in fila:
            celda.ocupacion = 0
    for agente in agentes:
        if agente.estado == 'vivo':
            mapa.matriz[agente.fila][agente.columna].ocupacion += 1


def _marcar_bajas_por_fuego(mapa, agentes):
    for agente in agentes:
        if (
            agente.estado == 'vivo'
            and mapa.matriz[agente.fila][agente.columna].estado == 'f'
        ):
            agente.estado = 'muerto'


def ejecutar_episodio(mapa, algoritmo, k_turnos_fuego=2, max_turnos=200):
    """Ejecuta un episodio reproducible sin salida por consola ni pausas."""
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
    buscar = obtener_algoritmo(algoritmo)
    turno = 0
    _marcar_bajas_por_fuego(mapa, agentes)

    while any(agente.estado == 'vivo' for agente in agentes) and turno < max_turnos:
        turno += 1
        _actualizar_ocupacion(mapa, agentes)

        for agente in agentes:
            if agente.estado != 'vivo':
                continue
            ruta = buscar(mapa, agente.posicion, objetivo)
            if ruta:
                agente.fila, agente.columna = ruta[0]
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
