"""
CLASE FACTURA

Descripción: Clase que almacena los datos más relevantes de la factura extraídos de cada registro y define
los mmétodos útiles de la clase

"""

#Definimos la clase factura donde guardaremos los datos importantes de la factura
class Factura:
    uuid = None
    nombre_receptor = None
    rfc_receptor = None
    nombre_emisor = None
    rfc_emisor = None
    fecha_emision = None
    monto = None
    metodo_pago = None
    vigencia = None
    divisa = None
        
    #Definimos el constructor de la clase
    def __init__(self, uuid, nombre_receptor, rfc_receptor, nombre_emisor, rfc_emisor, fecha_emision, monto, metodo_pago, vigencia, divisa):
        self.uuid = uuid
        self.nombre_receptor = nombre_receptor
        self.rfc_receptor = rfc_receptor
        self.nombre_emisor = nombre_emisor
        self.rfc_emisor = rfc_emisor
        self.fecha_emision = fecha_emision
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.vigencia = vigencia
        self.divisa = divisa
        pass
    
    #Definimos un método para imprimir los valores del objeto
    def showFactura(self):
        print("UUID de la factura: ", self.uuid)
        print("Nombre del receptor: ", self.nombre_receptor)
        print("RFC del receptor: ", self.rfc_receptor)
        print("Nombre del emisor: ", self.nombre_emisor)
        print("RFC del emisor: ", self.rfc_emisor)
        print("Fecha de emisión: ", self.fecha_emision)
        print("Monto: ", self.monto)
        print("Método de pago: ", self.metodo_pago)
        print("Vigencia: ", self.vigencia)
        print("Divisa: ", self.divisa)
        pass
    