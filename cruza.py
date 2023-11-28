#IMPORTAMOS LAS LIBRERIAS NECESARIAS
import random

#DEFINIMOS LAS DIFERENTES ESTRATEGIAS DE CRUZA QUE PODRÍAMOS UTILIZAR
def cruza_dos_puntos(parent1, parent2):
    # Asegúrate de que los cromosomas tengan la misma longitud
    assert len(parent1) == len(parent2), "Los cromosomas deben tener la misma longitud"

    # Selecciona dos puntos de corte aleatorios
    point1 = random.randint(0, len(parent1) - 1)
    point2 = random.randint(point1, len(parent1) - 1)

    # Realiza la cruza en los puntos de corte
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

    return child1, child2

def cruza_de_posicion_fija(parent1, parent2, fixed_position):
    # Asegúrate de que los cromosomas tengan la misma longitud
    assert len(parent1) == len(parent2), "Los cromosomas deben tener la misma longitud"

    # Realiza la cruza de posición fija
    child1 = parent1[:fixed_position] + parent2[fixed_position:]
    child2 = parent2[:fixed_position] + parent1[fixed_position:]

    return child1, child2