import pandas as pd

#1. Abrimos primero el dataset con los movimientos
movimientos = pd.read_csv('Data/movimientos.csv')
movs_normalized = movimientos.copy()

#2. Lo primero que debemos de normalizar son las empresas clientes de Moniic
#2.1. Abrimos la base de conocimientos con las empresas
empresas = pd.read_csv('Knowledge_Base/empresas_moniic.csv')

#2.2. Filtramos primero los movimientos donde coincida el nombre de la empresa y obtenemos el subconjunto
for index, empresa in empresas.iterrows():
    
    subconjunto_empresa = movimientos[movimientos['Empresa'] == empresa['empresa']]
    #Ahora filtramos el subconjunto y extraemos únicamente los movimientos que son ingresos y egresos y donde la empresa es la receptora
    sub_emp_ingresos = subconjunto_empresa[(subconjunto_empresa['TipoMovimiento']=='Ingreso') | (subconjunto_empresa['TipoMovimiento']=='Ingreso interbancario')]
    sub_emp_egresos = subconjunto_empresa[(subconjunto_empresa['TipoMovimiento']=='Egreso') | (subconjunto_empresa['TipoMovimiento']=='Egreso interbancario')]
    
    #A los ingresos colocamos el nombre y rfc de la empresa al receptor
    for i, ingreso in sub_emp_ingresos.iterrows():
        movs_normalized.iloc[i,movs_normalized.columns.get_loc('NombreReceptor')] = empresa['empresa']
        movs_normalized.iloc[i,movs_normalized.columns.get_loc('CEP_NombreReceptor')] = empresa['empresa']
        movs_normalized.iloc[i,movs_normalized.columns.get_loc('RFCReceptor')] = empresa['rfc']
        movs_normalized.iloc[i,movs_normalized.columns.get_loc('CEP_RFCReceptor')] = empresa['rfc']
    #A los egresos colocamos el nombre y rfc de la empresa al emisor
    for i, egreso in sub_emp_egresos.iterrows():
        movs_normalized.iloc[i,movs_normalized.columns.get_loc('NombreEmisor')] = empresa['empresa']
        movs_normalized.iloc[i,movs_normalized.columns.get_loc('CEP_NombreEmisor')] = empresa['empresa']
        movs_normalized.iloc[i,movs_normalized.columns.get_loc('RFCEmisor')] = empresa['rfc']
        movs_normalized.iloc[i,movs_normalized.columns.get_loc('CEP_RFCEmisor')] = empresa['rfc']
    
    input('')
    

