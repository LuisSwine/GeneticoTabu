"""
MODULO DE NORMALIZACIÓN 

Descripción: Este módulo funciona para normalizar los movimientos con ayuda de la base de conocimiento extraída
completando los datos faltantes con los datos registrados

"""

import pandas as pd
from datetime import datetime

#Primero abrimos el dataset con todos los movimientos
df_movimientos = pd.read_csv('Data/movimientos.csv')
df_movs_copia = df_movimientos.copy()

#Tambien abrimos nuestra base de conocimientos de empresas
df_empresas_moniic = pd.read_csv('Knowledge_Base/empresas_moniic.csv')
df_empresas_externas = pd.read_csv('Knowledge_Base/empresa_externas.csv')

#Iteramos sobre las filas de df_movimientos
for index, row in df_movimientos.iterrows():
    #Extraemos el valor de la columna 'Empresa' y lo guardamos en una variable empresa
    empresa = row['Empresa']
    #Verificamos si la empresa coincide con el valor de la columna 'empresa' de alguno de los registros del df_empresas_moniic
    valores_empresa = df_empresas_moniic[df_empresas_moniic['empresa'] == empresa]
    
    #Validamos las fechas del movimiento y del CEP
    #Primero obtenemos los valores de la fecha y los 3 valores del CEP
    fecha = row['Fecha']
    cep_dia = row['CEP_Dia']
    cep_mes = row['CEP_Mes']
    cep_anio = row['CEP_Anio']
    
    if (pd.isna(fecha) and (not pd.isna(cep_dia) and not pd.isna(cep_mes) and not pd.isna(cep_anio))):
        #En caso de que falte la fecha pero se tenga información de los datos del cep
        fecha = cep_dia+'/'+cep_mes+'/'+cep_anio
        #Ahora asignamos la fecha
        df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('Fecha')] = fecha
    elif (pd.isna(cep_dia) and pd.isna(cep_mes) and pd.isna(cep_anio)) and not pd.isna(fecha):
        #En caso que no tengamos los datos cep pero si la fecha entonces ajustamos
        fecha_obj = datetime.strptime(fecha, '%d/%m/%y')
        df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_Dia')] = fecha_obj.day
        df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_Mes')] = fecha_obj.month
        df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_Anio')] = fecha_obj.year
        
    #Validamos los montos del movimiento y del CEP
    monto = row['Monto']
    cep_monto = row['CEP_Amount']
    
    if pd.isna(monto) and not pd.isna(cep_monto):
        #En este caso colocamos el valor del monto del cep al monto del movimiento
        df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('Monto')] = cep_monto
    elif pd.isna(cep_monto) and not pd.isna(monto):
        #En este caso colocamos el valor del monto del movimiento al monto del cep
        df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_Amount')] = monto
        
    #Validamos las claves de rastreo del movimiento y del cep
    rastro_key = row['ClaveRastreo']
    cep_rastreo_key = row['CEP_ClaveRastreo']
    
    if pd.isna(rastro_key) and not pd.isna(cep_rastreo_key):
        #En este caso colocamos el valor del monto del cep al monto del movimiento
        df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('ClaveRastreo')] = cep_rastreo_key
    elif pd.isna(cep_rastreo_key) and not pd.isna(rastro_key):
        #En este caso colocamos el valor del monto del cep al monto del movimiento
        df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_ClaveRastreo')] = rastro_key
    
    #Validamos los receptores y emisores
    if valores_empresa.empty:
        print(f"La empresa {empresa} no está registrada en nuestra Base de Conocimiento")
        #TODO: Hacer un script para guardar la nueva empresa
    else:
        #print(valores_empresa)    
        #Identificamos el tipo de movimiento
        if row['TipoMovimiento'] == 'Egreso' or row['TipoMovimiento'] == 'Egreso interbancario' or row['RFCEmisor'] == str(valores_empresa['rfc'].values[0]) or row['CEP_RFCEmisor'] == str(valores_empresa['rfc'].values[0]):
            #Asignamos la información de la empresa a los valores de NombreEmisor, RFCEmisor, CEP_NombreEmisor y CEP_RFCEmisor
            df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('NombreEmisor')] = valores_empresa['empresa']
            df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('RFCEmisor')] = valores_empresa['rfc']
            df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_NombreEmisor')] = valores_empresa['empresa']
            df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_RFCEmisor')] = valores_empresa['rfc']
            df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('TipoMovimiento')] = 'Egreso'
            
            #Ahora verificamos la empresa receptora
            #Validamos primero el NombreReceptor
            nombre_receptor = row['NombreReceptor']
            rfc_receptor = row['RFCReceptor']
            cep_nombre_receptor = row['CEP_NombreReceptor']
            cep_rfc_receptor = row['CEP_RFCReceptor']
            
            v_empresa_new = None
            
            #Si todos los valores son nan
            if pd.isna(nombre_receptor) and pd.isna(rfc_receptor) and pd.isna(cep_nombre_receptor) and pd.isna(cep_rfc_receptor):
                print('No es posible verificar los valores del receptor del movimiento '+ row['idTransaccion'] +' pues falta información')
            else: 
                if not pd.isna(nombre_receptor):
                    v_empresa_new = df_empresas_externas[df_empresas_externas['empresa'] == nombre_receptor]
                elif not pd.isna(rfc_receptor):
                    v_empresa_new = df_empresas_externas[df_empresas_externas['rfc'] == rfc_receptor]
                elif not pd.isna(cep_nombre_receptor):
                    v_empresa_new = df_empresas_externas[df_empresas_externas['empresa'] == cep_nombre_receptor]
                elif not pd.isna(cep_rfc_receptor):
                    v_empresa_new = df_empresas_externas[df_empresas_externas['rfc'] == cep_rfc_receptor]
                    
                if v_empresa_new.empty:
                    print(f"No se encontró a '{nombre_receptor}' '{rfc_receptor}' '{cep_nombre_receptor}' '{cep_rfc_receptor}' entre las empresas externas.")
                else:
                    df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('NombreReceptor')] = v_empresa_new['empresa']
                    df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('RFCReceptor')] = v_empresa_new['rfc']
                    df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_NombreReceptor')] = v_empresa_new['empresa']
                    df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_RFCReceptor')] = v_empresa_new['rfc']
        else:
            #Asignamos la información de la empresa a los valores de NombreReceptor, RFCReceptor, CEP_NombreReceptor y CEP_RFCReceptor
            df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('NombreReceptor')] = valores_empresa['empresa']
            df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('RFCReceptor')] = valores_empresa['rfc']
            df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_NombreReceptor')] = valores_empresa['empresa']
            df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_RFCReceptor')] = valores_empresa['rfc']
            
            #Ahora verificamos la empresa receptora
            #Validamos primero el NombreReceptor
            nombre_emisor = row['NombreEmisor']
            rfc_emisor = row['RFCEmisor']
            cep_nombre_emisor = row['CEP_NombreEmisor']
            cep_rfc_emisor = row['CEP_RFCEmisor']
            
            v_empresa_new = None
            
            #Si todos los valores son nan
            if pd.isna(nombre_emisor) and pd.isna(rfc_emisor) and pd.isna(cep_nombre_emisor) and pd.isna(cep_rfc_emisor):
                print('No es posible verificar los valores del emisor del movimiento '+ row['idTransaccion'] +' pues falta información')
            else: 
                if not pd.isna(nombre_emisor):
                    v_empresa_new = df_empresas_externas[df_empresas_externas['empresa'] == nombre_emisor]
                elif not pd.isna(rfc_emisor):
                    v_empresa_new = df_empresas_externas[df_empresas_externas['rfc'] == rfc_emisor]
                elif not pd.isna(cep_nombre_emisor):
                    v_empresa_new = df_empresas_externas[df_empresas_externas['empresa'] == cep_nombre_emisor]
                elif not pd.isna(cep_rfc_emisor):
                    v_empresa_new = df_empresas_externas[df_empresas_externas['rfc'] == cep_rfc_emisor]
                    
                if v_empresa_new.empty:
                    print(f"No se encontró a '{nombre_emisor}' '{rfc_emisor}' '{cep_nombre_emisor}' '{cep_rfc_emisor}' entre las empresas externas.")
                else:
                    df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('NombreEmisor')] = v_empresa_new['empresa']
                    df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('RFCEmisor')] = v_empresa_new['rfc']
                    df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_NombreEmisor')] = v_empresa_new['empresa']
                    df_movs_copia.iloc[index,df_movs_copia.columns.get_loc('CEP_RFCEmisor')] = v_empresa_new['rfc']
                    pass
                pass
            pass
        pass
      
df_movs_copia.to_csv('Data/movimientos_normalized_4.csv', index=False)