import random
import funcion

class Cromosoma:
    def __init__(self):
        self.vector_solution = []
        self.fitness = 0

    def randomInitialization(self, lista_movimientos):
        valores = len(lista_movimientos) - 1
        #TODO: Se podría optimizar si solo constará de un movimiento seleccionado al inicio
        self.vector_solution = [0 for _ in lista_movimientos]
        self.vector_solution[random.randint(0, valores)] = 1
        pass

    def setFitness(self, value):
        self.fitness = value

    def evaluateFunction(self, monto_objetivo, lista_movimientos):
        self.fitness = funcion.calidad_candidato(monto_objetivo, self.vector_solution, lista_movimientos)
        pass

    def printCromosoma(self):
        print(f"Datos del cromosoma: \n"
              + f"Vector solucion {self.vector_solution} \n"
              + f"Fitness {self.fitness}")