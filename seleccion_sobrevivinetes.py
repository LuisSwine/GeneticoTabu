"""
MODULO SELECCION DE SOBREVIVIENTES

Descripción: En este módulo se define la estrategia de selección de sobrevivientes, que si bien pueden ser las
mismas que para la selección de padres, cuando se busca un algoritmo rápido y discriminante se recomienda 
utilizar una estrategia elitista o por extinción

"""

#Definimos la estrategia de selección de sobrevivientes la cuál será una estrategia elitista
def seleccion_por_extincion(poblacion, tamano_seleccion):

    #Ordenamos la población de mayor a menor
    sorted_population = []

    sorted_population = sorted(poblacion, key = lambda x: x.fitness, reverse=True)

    #Retornamos únicamente a los primeros que quepan en el tamaño de población original
    new_population = sorted_population[:tamano_seleccion]

    return new_population