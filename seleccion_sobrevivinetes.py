def seleccion_por_extincion(poblacion, tamano_seleccion):

    sorted_population = []

    sorted_population = sorted(poblacion, key = lambda x: x.fitness, reverse=True)

    new_population = sorted_population[:tamano_seleccion]

    return new_population