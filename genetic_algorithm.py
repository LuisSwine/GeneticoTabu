import poblacion
import cromosoma
import seleccion_padres
import seleccion_sobrevivinetes
import cruza
import mutacion
import tabu_search

#Implementamos la funcion de parada
def stop_requeriment(global_solution, best_child):
    #Evaluamos la funcion
    result = best_child.fitness

    #Evaluamos la diferencia
    if global_solution == result: return False
    else: return True

def algoritmoGeneticoHibrido(tam_poblacion, porcentaje_mutacion, global_solution, monto_objetivo, vector_movimientos):

    #PRIMERO GENERAMOS LA POBLACION INICIAL
    poblacion_inicial = poblacion.Poblacion(tam_poblacion, vector_movimientos, monto_objetivo)
    poblacion_inicial.inicializarPoblacion()
    poblacion_inicial.setAllFitness()

    #CREAMOS LOS LISTADOS DE CONTROL
    mejores = []
    peores = []
    promedio = []

    mejores.append(poblacion_inicial.getMax())
    peores.append(poblacion_inicial.getMin())
    promedio.append(poblacion_inicial.getProm())

    #Creamos el criterio de paro y el iterados de generaciones
    compare = True
    generacion = 0

    #Iniciamos un contador en 0 para saber cuando llevamos mucho tiempo estabcados
    iterador_maxmin_local = 0
    last_best = 0
    last_worst = 0

    #Instanciamos las variables totales
    global_worst_fitness = mejores[-1].fitness
    global_best_fitness = peores[-1].fitness
    
    global_best_solution = []

    while compare:
        #Imprimimos la generacion en la que vamos
        global_best_solution = mejores[-1].vector_solution  
        print(f"Generacion {generacion}")
        generacion += 1

        #Hacemos la seleccion de padres
        indices_padres = seleccion_padres.uniform_selection(tam_poblacion)
        #indices_padres = seleccion_sobrevivientes_torneo(poblacion_inicial.poblacion, 10, max_min)

        #APLICAMOS LA CRUZA
        hijos = []
        for i in range(0, len(indices_padres) - 1, 2):
            padre1 = poblacion_inicial.poblacion[i].vector_solution
            padre2 = poblacion_inicial.poblacion[i+1].vector_solution

            #hijo1, hijo2 = cruza.orderBasedCrossover(padre1, padre2, (numeros // 2))
            hijo1, hijo2 = cruza.cruza_dos_puntos(padre1, padre2)
            hijos.append(hijo1)
            hijos.append(hijo2)

        #Convertimos cada vector hijo en un objeto de la clase cromosoma para acceder a todos sus atributos
        cromosomas_hijos = []
        for hijo in hijos:
            new_hijo = cromosoma.Cromosoma()
            new_hijo.vector_solution = hijo
            cromosomas_hijos.append(new_hijo)

        #Ahora aplicamos la mutación a cada hijo
        for hijo in cromosomas_hijos:
            #Ahora aplicamos la mutacion
            #mutated = mutacionHeuristica(hijo.vector_solution, porcentaje_mutacion, funcion, suma, poblacion_inicial.corte, max_min)
            mutated = mutacion.mutacion_probabilistica(hijo.vector_solution, porcentaje_mutacion)
            
            #Asignamos el valor mutado al cromosoma
            hijo.vector_solution = mutated
            
            #Por ultimo ajusramos la mutacion para el cromosoma no quede fuera de los parametros
            #Calculamos el fitness de cada hijo
            hijo.evaluateFunction(monto_objetivo, vector_movimientos)
            hijo.printCromosoma()
            
            #Agregamos los hijos mutados y ajustados a la poblacion
            poblacion_inicial.poblacion.append(hijo)

        #SELECCIONAMOS A LOS SOBREVIVIENTES
        poblacion_inicial.poblacion = seleccion_sobrevivinetes.seleccion_por_extincion(poblacion_inicial.poblacion, tam_poblacion)

        mejores.append(poblacion_inicial.getMax())
        peores.append(poblacion_inicial.getMin())
        promedio.append(poblacion_inicial.getProm())

        # print(f"Promedio: {promedio[-1]} Peor: {peores[-1].fitness} Mejor: {mejores[-1].fitness}")

        #Validamos o contamos los estancamientos
        if last_best == mejores[-1].fitness and last_worst == peores[-1].fitness:
            iterador_maxmin_local += 1
            print(f"Lleva estancado {iterador_maxmin_local} iteraciones")
        else: iterador_maxmin_local = 0

        last_best = mejores[-1].fitness
        last_worst = peores[-1].fitness

        iteraciones_tabu = 0
        if iterador_maxmin_local == 1000:
            input('Pasando a Busqueda tabu')
            global_best_solution = mejores[-1].vector_solution
            iterador_maxmin_local = 0
            #Rompemos el ciclo pero primero iniciamos la busqueda local
            global_best_solution, global_best_fitness, iteraciones_tabu = tabu_search.tabu_search(
                global_best_solution,
                60,
                monto_objetivo,
                vector_movimientos,
                global_solution,
                )
            
            mejores.append(global_best_solution)
            break

        compare = stop_requeriment(global_solution, mejores[-1])
        
    return global_best_solution, global_best_fitness, global_worst_fitness, generacion, iteraciones_tabu
