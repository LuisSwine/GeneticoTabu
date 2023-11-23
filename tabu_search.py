import funcion

#Implementamos la busqueda tabu
def tabu_search(solucion_inicial, tabu_length, monto_objetivo, vector_candidatos, global_solution):
    current_solution = solucion_inicial.copy()
    best_solution = current_solution
    #best_fitness = funcion(current_solution, suma)
    best_fitness = funcion.calidad_candidato(monto_objetivo, current_solution, vector_candidatos)
    tabu_list = []
    criterio = True
    iteracion = 0

    while criterio:
        print(f"Iteracion {iteracion}")
        iteracion += 1
        print(f"Mejor fitness {best_fitness}")
        print(f"Mejor solution {best_solution}")

        #TODO: Mejorar la generación de vecindario
        vecinos = []
        for i in range(len(current_solution)):
          # Generamos un vecino cambiando el bit en la posición i.
          nuevo_vector = current_solution.copy()
          nuevo_vector[i] = not nuevo_vector[i]
          vecinos.append(nuevo_vector)

        # Seleccione el mejor vecino que no esté en la lista tabú
        best_neighbor = None
        best_neighbor_fitness =  float('-inf')
        for neighbor in vecinos:
            # neighbor_fitness = funcion(neighbor, suma)
            neighbor_fitness = funcion.calidad_candidato(monto_objetivo, current_solution, vector_candidatos)
            best_neighbor = neighbor
            best_neighbor_fitness = neighbor_fitness
            

        # Actualiza la solución actual y la mejor solución
        current_solution = best_neighbor
        current_fitness = best_neighbor_fitness
        best_solution = current_solution
        best_fitness = current_fitness
        

        # Agrega la solución actual a la lista tabú
        tabu_list.append(current_solution)
        # Elimina las soluciones antiguas de la lista tabú
        if len(tabu_list) > tabu_length:
            tabu_list.pop(0)

        if best_fitness == global_solution or iteracion == 1000: criterio = False

    return best_solution, best_fitness, iteracion