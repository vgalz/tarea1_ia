import random
from entorno.celda import Celda

class Mapa:
    def __init__(self, filas=10, columnas=10, seed=None):
        self.filas = filas
        self.columnas = columnas
        self.rng = random.Random(seed)
        self.matriz = []
        for i in range(self.filas):
            fila_actual = []
            for j in range(self.columnas):
                fila_actual.append(Celda(estado='d'))
            self.matriz.append(fila_actual)

        self._generar_entorno_basico()

    def _generar_entorno_basico(self):
        plantilla = [
            ['m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'],
            ['m', 's', 'd', 'd', 'm', 'd', 'd', 'm', 's', 'm'], # 's' (Inicio) en (1, 1)
            ['m', 'm', 'm', 'd', 'm', 'd', 'd', 'm', 'd', 'm'],
            ['m', 'd', 'd', 'd', 'm', 'd', 'd', 'm', 'd', 'm'],
            ['m', 'd', 'd', 'd', 'm', 'm', 'd', 'm', 'd', 'm'],
            ['m', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'm'],
            ['m', 'm', 'm', 'm', 'd', 'd', 'd', 'd', 'd', 'm'],
            ['m', 's', 'd', 'm', 'd', 'm', 'm', 'm', 'm', 'm'], # 's' (Inicio) en (7, 1)
            ['m', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'g', 'm'], # 'g' (Salida) en (8, 8)
            ['m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm']
        ]
        
        # Cargamos la plantilla
        for i in range(self.filas):
            for j in range(self.columnas):
                self.matriz[i][j].estado = plantilla[i][j]

        # El fuego inicial debe comenzar en un pasillo, no sobre un muro,
        # la salida o una posicion inicial.
        celdas_iniciales = [
            (f, c)
            for f in range(self.filas)
            for c in range(self.columnas)
            if self.matriz[f][c].estado == 'd'
        ]
        f_fila, f_col = self.rng.choice(celdas_iniciales)
        self.matriz[f_fila][f_col].estado = 'f'

    def propagar_fuego(self):
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        nuevas_celdas_en_fuego = set()

        # El fuego se expande a todas las celdas transitables adyacentes.
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.matriz[f][c].estado == 'f':
                    for df, dc in direcciones:
                        nf, nc = f + df, c + dc
                        if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                            if self.matriz[nf][nc].estado in ['d', 's', 'g']:
                                nuevas_celdas_en_fuego.add((nf, nc))

        for nf, nc in nuevas_celdas_en_fuego:
            self.matriz[nf][nc].estado = 'f'

    def mostrar_mapa(self):
        for fila in self.matriz:
            print(" ".join(str(celda) for celda in fila))
        print("-" * 20)