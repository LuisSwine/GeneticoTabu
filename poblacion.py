#Importamos el modulo personalizado de cromosoma para utilizar la clase
import cromosoma

#Creamos la clase poblacion
class Poblacion:
    #Definimos el método constructor de la clase
    def __init__(self, tam_poblacion, lista_movimientos, monto_objetivo):

        self.lista_movimientos = lista_movimientos #Almacenará la lista original de movimientos del espacio de busqueda
        self.monto_objetivo = monto_objetivo #Almacena el monto de la factura que será el monto objetivo

        self.poblacion = [] #Lista de individuos o cromosomas
        self.tam_poblacion = tam_poblacion #Cantidad de individuos de la poblacion

    #Definimos el método para inicializar la población
    def inicializarPoblacion(self):
        self.poblacion = [] #Creamos una lista vacia para almacenar los cromosomas de la poblacion

        #Para cada elemento de la poblacion
        for _ in range(self.tam_poblacion):
            new_cromosoma = cromosoma.Cromosoma() #Instanciamos un objeto de la clase cromosoma
            new_cromosoma.randomInitialization(self.lista_movimientos) #Inicializamos los valores del objeto
            self.poblacion.append(new_cromosoma) #Añadimos el objeto a la población
        pass

    #Definimos un método para imprimir los cromosomas de la población 
    def printPoblacion(self):
        #Para cada individuo de la población invocamos el método que imprime sus valores
        for individuo in self.poblacion:
            individuo.printCromosoma()

    #Definimos un método que permite actualizar la aptitud de todos los individuos de la población cuando sea necesario
    def setAllFitness(self):
        for individuo in self.poblacion:
            #Evaluamos la funcion
            individuo.evaluateFunction(self.monto_objetivo, self.lista_movimientos)
        pass

    #Definimos un método para extraer al individuo con la menor aptitud (puede ser el mejor o peor dependiendo del enfoque de maximizar o minimizar)
    def getMin(self):
        #Primero asignamos todos los fitness a cada cromosoma y los ordenamos de menor a mayor
        poblacion_ordenada = sorted(self.poblacion, key= lambda x: x.fitness)
        #Extraemos el primer elemento y lo retornamos
        best = poblacion_ordenada[0]
        return best

    #Definimos un método para extraer al individuo con la mayor aptitud (puede ser el mejor o peor dependiendo del enfoque de maximizar o minimizar)
    def getMax(self):
        #Primero asignamos todos los fitness a cada cromosoma y los ordenamos de menor a mayor
        poblacion_ordenada = sorted(self.poblacion, key= lambda x: x.fitness)
        #Extraemos el último elemento y lo retornamos
        best = poblacion_ordenada[-1]
        return best

    #Definimos un método para obtener el promedio de los valores de aptitud de los individuos de la población
    def getProm(self):
        sumatoria = 0 #Inicializamos la sumatoria
        #Para cada individuo
        for individuo in self.poblacion:
            #Extraemos la aptitud y la sumamos
            sumatoria += individuo.fitness
        #Dividimos la suma de aptitudes entre el tamaño de la población
        prom = sumatoria / len(self.poblacion)
        #Retornamos el promedio de aptitud
        return prom