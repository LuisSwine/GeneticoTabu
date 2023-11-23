import random

def uniform_selection(tam_poblacion):
    indices = []
    for i in range(tam_poblacion):
        indice_padre = random.randint(0, tam_poblacion-1)
        indices.append(indice_padre)
    return indices

def seleccion_sobrevivientes_torneo(poblacion, emparejamiento, max_min):
    indices = []
    while len(indices) < len(poblacion):
        top = len(poblacion) - 1
        subconjunto = random.sample(range(0, top), emparejamiento)

        indice_mejor = subconjunto[0]
        for i in range(1, len(subconjunto)):
            if max_min == 1 and poblacion[i].fitness > poblacion[indice_mejor].fitness:
                indice_mejor = i
            elif max_min == 2 and poblacion[i].fitness < poblacion[indice_mejor].fitness:
                indice_mejor = i

        indices.append(indice_mejor)

    return indices