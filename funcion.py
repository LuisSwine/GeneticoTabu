#Primero creamos la funcion de aptitud para evaluar a los candidatos
def calidad_candidato(monto_objetivo, vector_binario, vector_candidatos):
    sumatoria = 0

    for i in range(len(vector_candidatos)):
        if vector_binario[i] == 1:
            sumatoria += vector_candidatos[i].monto

    dividendo = abs(monto_objetivo - sumatoria) + 1 

    return 1 / dividendo