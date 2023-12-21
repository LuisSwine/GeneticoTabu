import pandas as pd
import secrets
import string
import random
import datetime

import factura
import movimiento
import cep

def generar_fecha_aleatoria(anio_inicio, anio_fin):
    # Calcular el número total de días en el período
    dias_totales = (datetime.date(anio_fin, 12, 31) - datetime.date(anio_inicio, 1, 1)).days

    # Seleccionar un día aleatorio en el período
    dias_aleatorios = random.randint(0, dias_totales)

    # Calcular la fecha aleatoria
    fecha_aleatoria = datetime.date(anio_inicio, 1, 1) + datetime.timedelta(days=dias_aleatorios)

    return fecha_aleatoria

def generar_cadena_aleatoria(longitud=32):
    alfabeto = string.ascii_letters + string.digits
    cadena_aleatoria = ''.join(secrets.choice(alfabeto) for _ in range(longitud))
    return cadena_aleatoria

class Empresa:
    def __init__(self, nombre_empresa, rfc):    
        self.nombre_empresa = nombre_empresa
        self.rfc = rfc
        pass


    
lista_tipo_movimiento = ['Ingreso', 'Ingreso interbancario', 'Egreso', 'Egreso interbancario']
    
#Definimos las empresas identificadas en el conjunto de datos
lista_empresas_sistema = []
lista_empresas_externas = []
lista_metodos_pago = ['PUE', 'PPD']

empresa = Empresa('C**** S****S****', 'CSS010101**0')
lista_empresas_sistema.append(empresa)
empresa = Empresa('O**** S****E****', 'EBT010101**6')
lista_empresas_sistema.append(empresa)
empresa = Empresa('S**** B****F****', 'SBF010101**0')
lista_empresas_sistema.append(empresa)


empresa = Empresa('A**** E****F****', 'FOR010101**A')
lista_empresas_externas.append(empresa)
empresa = Empresa('C**** I****C****', 'CIC010101**5')
lista_empresas_externas.append(empresa)
empresa = Empresa('D****', 'RIV010101**6')
lista_empresas_externas.append(empresa)
empresa = Empresa('E**** B****T****', 'EBT010101**6')
lista_empresas_externas.append(empresa)
empresa = Empresa('F****', 'LUA010101**2')
lista_empresas_externas.append(empresa)
empresa = Empresa('G**** A****G****', 'GOR010101**6')
lista_empresas_externas.append(empresa)
empresa = Empresa('J**** M****C****', 'CAM010101**4')
lista_empresas_externas.append(empresa)
empresa = Empresa('J**** M****D****', 'JMA010101**0')
lista_empresas_externas.append(empresa)
empresa = Empresa('L****', 'MAA010101**7')
lista_empresas_externas.append(empresa)
empresa = Empresa('M****', 'MOA010101**5')
lista_empresas_externas.append(empresa)
empresa = Empresa('M**** M****A****', 'VIC010101**1')
lista_empresas_externas.append(empresa)
empresa = Empresa('M**** N****O****', 'OIS010101**X')
lista_empresas_externas.append(empresa)
empresa = Empresa('O**** S****D****', 'OPE010101**4')
lista_empresas_externas.append(empresa)
empresa = Empresa('P**** D****F****', 'FUT010101**X')
lista_empresas_externas.append(empresa)
empresa = Empresa('P**** Y****D****', 'PDO010101**2')
lista_empresas_externas.append(empresa)
empresa = Empresa('R****', 'SUL010101**4')
lista_empresas_externas.append(empresa)
empresa = Empresa('S**** P****A****', 'SIN010101**4')
lista_empresas_externas.append(empresa)
empresa = Empresa('U**** I****A****', 'UIB010101**3')
lista_empresas_externas.append(empresa)
empresa = Empresa('Y**** L****R****', 'LER010101**7')
lista_empresas_externas.append(empresa)

nuevas_facturas_cxc = []

#PROCEDEMOS A GENERAR FACTURAS POR COBRAR DE FORMA ALEATORIA
for i in range(10):
    
    indice_empresa = random.randint(0, 2)
    indice_metodo = random.randint(0, 1)
    indice_receptor = random.randint(0,19)
    
    new_factura = factura.Factura(
        uuid = generar_cadena_aleatoria(),
        nombre_receptor = lista_empresas_externas[indice_receptor].nombre_empresa,
        rfc_receptor = lista_empresas_externas[indice_receptor].rfc, 
        nombre_emisor = lista_empresas_sistema[indice_empresa].nombre_empresa,
        rfc_emisor = lista_empresas_sistema[indice_empresa.rfc],
        fecha_emision = generar_fecha_aleatoria(2023, 2024),
        monto = round(random.uniform(5, 1000000), 2),
        metodo_pago = lista_metodos_pago[indice_metodo],
        vigencia = 'No definido',
        divisa = 'MXN'
    )
    
    nuevas_facturas_cxc.append(new_factura)
    
    if indice_metodo == 0 and random.randint(0,1) == 1:
        #SI EL METODO ES EFECTIVO SE AGREGA UN MOVIMIENTO QUE CONCILIE LA FACTURA
        new_movimiento = movimiento.Movimiento(
            id_transaccion = generar_cadena_aleatoria(),
            empresa = lista_empresas_sistema[indice_empresa].nombre_empresa,
            fecha = new_factura.fecha_emision + datetime.timedelta(days=random.randint(-5,5))
            concepto = 'Datos extra',
            monto = new_factura.monto,
            moneda = new_factura.divisa,
            referencia = new_factura.uuid,
            clave_rastreo = generar_cadena_aleatoria(12),
            tipo_movimiento = lista_tipo_movimiento[random.randint(0,1)],
            banco_emisor = 
            
        )
    
    