from benchmark import ejecutar_benchmark
from entorno.escenarios import crear_mapa, nombres_escenarios
from entorno.simulador import ejecutar_episodio
from visualizar_resultados import crear_figura

# archivo que contiene pruebas unitarias para el benchmark y los escenarios
# pruebas verifican que los escenarios se carguen correctamente y que el benchmark se ejecute sin errores

def test_escenarios_validos():
    escenarios = nombres_escenarios()
    assert escenarios == ('cuello', 'laberinto', 'abierto')
    for nombre in escenarios:
        mapa = crear_mapa(nombre, seed=1)
        assert mapa.filas == 10
        assert mapa.columnas == 10


def test_episodio_bfs():
    mapa = crear_mapa('abierto', seed=7)
    resultado = ejecutar_episodio(mapa, 'bfs', max_turnos=20)
    assert set(resultado) >= {'algoritmo', 'escapados', 'muertos', 'tasa_supervivencia'}
    assert 0.0 <= resultado['tasa_supervivencia'] <= 1.0


def test_benchmark_pequeno():
    resultado = ejecutar_benchmark(
        iteraciones=1,
        max_turnos=20,
        semilla=2,
        escenarios=('abierto',),
        algoritmos=('bfs', 'astar'),
        genetico_poblacion=5,
        genetico_generaciones=2,
        mostrar_progreso=False,
    )
    assert len(resultado) == 2
    assert {'escenario', 'algoritmo', 'tiempo_media'}.issubset(set(resultado[0]))

def test_visualizacion_desde_resultados():
    resultados = ejecutar_benchmark(
        iteraciones=1,
        max_turnos=20,
        semilla=2,
        escenarios=('abierto',),
        algoritmos=('bfs', 'astar'),
        mostrar_progreso=False,
    )
    figura = crear_figura(resultados)
    assert len(figura.axes) == 2
    figura.canvas.draw()
    figura.clf()