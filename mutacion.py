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