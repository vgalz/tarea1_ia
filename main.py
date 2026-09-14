#ejecutar python3 main.py
import os
import time
from simulacion import ejecutar_simulacion_genetica
from entorno.grilla import Mapa

def limpiar_pantalla():
    #limpiar la consola
    os.system('cls' if os.name == 'nt' else 'clear')
def visualizar_ruta(mapa, inicio, objetivo, adn):
    fila_actual, col_actual = inicio
    movimientos = {
        0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 4: (0, 0)
    }
    
    # Lista para guardar los estados originales y no arruinar el mapa
    historial_cambios = []
    
    for gen in adn:
        df, dc = movimientos[gen]
        nueva_fila, nueva_col = fila_actual + df, col_actual + dc
        
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_col < mapa.columnas:
            estado = mapa.matriz[nueva_fila][nueva_col].estado
            
            if estado == 'm':
                pass # Choca con un muro, se queda en el mismo lugar
            elif estado == 'f':
                break # Pisa fuego y muere, termina el trazado aquí
            else:
                # Movimiento válido
                fila_actual, col_actual = nueva_fila, nueva_col
                
                # Si la celda no es la de inicio ni la salida, la marcamos
                if (fila_actual, col_actual) not in [inicio, objetivo]:
                    # Guardamos el estado original si no lo hemos guardado antes
                    if not any(f == fila_actual and c == col_actual for f, c, _ in historial_cambios):
                        historial_cambios.append((fila_actual, col_actual, estado))
                    
                    # Marcamos la ruta con un asterisco
                    mapa.matriz[fila_actual][col_actual].estado = '*'
                    
        # Si llega a la salida, detenemos el trazado
        if (fila_actual, col_actual) == objetivo:
            break
            
    print("\n[*] Ruta trazada en el mapa (marcada con '*'):")
    mapa.mostrar_mapa()
    
    # Limpiamos el mapa restaurando los estados originales
    for f, c, estado_original in historial_cambios:
        mapa.matriz[f][c].estado = estado_original
def main():
    # Instanciamos el entorno de pruebas una sola vez al inicio
    mapa_actual = Mapa(filas=10, columnas=10)
    
    # Coordenadas de inicio ('s') y salida ('g') plantilla
    inicio = (1, 1)
    objetivo = (8, 8)

    while True:
        print("\n" + "="*40)
        print(" SIMULADOR DE EVACUACIÓN - TAREA 1")
        print("="*40)
        print(" Búsqueda No Informada:")
        print("   1. Ejecutar BFS (Búsqueda en Anchura) o otro")
        print("   2. Ejecutar DFS (Búsqueda en Profundidad) o otro")
        print("\n Búsqueda Informada:")
        print("   3. Ejecutar A* (A-Estrella) o otro")
        print("   4. Ejecutar Greedy Best-First Search o otro")
        print("\n Optimización Bioinspirada:")
        print("   5. Ejecutar Algoritmo Genético (Bacterias)")
        print("\n Herramientas de Visualización:")
        print("   6. Mostrar estado actual del mapa")
        print("   7. Simular propagación del fuego (1 turno)")
        print("   8. Reiniciar mapa al estado original")
        print("\n   0. Salir")
        print("="*40)
        
        opcion = input("Seleccione un modo de ejecución: ")

        # poner los case en simulacion.py y llamar el metodo aqui
        match opcion:
            case '1':
                print("\n[!] Ejecutando BFS... (Pendiente de implementar)")
                # logica_bfs(mapa_actual, inicio)
            
            case '2':
                print("\n[!] Ejecutando DFS... (Pendiente de implementar)")
                # logica_dfs(mapa_actual, inicio)
            
            case '3':
                print("\n[!] Ejecutando A*... (Pendiente de implementar)")
                # logica_astar(mapa_actual, inicio, objetivo)
            
            case '4':
                print("\n[!] Ejecutando Greedy... (Pendiente de implementar)")
                # logica_greedy(mapa_actual, inicio, objetivo)
            
            case '5':
               ejecutar_simulacion_genetica(mapa_actual)
            case '6':
                print("\n[*] Mapa actual:")
                mapa_actual.mostrar_mapa()
            
            case '7':
                print("\n[*] El fuego se ha propagado 1 turno.")
                mapa_actual.propagar_fuego()
                mapa_actual.mostrar_mapa()
                
            case '8':
                print("\n[*] Reiniciando mapa...")
                mapa_actual = Mapa(filas=10, columnas=10)
                print("Mapa reiniciado a su estado original.")
            
            case '0':
                print("\nSaliendo del simulador... ¡Éxito en la tarea!")
                break
                
            case _:
                # El equivalent a 'default' en C
                print("\n[x] Opción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()

if __name__ == "__main__":
    main()