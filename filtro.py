#IMPORTAMOS LAS LIBRERIAS NECESARIAS
import math

"""
Definimos un primer filtro para los movimientos donde vamos a filtrar los movimientos por monto, dependiendo 
de si la factura a conciliar es de tipo PUE o PPD
"""
def filtrar_por_tipo(tipo, monto_factura, movimientos):
    if tipo == 'PUE':
        #Si la factura es PUE entonces vamos a devolver solo los movimiento cuyo monto sea mayor o igual al de la factura
        #esto porque en caso de que el movimiento busque pagar más de una PUE  la vez debemos considerar montos mayores al de la factura
        return list(filter(lambda mov: mov.monto >= monto_factura, movimientos))
    elif tipo == 'PPD':
        #Si la factura es de tipo PPD siempre el movimiento deberá ser de un monto menor o igual al monto de la factura.
        return list(filter(lambda mov: mov.monto <= monto_factura, movimientos))

"""
Definimos una funcion para filtrar el rfc en casos de ingreso, donde el receptor del movimiento tiene que ser el emisor de la factura 
"""
def filtro_rfc_ingreso(mov, factura):
    return mov.rfc_receptor == factura.rfc_emisor or (not isinstance(mov.rfc_receptor, str) and math.isnan(float(mov.rfc_receptor)))

"""
Definimos una funcion para filtrar el rfc en casos de egreso, donde el emisor del movimiento tiene que ser el receptor de la factura 
"""
def filtro_rfc_egreso(mov, factura):
    return mov.rfc_emisor == factura.rfc_receptor or (not isinstance(mov.rfc_emisor, str) and math.isnan(float(mov.rfc_emisor)))

"""
Definimos el filtro que se va a apoyar de las dos funciones anteriores para regresar los movimientos indicados
"""
def filtrar_por_cuenta(factura, flag_flujo, movimientos):
    if flag_flujo == 0: #0 -> corresponde a un ingreso
        movimientos = list(filter(lambda mov:  filtro_rfc_ingreso(mov, factura), movimientos))
    if flag_flujo == 1: #1 -> corresponde a un egreso
        movimientos = list(filter(lambda mov:  filtro_rfc_ingreso(mov, factura), movimientos))
    
    return movimientos

"""
Definimos un tercer filtro por fecha donde en caso de las PUE únicamente vamos a retornar 
aquellos movimientos recibidos después de la fecha de la factura y en caso PPD retornamos
todos los movimientos, pues todos son posibles
"""
def filtrar_por_fecha(tipo, fecha, movimientos):
    if tipo == 'PUE':
        return [
            movimiento for movimiento in movimientos
            if movimiento.fecha >= fecha
        ]
    else:
        return movimientos