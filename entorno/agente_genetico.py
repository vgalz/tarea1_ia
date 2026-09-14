from algoritmos.genetico import AlgoritmoGenetico

class AgenteGenetico:
    def __init__(self, id_agente, fila, col):
        self.id = id_agente
        self.fila = fila
        self.col = col
        self.estado = 'vivo' # estados  'vivo', 'escapo', 'muerto'
        self.ruta_planeada = [] #  secuencia de genes/movimientos
        self.objetivo = None

    @classmethod
    def spawnear_desde_mapa(cls, mapa):
        # lee el mapa, busca todas las 's' y crea un agente por cada una.
        # tambien detecta donde esta la 'g' (salida) para asignarla como objetivo.
        agentes_creados = []
        objetivo_encontrado = None
        id_contador = 1
        
        for f in range(mapa.filas):
            for c in range(mapa.columnas):
                estado_celda = mapa.matriz[f][c].estado
                if estado_celda == 's':
                    agentes_creados.append(cls(id_contador, f, c))
                    id_contador += 1
                elif estado_celda == 'g':
                    objetivo_encontrado = (f, c)
                    
        # asignamos el objetivo a todos los agentes creados
        for agente in agentes_creados:
            agente.objetivo = objetivo_encontrado
            
        return agentes_creados, objetivo_encontrado

    def replanificar(self, mapa):
        # usa el algoritmo genetico desde su posicion actual para buscar la salida
        if self.estado != 'vivo':
            return
            
        genetico = AlgoritmoGenetico(
            mapa=mapa, 
            inicio=(self.fila, self.col), 
            objetivo=self.objetivo, 
            tam_poblacion=80, 
            longitud_adn=20 
        )
        # evoluciona en silencio para encontrar la ruta
        mejor_bacteria = genetico.evolucionar(generaciones=60)
        self.ruta_planeada = mejor_bacteria.adn

    def mover(self, mapa):
        # da un paso usando su ruta planeada
        if self.estado != 'vivo' or not self.ruta_planeada:
            return
            
        gen_actual = self.ruta_planeada.pop(0) # extrae el primer movimiento
        movimientos = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 4: (0, 0)}
        df, dc = movimientos[gen_actual]
        nueva_fila, nueva_col = self.fila + df, self.col + dc
        
        # validar si el paso es legal y no es un muro
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_col < mapa.columnas:
            estado_destino = mapa.matriz[nueva_fila][nueva_col].estado
            if estado_destino != 'm':
                # el agente se mueve
                self.fila = nueva_fila
                self.col = nueva_col
                
        # revisar si piso fuego al moverse
        if mapa.matriz[self.fila][self.col].estado == 'f':
            self.estado = 'muerto'
        # revisar si llego a la salida
        elif (self.fila, self.col) == self.objetivo:
            self.estado = 'escapo'