import pandas as pd
import datetime
import warnings
import math


import factura
import movimiento
import cep

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
        
        if move.tipo_movimiento in ['Ingreso', 'Ingreso interbancario']:
            arreglo_ingresos.append(move)
        elif move.tipo_movimiento in ['Egreso', 'Egreso interbancario']:
            arreglo_egresos.append(move)
        
    return arreglo_ingresos, arreglo_egresos


#Fecha formato AAAA/MM/DD
def filtraPorFecha(df, nombreCampoFecha, fechaFactura, tipo): 
  matches = pd.DataFrame()
  matches = df.head(0)
  matches = matches.copy()
  splitDateFac = fechaFactura.split('/')
  year = int(splitDateFac[2])
  month = int(splitDateFac[1])
  day = 1

  if tipo == "PUE":
    if(month==1):
      month = 12
      year = year-1
    else:
      month = month-1
    print("Buscando desde ",str(year)+"/"+str(month))
  elif tipo == "PPD":
    year = year-1
    month = 1
    print("Buscando desde ",str(year)+"/"+str(month))
  else:
    print("Tipo invalido")

  for index, row in df.iterrows():
    item = row[nombreCampoFecha]
    splitDateMov = item.split('/')
    yearMov = int(splitDateMov[2])
    monthMov = int(splitDateMov[1])
    if yearMov>=year and monthMov>=month:
      matches.loc[len(matches)] = row

  return matches