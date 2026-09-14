class Celda:
    def __init__(self,estado='d',heuristica=0.0):
        #Estados: d disponible, m muro, f fuego
        self.estado =estado
        self.heuristica=heuristica
        # cantidad de gente o agentes en la casilla
        self.ocupacion=0 

    def __repr__(self):
        #permite imprimir en pantalla
        return self.estado
