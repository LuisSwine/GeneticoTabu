import random
import funcion

#Definimos la clase Cromosoma
class Cromosoma:
    def __init__(self):
        self.vector_solution = [] #Vector binario que almacena la combinatoria de movimientos candidata
        self.fitness = 0          #Aptitud del candidato obtenida de evaluar el vector en la función

    """ 
    Método que inicializa de forma aletaoria cada uno de los vectores candidatos:
    Para fines prácticos se ha decidido que al momento de inicializar la población únicamente se seleccione
    un solo movimiento de la lista de movimiento para iniciar
    """
    def randomInitialization(self, lista_movimientos):
        valores = len(lista_movimientos) - 1 #Definimos la ultima posición de cada vector
        self.vector_solution = [0 for _ in lista_movimientos] #Inicializamos el vector con puros 0's
        self.vector_solution[random.randint(0, valores)] = 1 #De forma aleatoria convertimos uno de los 0 a 1, seleccionando ese movimiento
        pass

    """
    Método creado únicamente para asignar la aptitud al atributo del objeto
    """
    def setFitness(self, value):
        self.fitness = value

    """
    Método que evalua la función de aptitud y asigna el resultado a la aptitud del objeto
    """
    def evaluateFunction(self, monto_objetivo, lista_movimientos):
        self.fitness = funcion.calidad_candidato(monto_objetivo, self.vector_solution, lista_movimientos)
        pass

    """
    Método para imprimir los valores del vector candidato y su aptitud
    """
    def printCromosoma(self):
        print(f"Datos del cromosoma: \n"
              + f"Vector solucion {self.vector_solution} \n"
              + f"Fitness {self.fitness}")