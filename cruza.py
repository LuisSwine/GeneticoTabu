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

def cruza_en_un_punto(padre1, padre2):
    
    # Asegurarse de que los padres tengan la misma longitud
    assert len(padre1) == len(padre2), "Los padres deben tener la misma longitud"

    # Seleccionar un punto de cruce aleatorio
    punto_de_cruce = random.randint(0, len(padre1) - 1)

    # Realizar la cruza en un punto
    descendiente1 = padre1[:punto_de_cruce] + padre2[punto_de_cruce:]
    descendiente2 = padre2[:punto_de_cruce] + padre1[punto_de_cruce:]

    return descendiente1, descendiente2

def cruza_uniforme(padre1, padre2, probabilidad_cruza):
   
    # Asegurarse de que los padres tengan la misma longitud
    assert len(padre1) == len(padre2), "Los padres deben tener la misma longitud"

    # Realizar la cruza uniforme
    descendiente1 = [gen1 if random.random() < probabilidad_cruza else gen2 for gen1, gen2 in zip(padre1, padre2)]
    descendiente2 = [gen1 if random.random() < probabilidad_cruza else gen2 for gen1, gen2 in zip(padre1, padre2)]

    return descendiente1, descendiente2

def cruza_de_posicion_fija(parent1, parent2, fixed_position):
    # Asegúrate de que los cromosomas tengan la misma longitud
    assert len(parent1) == len(parent2), "Los cromosomas deben tener la misma longitud"

    # Realiza la cruza de posición fija
    child1 = parent1[:fixed_position] + parent2[fixed_position:]
    child2 = parent2[:fixed_position] + parent1[fixed_position:]

    return child1, child2

def cruza_por_orden(padre1, padre2):
    
    # Asegurarse de que los padres tengan la misma longitud
    assert len(padre1) == len(padre2), "Los padres deben tener la misma longitud"

    # Seleccionar dos puntos de cruce aleatorios
    punto1 = random.randint(0, len(padre1) - 1)
    punto2 = random.randint(0, len(padre1) - 1)

    # Asegurarse de que los puntos de cruce sean distintos
    while punto1 == punto2:
        punto2 = random.randint(0, len(padre1) - 1)

    # Ordenar los puntos de cruce
    punto_inicio = min(punto1, punto2)
    punto_fin = max(punto1, punto2)

    # Extraer los segmentos entre los puntos de cruce de ambos padres
    segmento_padre1 = padre1[punto_inicio:punto_fin + 1]
    segmento_padre2 = padre2[punto_inicio:punto_fin + 1]

    # Inicializar los descendientes con los segmentos extraídos
    descendiente1 = [-1] * len(padre1)
    descendiente2 = [-1] * len(padre2)

    descendiente1[punto_inicio:punto_fin + 1] = segmento_padre1
    descendiente2[punto_inicio:punto_fin + 1] = segmento_padre2

    # Completar los descendientes con los elementos no seleccionados
    idx1 = punto_fin + 1
    idx2 = punto_fin + 1

    for i in range(len(padre1)):
        if padre2[(punto_fin + 1 + i) % len(padre2)] not in segmento_padre1:
            descendiente1[idx1 % len(padre1)] = padre2[(punto_fin + 1 + i) % len(padre2)]
            idx1 += 1

        if padre1[(punto_fin + 1 + i) % len(padre1)] not in segmento_padre2:
            descendiente2[idx2 % len(padre2)] = padre1[(punto_fin + 1 + i) % len(padre1)]
            idx2 += 1

    return descendiente1, descendiente2

def cruza_de_ciclos(padre1, padre2):
    # Asegurarse de que los padres tengan la misma longitud
    assert len(padre1) == len(padre2), "Los padres deben tener la misma longitud"

    # Inicializar los descendientes con valores nulos
    descendiente1 = [-1] * len(padre1)
    descendiente2 = [-1] * len(padre2)

    # Ciclo de cruza
    ciclo_actual = 0
    while -1 in descendiente1:
        # Seleccionar un padre alternando entre padre1 y padre2
        padre_actual = padre1 if ciclo_actual % 2 == 0 else padre2

        # Encontrar el primer índice no utilizado en el descendiente
        idx = descendiente1.index(-1)

        # Copiar el ciclo actual al descendiente
        while descendiente1[idx] == -1:
            descendiente1[idx] = padre_actual[idx]
            descendiente2[idx] = padre_actual[idx]
            idx = padre1.index(padre2[idx])

        # Pasar al siguiente ciclo
        ciclo_actual += 1

    return descendiente1, descendiente2