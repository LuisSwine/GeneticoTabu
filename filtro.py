import math

def filtrar_por_tipo(tipo, monto_factura, movimientos):
    if tipo == 'PUE':
        return list(filter(lambda mov: mov.monto >= monto_factura, movimientos))
    elif tipo == 'PPD':
        return list(filter(lambda mov: mov.monto <= monto_factura, movimientos))

def filtro_rfc_ingreso(mov, factura):
    return mov.rfc_receptor == factura.rfc_emisor or (not isinstance(mov.rfc_receptor, str) and math.isnan(float(mov.rfc_receptor)))

def filtro_rfc_egreso(mov, factura):
    return mov.rfc_emisor == factura.rfc_receptor or (not isinstance(mov.rfc_emisor, str) and math.isnan(float(mov.rfc_emisor)))

def filtrar_por_cuenta(factura, flag_flujo, movimientos):
    if flag_flujo == 0: #0 -> corresponde a un ingreso
        movimientos = list(filter(lambda mov:  filtro_rfc_ingreso(mov, factura), movimientos))
    if flag_flujo == 1: #1 -> corresponde a un egreso
        movimientos = list(filter(lambda mov:  filtro_rfc_ingreso(mov, factura), movimientos))
    
    return movimientos

def filtrar_por_fecha(tipo, fecha, movimientos):
    if tipo == 'PUE':
        return [
            movimiento for movimiento in movimientos
            if movimiento.fecha >= fecha
        ]
    else:
        return movimientos