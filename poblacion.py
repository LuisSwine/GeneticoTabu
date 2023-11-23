import cromosoma

#Creamos la clase poblacion
class Poblacion:
    def __init__(self, tam_poblacion, lista_movimientos, monto_objetivo):

        self.lista_movimientos = lista_movimientos
        self.monto_objetivo = monto_objetivo

        self.poblacion = [] #Lista de individuos o cromosomas
        self.tam_poblacion = tam_poblacion #Cantidad de individuos de la poblacion

    def inicializarPoblacion(self):
        self.poblacion = []

        for _ in range(self.tam_poblacion):
            new_cromosoma = cromosoma.Cromosoma()
            new_cromosoma.randomInitialization(self.lista_movimientos)
            self.poblacion.append(new_cromosoma)
        pass

    def printPoblacion(self):
        for individuo in self.poblacion:
            individuo.printCromosoma()

    def setAllFitness(self):
        for individuo in self.poblacion:
            #Evaluamos la funcion
            individuo.evaluateFunction(self.monto_objetivo, self.lista_movimientos)
            
        pass

    def getMin(self):
        #Primero asignamos todos los fitness a cada cromosoma
        poblacion_ordenada = sorted(self.poblacion, key= lambda x: x.fitness)
        best = poblacion_ordenada[0]
        return best

    def getMax(self):
        #Primero asignamos todos los fitness a cada cromosoma
        poblacion_ordenada = sorted(self.poblacion, key= lambda x: x.fitness)
        best = poblacion_ordenada[-1]
        return best

    def getProm(self):
        sumatoria = 0
        for individuo in self.poblacion:
            sumatoria += individuo.fitness
        prom = sumatoria / len(self.poblacion)
        return prom