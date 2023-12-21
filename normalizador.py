import pandas as pd

array_ingresos = ['Ingreso', 'Ingreso interbancario']
array_egresos = ['Egreso', 'Egreso interbancario']

movimientos = pd.read_csv('Data/movimientos.csv')
movimientos_copy = movimientos.copy()

#Vamos a obtener los valores únicos de las empresas
cat001_empresa = movimientos['Empresa'].unique()

print(cat001_empresa)

for empresa in cat001_empresa:
    #Obtenemos todos los movimientos de la empresa cliente de Moniic iterada
    subconjunto_empresa = movimientos[movimientos['Empresa'] == empresa]
    
    #Obtenemos todos los registros que representen un ingreso a la empresa
    sub_emp_ingresos = subconjunto_empresa[subconjunto_empresa['TipoMovimiento'].isin(array_ingresos)]
    #Obtenemos todos los registros que representen un egreso a la empresa
    sub_emp_egresos = subconjunto_empresa[subconjunto_empresa['TipoMovimiento'].isin(array_egresos)]
    
    #Obtenemos todos los rfc_unicos de los ingresos en el apartado CEP y movimiento
    cat002_rfc_receptor_cep = sub_emp_ingresos['CEP_RFCReceptor'].unique()
    cat002_rfc_receptor     = sub_emp_ingresos['RFCReceptor'].unique()
    #Obtenemos todos los rfc_unicos de los egresos en el apartado CEP
    cat002_rfc_emisor_cep = sub_emp_egresos['CEP_RFCEmisor'].unique()
    cat002_rfc_emisor     = sub_emp_egresos['RFCEmisor'].unique()
    
    #Filtramos y eliminamos de la lista los valores NA o nan
    cat002_rfc_receptor_cep = pd.Series(cat002_rfc_receptor_cep).dropna().tolist()
    cat002_rfc_receptor     = pd.Series(cat002_rfc_receptor).dropna().tolist()
    cat002_rfc_emisor_cep   = pd.Series(cat002_rfc_emisor_cep).dropna().tolist()
    cat002_rfc_emisor       = pd.Series(cat002_rfc_emisor).dropna().tolist()
    
    #Obtenemos el primer registro
    rfc_receptor_cep = cat002_rfc_receptor_cep[0] if len(cat002_rfc_receptor_cep) > 0 else None
    rfc_receptor     = cat002_rfc_receptor[0] if len(cat002_rfc_receptor) > 0 else None
    rfc_emisor_cep   = cat002_rfc_emisor_cep[0] if len(cat002_rfc_emisor_cep) > 0 else None
    rfc_emisor       = cat002_rfc_emisor[0] if len(cat002_rfc_emisor) > 0 else None
    
    #Mostramos el registro por empresa
    print('Empresa: ' + empresa)
    print('Datos emisor -> CEP_RFC: {} ; RFC: {}'.format(rfc_emisor_cep, rfc_emisor))
    print('Datos receptor -> CEP_RFC: {} ; RFC: {}'.format(rfc_receptor_cep, rfc_receptor))
    
    movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_ingresos)), 'NombreReceptor'] = empresa
    movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_ingresos)), 'CEP_NombreReceptor'] = empresa
    movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_egresos)), 'NombreEmisor'] = empresa
    movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_egresos)), 'CEP_NombreEmisor'] = empresa
    
    if rfc_receptor == rfc_receptor_cep or (rfc_receptor is not None and rfc_receptor_cep is None):
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_ingresos)), 'CEP_RFCReceptor'] = rfc_receptor
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_ingresos)), 'RFCReceptor'] = rfc_receptor
    elif rfc_receptor_cep is not None and rfc_receptor is None:
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_ingresos)), 'CEP_RFCReceptor'] = rfc_receptor_cep
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_ingresos)), 'RFCReceptor'] = rfc_receptor_cep
    elif rfc_receptor != 'ND010101**D':   
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_ingresos)), 'CEP_RFCReceptor'] = rfc_receptor
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_ingresos)), 'RFCReceptor'] = rfc_receptor
    else:
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_ingresos)), 'CEP_RFCReceptor'] = rfc_receptor_cep
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_ingresos)), 'RFCReceptor'] = rfc_receptor_cep
    
    if rfc_emisor == rfc_emisor_cep or (rfc_emisor != None and rfc_emisor_cep == None):
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_egresos)), 'CEP_RFCEmisor'] = rfc_emisor
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_egresos)), 'RFCEmisor'] = rfc_emisor
    elif rfc_emisor_cep != None and rfc_emisor == None:
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_egresos)), 'CEP_RFCEmisor'] = rfc_emisor_cep
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_egresos)), 'RFCEmisor'] = rfc_emisor_cep
    elif rfc_emisor != 'ND010101**D':   
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_egresos)), 'CEP_RFCEmisor'] = rfc_emisor
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_egresos)), 'RFCEmisor'] = rfc_emisor
    else:
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_egresos)), 'CEP_RFCEmisor'] = rfc_emisor_cep
        movimientos_copy.loc[(movimientos_copy['Empresa'] == empresa) & (movimientos_copy['TipoMovimiento'].isin(array_egresos)), 'RFCEmisor'] = rfc_emisor_cep
     
    pass

movimientos_copy.to_csv('Data/movimientos_normalized.csv', index=False)
    
