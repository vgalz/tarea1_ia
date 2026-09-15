from entorno.grilla import Mapa

# archivo que define los escenarios del entorno
_PLANTILLAS = { # ejemplos de escenarios de prueba, donde 'm' es muro, 's' es salida, 'g' es goal, 'd' es espacio libre y 'f' es fuego. hechos a mano y al ojo
    'cuello': (
        'mmmmmmmmmm',
        'msdddddddm',
        'mmmmmmmmdm',
        'mddddddddm',
        'mddddddddm',
        'mmmmmmmmdm',
        'msdddddddm',
        'mmmmmmmmdm',
        'mdddddddg m'.replace(' ', ''),
        'mmmmmmmmmm',
    ),
    'laberinto': (
        'mmmmmmmmmm',
        'msddmddddm',
        'mmdmdmmmdm',
        'mdddddmdgm',
        'mmdmmmdmdm',
        'mdddmddddm',
        'mdmdmmmdmm',
        'msdddddddm',
        'mmmmmmmmmm',
        'mmmmmmmmmm',
    ),
    'abierto': (
        'mmmmmmmmmm',
        'msdddddddm',
        'mddddddddm',
        'mddddddddm',
        'mddddddddm',
        'mddddddddm',
        'mddddddddm',
        'msdddddddm',
        'mdddddddg m'.replace(' ', ''),
        'mmmmmmmmmm',
    ),
}

# funciones para crear mapas a partir de plantillas y listar escenarios disponibles
def crear_mapa(nombre, seed=None):
    try:
        plantilla = _PLANTILLAS[nombre.lower()]
    except KeyError as error:
        disponibles = ', '.join(sorted(_PLANTILLAS))
        raise ValueError(f'Mapa desconocido: {nombre}. Disponibles: {disponibles}') from error
    return Mapa.desde_plantilla(plantilla, seed=seed)


def nombres_escenarios():
    return tuple(_PLANTILLAS)