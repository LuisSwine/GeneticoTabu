"""
MODULO ALGORITMO HIBRIDO

Descripción: En este modulo se definen los siguientes métodos o funciones:
-Requerimiento de paro: evalua el estado del algoritmo en cada iteración para determinar si parar o continuar
-Algoritmo híbrido entre algoritmo genético y búsqueda tabú

"""

#PRIMERO IMPORTAMOS LOS MODULOS PERSONALIZADOS
import poblacion
import cromosoma
import seleccion_padres
import seleccion_sobrevivinetes
import cruza
import mutacion
import tabu_search

#Definimos e implementamos la funcion de parada
def stop_requeriment(global_solution, best_child):
    #Evaluamos la funcion
    result = best_child.fitness

    #Evaluamos la diferencia
    if global_solution == result: return False
    else: return True

#Definimos el algortimo genético
def algoritmoGeneticoHibrido(tam_poblacion, porcentaje_mutacion, global_solution, monto_objetivo, vector_movimientos):

    #PRIMERO GENERAMOS LA POBLACION INICIAL
    poblacion_inicial = poblacion.Poblacion(tam_poblacion, vector_movimientos, monto_objetivo) #Instanciamos un objeto de la clase población
    poblacion_inicial.inicializarPoblacionHeuristic() #Utilizamos el método correspondiente para inicializar la población
    poblacion_inicial.setAllFitness() #Asigamos la aptitud de cada uno de los individuos de la población

    #CREAMOS LOS LISTADOS DE CONTROL
    mejores = []
    peores = []
    promedio = []

    #Obtenemos y registramos el mejor, peor y el promedio de los individuos
    mejores.append(poblacion_inicial.getMax())
    peores.append(poblacion_inicial.getMin())
    promedio.append(poblacion_inicial.getProm())

    #Creamos el criterio de paro y el iterador de generaciones
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

    #Mientras no se cumpla alguno de los criterior de parada
    while compare:
        #Imprimimos la generacion en la que vamos
        print(f"Generacion {generacion}")
        global_best_solution = mejores[-1].vector_solution #Registramos la mejor solucion global
        generacion += 1 #Actualizamos la generación 

        #Hacemos la seleccion de los indices de los padres mediante la estrategia seleccionada
        indices_padres = seleccion_padres.uniform_selection(tam_poblacion)
        #indices_padres = seleccion_sobrevivientes_torneo(poblacion_inicial.poblacion, 10, max_min)

        #APLICAMOS LA CRUZA
        hijos = [] #Creamos un vector para almacenar temporalmente los hijos
        for i in range(0, len(indices_padres) - 1, 2):
            #Seleccionamos a los padres de la población con base en los indices indicados
            padre1 = poblacion_inicial.poblacion[i].vector_solution
            padre2 = poblacion_inicial.poblacion[i+1].vector_solution

            #hijo1, hijo2 = cruza.orderBasedCrossover(padre1, padre2, (numeros // 2))
            #Creamos dos vectores hijos nuevos que guardaremos en el vector hijos
            hijo1, hijo2 = cruza.cruza_dos_puntos(padre1, padre2)
            hijos.append(hijo1)
            hijos.append(hijo2)

        #Convertimos cada vector hijo en un objeto de la clase cromosoma para acceder a todos sus atributos
        cromosomas_hijos = [] #Creamos una lista temporal para guardar los cromosomas hijos
        for hijo in hijos:
            new_hijo = cromosoma.Cromosoma() #Instanciamos un objeto de la clase cromosoma
            new_hijo.vector_solution = hijo #Asignamos el vector del hijo al vector solucion del objeto creado
            cromosomas_hijos.append(new_hijo) #Añadimos las nuevas instancias a la lista

        #Ahora aplicamos la mutación a cada hijo
        for hijo in cromosomas_hijos:
            #Ahora aplicamos la mutacion
            #mutated = mutacionHeuristica(hijo.vector_solution, porcentaje_mutacion, funcion, suma, poblacion_inicial.corte, max_min)
            mutated = mutacion.mutacion_probabilistica(hijo.vector_solution, porcentaje_mutacion)
            
            #Asignamos el valor mutado al cromosoma
            hijo.vector_solution = mutated
            
            #Calculamos el fitness de cada hijo
            hijo.evaluateFunction(monto_objetivo, vector_movimientos)
            
            #Agregamos los hijos mutados  a la poblacion
            poblacion_inicial.poblacion.append(hijo)

        #SELECCIONAMOS A LOS SOBREVIVIENTES
        poblacion_inicial.poblacion = seleccion_sobrevivinetes.seleccion_por_extincion(poblacion_inicial.poblacion, tam_poblacion)

        mejores.append(poblacion_inicial.getMax())
        peores.append(poblacion_inicial.getMin())
        promedio.append(poblacion_inicial.getProm())

        #Validamos o contamos los estancamientos
        if last_best == mejores[-1].fitness and last_worst == peores[-1].fitness:
            iterador_maxmin_local += 1
            print(f"Lleva estancado {iterador_maxmin_local} iteraciones")
        else: iterador_maxmin_local = 0

        #Actualizamos el último mejor y el útimo peor antes de actualizar los valores 
        last_best = mejores[-1].fitness
        last_worst = peores[-1].fitness

        iteraciones_tabu = 0
        #Validamos si conviene entrar a la búsqueda tabú
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

        #Verficamos el criterio de parada
        compare = stop_requeriment(global_solution, mejores[-1])
        
    return global_best_solution, global_best_fitness, global_worst_fitness, generacion, iteraciones_tabu
