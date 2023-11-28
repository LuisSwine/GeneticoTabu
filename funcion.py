#Primero creamos la funcion de aptitud para evaluar a los candidatos
def calidad_candidato(monto_objetivo, vector_binario, vector_candidatos):
    sumatoria = 0 #Inicializamos el sumador para llevar la suma de los montos de los movimientos candidatos

    #Iteramos sobre el vector candidato llevando la sumatoria de los montos
    for i in range(len(vector_candidatos)):
        if vector_binario[i] == 1:
            sumatoria += vector_candidatos[i].monto

    #Dividimos 1 sobre la suma del valor absoluto de la diferencia del monto objetivo y la suma, más 1.
    dividendo = abs(monto_objetivo - sumatoria) + 1 

    return 1 / dividendo

"""
El más uno del denominador se decidió añadir por dos razones:
-Para evitar que los resultados obtenidos de esta función sean mayores a 1, lo que permite utilizar un enfoque de maximización
 con 1 como valor objetivo.
-Para no tener que lidiar con el problema de la división entre 0.
"""