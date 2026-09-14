#Funcion fittnes
#F(x)= 1/(1+distancia manhatan - sumatoria (pasos arriba, abajo i=1)(Cocupacion(celdai)-penalizaciones)
#maxmiza acercarse al destino y minimiza por chocar, quemarse, generar embotellamiento
# Cocupacion(celda)= alpha por ocupacion_actual al cuadrado
#reglas
# llegar al goal, bono de puntos
#chocar un muro, detiene el movimiento, penalizacion de puntos
#pisar fuego, detiene el movimiento, penalizacion de puntos


import random
import time
import os

class Bacteria:
    def __init__(self, longitud_adn):
        # ADN: 0=Arriba, 1=Abajo, 2=Izquierda, 3=Derecha, 4=Esperar, cada bacteria tiene una combinacion de estos movimientos
        self.adn = [random.randint(0, 4) for _ in range(longitud_adn)]
        #parten con 0 en fitnes
        self.fitness = 0.0

class AlgoritmoGenetico:
    def __init__(self, mapa, inicio, objetivo, tam_poblacion=100, longitud_adn=30, tasa_mutacion=0.05):
        self.mapa = mapa #mapa que se da
        self.inicio = inicio # s en el mapa
        self.objetivo = objetivo # g en el mapa
        self.tam_poblacion = tam_poblacion #cantidad de bacterias que se generan
        self.longitud_adn = longitud_adn #cantidad de pasos que puede dar cada bacteria
        self.tasa_mutacion = tasa_mutacion # probabilidad de mutar
        
        #población inicial de bacterias
        self.poblacion = [Bacteria(longitud_adn) for _ in range(tam_poblacion)]
        #la heuristica, que considere mejor
    def _calcular_distancia_manhattan(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    #aqui se evalua el fitness
    def evaluar_fitness(self, bacteria):
        #la bacteria parte del inici
        fila_actual, col_actual = self.inicio
        penalizacion_total = 0
        costo_embotellamiento = 0
        llego_meta = False
        
        # mapeo de genes a movimientos
        movimientos = {
            0: (-1, 0), # Arriba
            1: (1, 0),  # Abajo
            2: (0, -1), # Izquierda
            3: (0, 1),  # Derecha
            4: (0, 0)   # Esperar 
        }

        #itera cada gen del adn
        for gen in bacteria.adn:
            df, dc = movimientos[gen]
            #calcula la nueva posicion de la bacteria
            nueva_fila, nueva_col = fila_actual + df, col_actual + dc
            
            # Verificamos límites del mapa
            if 0 <= nueva_fila < self.mapa.filas and 0 <= nueva_col < self.mapa.columnas:
                estado_celda = self.mapa.matriz[nueva_fila][nueva_col].estado
                
                if estado_celda == 'm':
                    # Choca con un muro, no avanza
                    penalizacion_total += 50
                elif estado_celda == 'f':
                    # Pisa fuego, muere y termina el ciclo
                    penalizacion_total += 500
                    break 
                else:
                    # Movimiento válido pasillo 'd' o 'goal' o 's'
                    fila_actual, col_actual = nueva_fila, nueva_col
                    
                    # Cálculo de función cuadrática por saturación de vías
                    ocupacion = self.mapa.matriz[fila_actual][col_actual].ocupacion
                    costo_embotellamiento += 2.0 * (ocupacion ** 2) 

            #verifico si llego a la meta
            if (fila_actual, col_actual) == self.objetivo:
                llego_meta = True
                break

        # calculo distancia
        distancia_final = self._calcular_distancia_manhattan((fila_actual, col_actual), self.objetivo)
        
        # Bono si sobrevive y llega a la salida
        bono_meta = 2000 if llego_meta else 0 

        #formula de fitness
        bacteria.fitness = (1000 / (1 + distancia_final)) + bono_meta - penalizacion_total - costo_embotellamiento
        
        # evito negativos
        bacteria.fitness = max(0.1, bacteria.fitness)


#fase de reproduccion, mutacionm, cruce
    def seleccion_torneo(self):
        #selecciona 3 bacterias al azar y devuelve la de mayor fitness
        torneo = random.sample(self.poblacion, 3)
        #ordenamos por fitness descendente y devolvemos la mejor
        torneo.sort(key=lambda x: x.fitness, reverse=True)
        return torneo[0]

    def cruzar(self, padre1, padre2):
        hijo = Bacteria(self.longitud_adn)
        # Punto de cruce aleatorio, una lado un padre y el otro lado el otro padre
        punto = random.randint(1, self.longitud_adn - 2)
        hijo.adn = padre1.adn[:punto] + padre2.adn[punto:]
        return hijo

    def mutar(self, bacteria):
        #recorre cada gen del adn y con probabilidad del 5 porciento muta uno de los genes, independientemete por cada gen
        for i in range(self.longitud_adn):
            if random.random() < self.tasa_mutacion:
                #la bacteria sufre una mutación aleatoria en su dirección
                bacteria.adn[i] = random.randint(0, 4)

    def evolucionar(self, generaciones=100):

        #evoluciona 100 veces
        for gen in range(generaciones):
            #evaluo cada bacteria viva
            for bacteria in self.poblacion:
                self.evaluar_fitness(bacteria)
            
            #Ordenamos para encontrar al mejor individuo de la generación
            self.poblacion.sort(key=lambda x: x.fitness, reverse=True)
            mejor_bacteria = self.poblacion[0]
            
            #Crear nueva generación
            nueva_poblacion = [mejor_bacteria] # la mejor bacteria siempre sobrevive
            
            while len(nueva_poblacion) < self.tam_poblacion:
                #seleccionamos dos padres mediante torneo, cruzamos y mutamos para crear un hijo
                padre1 = self.seleccion_torneo()
                padre2 = self.seleccion_torneo()
                hijo = self.cruzar(padre1, padre2)
                self.mutar(hijo)
                nueva_poblacion.append(hijo)
                
            self.poblacion = nueva_poblacion
            #print(f"Generación {gen+1} | Mejor Fitness: {mejor_bacteria.fitness:.2f}")

        return self.poblacion[0] # Retorna la bacteria con la ruta más óptima







    def mostrar_ruta(self, bacteria, retardo=0.4):
        fila_actual, col_actual = self.inicio
        movimientos = {
            0: (-1, 0), # Arriba
            1: (1, 0),  # Abajo
            2: (0, -1), # Izquierda
            3: (0, 1),  # Derecha
            4: (0, 0)   # Esperar
        }

        # Creamos una copia visual de la grilla
        mapa_visual = []
        for i in range(self.mapa.filas):
            fila_visual = []
            for j in range(self.mapa.columnas):
                fila_visual.append(self.mapa.matriz[i][j].estado)
            mapa_visual.append(fila_visual)

        paso = 1
        for gen in bacteria.adn:
            # Limpiamos la pantalla para el efecto de animación
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n--- PASO {paso} ---")
            
            df, dc = movimientos[gen]
            nueva_fila, nueva_col = fila_actual + df, col_actual + dc
            
            # Verificamos el movimiento
            if 0 <= nueva_fila < self.mapa.filas and 0 <= nueva_col < self.mapa.columnas:
                estado_celda = mapa_visual[nueva_fila][nueva_col]
                
                if estado_celda == 'm':
                    print("[!] Chocó con un muro y no avanzó.")
                elif estado_celda == 'f':
                    mapa_visual[fila_actual][col_actual] = 'X' # Marca de muerte
                    self._imprimir_cuadro(mapa_visual)
                    print("\n[X] ¡Pisó fuego y murió!")
                    break 
                else:
                    # Dejamos un rastro '+' en la posición que abandonamos
                    if mapa_visual[fila_actual][col_actual] not in ['s', 'g']:
                        mapa_visual[fila_actual][col_actual] = '+'
                    # Actualizamos a la nueva posición
                    fila_actual, col_actual = nueva_fila, nueva_col
                    print("[+] Avanzó con éxito.")
            else:
                print("[!] Intentó salir del mapa.")

            # Guardamos el estado de la celda actual para no borrar la 'g' o 's'
            valor_original = mapa_visual[fila_actual][col_actual]
            
            # Dibujamos a la bacteria 'B' en su posición actual
            mapa_visual[fila_actual][col_actual] = 'B'
            
            # Imprimimos la grilla
            self._imprimir_cuadro(mapa_visual)
            
            # Restauramos el valor de la celda para el siguiente turno
            if valor_original in ['s', 'g']:
                mapa_visual[fila_actual][col_actual] = valor_original
            else:
                mapa_visual[fila_actual][col_actual] = '+'
            
            # Condición de victoria
            if (fila_actual, col_actual) == self.objetivo:
                print("\n[VICTORIA] ¡Llegó a la salida!")
                break
                
            # Pausa para ver la animación
            time.sleep(retardo)
            paso += 1

    def _imprimir_cuadro(self, mapa_visual):
        # Método de ayuda para imprimir la matriz de forma ordenada
        for fila in mapa_visual:
            print(" ".join(fila))
        print("-" * 33)