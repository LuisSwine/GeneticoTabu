import pandas as pd
from datetime import date, timedelta

import preprocesamiento

movimientos = pd.read_csv('Data/movimientos_normalized.csv')

#Primero eliminamos todos los movimientos menores a un peso
condicion_monto = movimientos['Monto'] >= 1.0
movimientos_filtrados = movimientos.loc[condicion_monto].copy()

#Generamos un script para conciliar todos los movimientos PUE
facturas_cxc = pd.read_csv('Data/reportCXC_20231113.csv')
facturas_cxp = pd.read_csv('Data/reportCXP_20231113.csv')

#Nos quedamos únicamente con las faturas PUE
condicion_pue_cxc = facturas_cxc['MetodoPago'] == 'PUE'
condicion_pue_cxp = facturas_cxp['MetodoPago'] == 'PPD'
cxc_pue = facturas_cxc.loc[condicion_pue_cxc].copy()
cxp_pue = facturas_cxp.loc[condicion_pue_cxp].copy()

#Ahora procedemos a iterar sobre las cuentas pue por cobrar
facturas_por_cobrar = preprocesamiento.clean_cuentas(cxc_pue)
facturas_por_pagar = preprocesamiento.clean_cuentas(cxp_pue)
ingresos, egresos = preprocesamiento.clean_movimientos(movimientos_filtrados)

#Ahora vamos a iterar sobre todos las cuentas por cobrar
for cuenta in facturas_por_cobrar:
    # cuenta.showFactura()
    
    #Como es cuenta por cobrar estaremos buscando directamente un ingreso para el emisor
    empresa = cuenta.nombre_emisor
    emisor = cuenta.rfc_emisor
    
    #Nos quedamos con los movimientos que tiene como valor de empresa el nombre_emisor de la fcatura
    espacio_busqueda = list(filter(lambda mov:  mov.empresa == cuenta.nombre_emisor, ingresos))
    #Nos quedamos con los movimientos que tienen como rfc_receptor el rfc_emisor de la factura
    espacio_busqueda = list(filter(lambda mov: mov.rfc_receptor == cuenta.rfc_emisor, espacio_busqueda))
    #Nos quedamos con los movimientos que tienen como cep_rfc_receptor el rfc_emisor de la factura
    espacio_busqueda = list(filter(lambda mov: mov.comprobante.rfc_receptor == cuenta.rfc_emisor, espacio_busqueda))
    #Nos quedamos con los movimientos emitidos a partir del 1 del mes anterior a la emisión de la factura
    # Calcular la fecha del 1 del mes anterior
    fecha_mes_anterior = cuenta.fecha_emision.replace(day=1) - timedelta(days=1)
    fecha_1_mes_anterior = fecha_mes_anterior.replace(day=1)
    # Filtrar la lista de objetos
    objetos_filtrados = [objeto for objeto in espacio_busqueda if objeto.fecha >= fecha_1_mes_anterior]
    
    print(len(espacio_busqueda))
        
    input()

    
    
    
    
