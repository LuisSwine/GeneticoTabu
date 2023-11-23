import random

def mutacion_probabilistica(vector, probabilidad_mutacion):
    vector_mutado = []

    for bit in vector:
        # Genera un número aleatorio entre 0 y 1
        prob = random.random()

        # Si el número aleatorio es menor que la probabilidad de mutación, realiza la mutación
        if prob < probabilidad_mutacion:
            # Cambia el bit de 0 a 1 o de 1 a 0
            bit_mutado = 1 - bit
        else:
            bit_mutado = bit

        vector_mutado.append(bit_mutado)

    return vector_mutado