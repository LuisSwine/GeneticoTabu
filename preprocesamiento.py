#PRIMERO IMPORTAMOS TODAS LAS LIBRERIAS NECESARIAS
import pandas as pd
import datetime
import math

#DESPUES IMPORTAMOS LAS CLASE NECESARIAS DE SUS RESPECTIVOS MODULOS
import factura
import movimiento
import cep

#Definimos la funcion para limpiar las facturas y convertir cada fila del dataset en un objeto de la clase correspondiente
def clean_cuentas(pd_df):
    arreglo_cuentas = []
    for index, row in pd_df.iterrows():
        nueva_factura = factura.Factura(
        row['UUIDFactura'], 
        row['Nombre_Receptor'],
        row['RFC_Receptor'],
        row['Nombre_Emisor'],
        row['RFC_Emisor'],
        datetime.datetime.strptime(row['FechaEmision'], '%d/%m/%Y'),
        row['Monto'],
        row['MetodoPago'],
        row['Vigencia'],
        row['DivisaFactura'])
    
        arreglo_cuentas.append(nueva_factura)
        
    return arreglo_cuentas
  
#Defimos la funcion para limpiar los movimientos y convertir cada fila del dataset en un objeto de la clase correspondiente
def clean_movimientos(pd_df):
    arreglo_ingresos = []
    arreglo_egresos = []
    
    for index, row in pd_df.iterrows():
        
        fecha = None
        
        if not math.isnan(row['CEP_Dia']) and not math.isnan(row['CEP_Mes']) and not math.isnan(row['CEP_Anio']):
            fecha = f"{int(row['CEP_Dia'])}/{int(row['CEP_Mes'])}/{int(row['CEP_Anio'])}"
            fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y')
        
        comprobante = cep.CEP(
            fecha,
            row['CEP_ClaveRastreo'],
            row['CEP_Amount'],
            row['CEP_IVA'],
            row['CEP_Concepto'],
            row['CEP_RFCReceptor'],
            row['CEP_NombreReceptor'],
            row['CEP_CuentaReceptora'],
            row['CEP_BancoReceptor'],
            row['CEP_RFCEmisor'],
            row['CEP_NombreEmisor'],
            row['CEP_CuentaEmisora'],
            row['CEP_BancoEmisor']
        )
        move = movimiento.Movimiento(
            row['idTransaccion'],
            row['Empresa'],
            datetime.datetime.strptime(row['Fecha'], '%d/%m/%y'),
            row['Concepto'],
            row['Monto'],
            row['Moneda'],
            row['Referencia'],
            row['ClaveRastreo'],
            row['TipoMovimiento'],
            row['BancoEmisor'],
            row['CuentaEmisora'],
            row['NombreEmisor'],
            row['RFCEmisor'],
            row['BancoReceptor'],
            row['CuentaReceptora'],
            row['NombreReceptor'],
            row['RFCReceptor'],
            comprobante
        )
        
        #Al final también clasificamos entre ingresos y egresos para tener identificada esta información
        if move.tipo_movimiento in ['Ingreso', 'Ingreso interbancario'] or pd.isna(move.tipo_movimiento):
            arreglo_ingresos.append(move)
        elif move.tipo_movimiento in ['Egreso', 'Egreso interbancario'] or pd.isna(move.tipo_movimiento):
            arreglo_egresos.append(move)
        
    return arreglo_ingresos, arreglo_egresos