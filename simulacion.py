import os
import time
from entorno.agente_genetico import AgenteGenetico

def ejecutar_simulacion_genetica(mapa_actual):

    print("\n[*] Iniciando simulación Dinámica con Agentes (Genético)...")
    
    #El agente lee el mapa e instancia a las personas
    agentes, meta = AgenteGenetico.spawnear_desde_mapa(mapa_actual)
    
    if not agentes or not meta:
        print("[!] Error: No se encontró inicio ('s') o meta ('g') en el mapa.")
        return
        
    
    k_turnos_fuego = 2 
    turno_actual = 1
    
    # Declaramos las variables de conteo iniciales para evitar errores si el bucle termina de golpe
    escapados = 0
    muertos = 0
    
   
    while any(a.estado == 'vivo' for a in agentes):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n--- TURNO {turno_actual} ---")
        
        # A. Replanificación y Movimiento de los agentes
        for agente in agentes:
            if agente.estado == 'vivo':
                # Replanifica su ruta desde donde está parado
                agente.replanificar(mapa_actual)
                agente.mover(mapa_actual)
                
        #Propagación del fuego cada 'k' turnos
        if turno_actual % k_turnos_fuego == 0:
            mapa_actual.propagar_fuego()
            print("\n[!] ¡EL FUEGO SE HA PROPAGADO!")
            
            # Revisar si el nuevo fuego quemó a un agente que estaba quieto
            for agente in agentes:
                if agente.estado == 'vivo' and mapa_actual.matriz[agente.fila][agente.col].estado == 'f':
                    agente.estado = 'muerto'
                    
        # Visualización del estado actual
        visual = [[celda.estado for celda in fila] for fila in mapa_actual.matriz]
        
        for agente in agentes:
            if agente.estado == 'vivo':
                visual[agente.fila][agente.col] = 'A' # Dibujamos al Agente
            elif agente.estado == 'muerto':
                visual[agente.fila][agente.col] = 'X' # Dibujamos su cadáver
                
        print("\nEstado del mapa:")
        for fila in visual:
            print(" ".join(fila))
            
        # D. Resumen de estados
        vivos = sum(1 for a in agentes if a.estado == 'vivo')
        escapados = sum(1 for a in agentes if a.estado == 'escapo')
        muertos = sum(1 for a in agentes if a.estado == 'muerto')
        print(f"\nAgentes vivos: {vivos} | Escaparon: {escapados} | Bajas: {muertos}")
        
        time.sleep(0.5) # Pausa para ver la animación
        turno_actual += 1
        
    print("\n[+] SIMULACIÓN FINALIZADA.")
    
    # Métricas requeridas por el marco de evaluación
    tasa_supervivencia = (escapados / len(agentes)) * 100
    print(f"Tasa de Supervivencia: {tasa_supervivencia:.2f}%")