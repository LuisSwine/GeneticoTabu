def generar_vecindario_swap(vector):
    vecindario = []
    n = len(vector)

    for i in range(n - 1):
        for j in range(i + 1, n):
            vecino = vector.copy()
            # Aplicar el operador Swap
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecindario.append(vecino)

    return vecindario

def generar_vecindario_insercion(vector):
    vecindario = []
    n = len(vector)

    for i in range(n):
        for j in range(n):
            if i != j:
                vecino = vector.copy()
                # Eliminar el elemento en la posición i
                elemento = vecino.pop(i)
                # Insertar el elemento en la posición j
                vecino.insert(j, elemento)
                vecindario.append(vecino)

    return vecindario

def generar_vecindario_inversion(vector):
    vecindario = []
    n = len(vector)

    for i in range(n - 1):
        for j in range(i + 1, n):
            vecino = vector.copy()
            # Invertir el orden de los elementos entre i y j
            vecino[i:j + 1] = reversed(vecino[i:j + 1])
            vecindario.append(vecino)

    return vecindario

def generar_vecindario_desplazamiento(vector):
    vecindario = []
    n = len(vector)

    for i in range(n):
        for j in range(n):
            if i != j:
                vecino = vector.copy()
                # Realizar el desplazamiento de un elemento desde la posición i hasta la posición j
                elemento = vecino.pop(i)
                vecino.insert(j, elemento)
                vecindario.append(vecino)

    return vecindario