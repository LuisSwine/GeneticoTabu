"""
CLASE MODULO DE SELECCION DE PADRES

Descripción: Este módulo integra los diferentes métodos o estrategias que pueden implementarse en el algoritmo
genético para realizar la selección de los padres que se cruzaran para la siguiente generación o iteración.

"""
#PRIMERO IMPORTAMOS LAS BIBLIOTECAS NECESARIAS
import random

#DEFINIMOS LAS DIFERENTES ESTRATEGIAS DE SELECCION DE PADRES

#FUNCIÓN DE SELECCION UNIFORME
def uniform_selection(tam_poblacion):
    indices = [] #Inicializamo un vector para poder guardar los indices de los padres seleccionados
    #Hasta alcanzar la cantidad de indices equivalente al tamaño de la población
    for i in range(tam_poblacion):
        #Seleccionamos un numero aleatorio entre 0 y el tamaño de la población menos 1 
        indice_padre = random.randint(0, tam_poblacion-1)
        #Añadimos el indice seleccionado al vector
        indices.append(indice_padre)
        
    #Retornamos el vector de indices
    return indices

def seleccion_por_ruleta(poblacion):
    #Extraemos la lista de aptitudes
    aptitudes = [individuo.fitness for individuo in poblacion]
    
    # Calcula la suma total de las aptitudes
    suma_aptitudes = sum(aptitudes)

    # Calcula las probabilidades de selección para cada individuo
    probabilidades = [aptitud / suma_aptitudes for aptitud in aptitudes]

    # Realiza la selección de padres por ruleta
    padres_seleccionados = random.choices(poblacion, weights=probabilidades, k=len(poblacion))

    return padres_seleccionados


#Seleccion mediante torneo
def seleccion_sobrevivientes_torneo(poblacion, emparejamiento, max_min):
    indices = [] #Inicializamos un vector de indices 
    #Mientras seleccionamos suficientes indices para equiparar el tamaño de la población
    while len(indices) < len(poblacion):
        #Seleccionamos un subconjunto de tamaño 'emparejamiento'
        top = len(poblacion) - 1
        subconjunto = random.sample(range(0, top), emparejamiento)

        #Del subcojunto vamos a obtener a aquerl que tiene la mejor aptitud
        indice_mejor = subconjunto[0]
        for i in range(1, len(subconjunto)):
            if max_min == 1 and poblacion[i].fitness > poblacion[indice_mejor].fitness:
                indice_mejor = i
            elif max_min == 2 and poblacion[i].fitness < poblacion[indice_mejor].fitness:
                indice_mejor = i

        #Añadimos el mejor padre a la lista de indices
        indices.append(indice_mejor)

    #Retornamos los indices seleccionados
    return indices