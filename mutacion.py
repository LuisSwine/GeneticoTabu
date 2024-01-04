"""
MODULO MUTACION

Descripción: En este módulo se definen los diferentes métodos o estrategias que pueden ser utilizadas para 
aplicar una mutación a las soluciones candidatas hijas que son generadas en el algoritmo genético

"""
#PRIMERO IMPORTAMOS LAS LIBRERÍAS NECESARIAS
import random

#Definimos la estrategia de mutación a utilizar
def mutacion_probabilistica(vector, probabilidad_mutacion):
    vector_mutado = [] #Instanciamos un vector vacío para almacenar el vector mutado resultante

    #Para cada bit del vector
    for bit in vector:
        # Genera un número aleatorio entre 0 y 1
        prob = random.random()

        # Si el número aleatorio es menor que la probabilidad de mutación, realiza la mutación
        if prob < probabilidad_mutacion:
            # Cambia el bit de 0 a 1 o de 1 a 0
            bit_mutado = 1 - bit
        else:
            #Se traslada el bit tal cuál
            bit_mutado = bit

        #Añadimos el bit al vector resultante
        vector_mutado.append(bit_mutado)

    #Retornamos el vector resultante
    return vector_mutado

def mutacion_de_intercambio(vector):
    # Selecciona dos índices distintos aleatorios
    idx1, idx2 = random.sample(range(len(vector)), 2)

    # Realiza el intercambio
    vector_mutado = vector.copy()
    vector_mutado[idx1], vector_mutado[idx2] = vector_mutado[idx2], vector_mutado[idx1]

    return vector_mutado

def mutacion_de_insercion(vector):
    
    # Selecciona dos índices distintos aleatorios
    idx1, idx2 = random.sample(range(len(vector)), 2)

    # Elimina el elemento en idx1
    elemento = vector.pop(idx1)

    # Inserta el elemento en idx2
    vector.insert(idx2, elemento)

    return vector

def mutacion_por_inversion(vector):
    
    # Selecciona dos índices distintos aleatorios
    idx1, idx2 = random.sample(range(len(vector)), 2)

    # Asegúrate de que idx1 sea menor que idx2
    if idx1 > idx2:
        idx1, idx2 = idx2, idx1

    # Invierte la sublista entre idx1 e idx2
    vector_mutado = vector[:idx1] + list(reversed(vector[idx1:idx2 + 1])) + vector[idx2 + 1:]

    return vector_mutado