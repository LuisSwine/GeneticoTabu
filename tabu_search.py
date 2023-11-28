#Importamos el modulo funcion pues lo utilizaremos
import funcion

#Implementamos la busqueda tabu
def tabu_search(solucion_inicial, tabu_length, monto_objetivo, vector_candidatos, global_solution):
    current_solution = solucion_inicial.copy() #Creamos una copia del vector que se nos pasa como solucion inicial
    best_solution = current_solution #Inicializamos el valor de la mejor solución con la solucion inicial
    
    best_fitness = funcion.calidad_candidato(monto_objetivo, current_solution, vector_candidatos) #Evaluamos la aptitud de la solucion inicial y la asignamos a la mejor aptitud
    tabu_list = [] #Inicializamos en blanco la búsqueda tabú
    criterio = True #Inicializamos el criterio de parada
    iteracion = 0 #Inicializamos el contador de iteraciones 

    #Mientras no se cumpla uno de los criterios de parada
    while criterio:
        #Imprimimos a manera informativa los datos de la iteración
        print(f"Iteracion {iteracion}") 
        iteracion += 1 #Actualizamos el número de iteración
        print(f"Mejor fitness {best_fitness}")
        print(f"Mejor solution {best_solution}")

        #TODO: Mejorar la generación de vecindario
        vecinos = [] #Inicializamos el vector de vecinos del vector solución actual
        #Generamos el vecindario de soluciones
        for i in range(len(current_solution)):
          # Generamos un vecino cambiando el bit en la posición i.
          nuevo_vector = current_solution.copy()
          nuevo_vector[i] = not nuevo_vector[i]
          vecinos.append(nuevo_vector)

        # Seleccionamos el mejor vecino que no esté en la lista tabú
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

        #Actualizamos el valor del criterio de parada verificando que no se haya cumplido alguno de los criterios definidos
        #que son alcanzar el valor objetivo o un limite de iteraciones
        if best_fitness == global_solution or iteracion == 1000: criterio = False

    #Retornamos el mejor vector, su aptitud y el numero de iteraciones ejecutadas. 
    return best_solution, best_fitness, iteracion