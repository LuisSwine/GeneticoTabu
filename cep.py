#Definimos la clase CEP donde rescataremos la información principal de los Comprobantes Electrónicos de Pago
class CEP:
    fecha = None
    clave_rastreo = None
    monto = None
    iva = None
    concepto = None
    rfc_receptor = None
    nombre_receptor = None
    cuenta_receptor = None
    banco_receptor = None
    rfc_emisor = None
    nombre_emisor = None
    cuenta_emisor = None
    banco_emisor = None
    
    #Declaramos el contructor de la clase para crear las instacias u objetos
    def __init__(self, fecha, clave_rastreo, monto, iva, concepto, rfc_receptor, nombre_receptor, cuenta_receptor, banco_receptor, rfc_emisor, nombre_emisor, cuenta_emisor, banco_emisor):
        self.fecha = fecha
        self.clave_rastreo = clave_rastreo
        self.monto = monto
        self.iva = iva
        self.concepto = concepto
        self.rfc_receptor = rfc_receptor
        self.nombre_receptor = nombre_receptor
        self.cuenta_receptor = cuenta_receptor
        self.banco_receptor = banco_receptor
        self.rfc_emisor = rfc_emisor
        self.nombre_emisor = nombre_emisor
        self.cuenta_emisor = cuenta_emisor
        self.banco_emisor = banco_emisor
        pass