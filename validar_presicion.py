import pandas as pd

import api_v1 as api

#Primero abrimos los dos archivos con los reportes de cxc y cxp
cuentas_por_cobrar = pd.read_csv('Data/reportCXC.csv') 
cuentas_por_pagar = pd.read_csv('Data/reportCXP.csv') 

#Filtramos solo aquellas facturas que podamos verificar, es decir conciliadas sin importar si están confirmadas o no
subconjunto_cxc = cuentas_por_cobrar[cuentas_por_cobrar['Observaciones'] != 'NINGUNA']
subconjunto_cxp = cuentas_por_pagar[cuentas_por_pagar['Observaciones'] != 'NINGUNA']

#Primero verificamos las confirmadas
subconjunto_cxc_confirmadas = subconjunto_cxc[subconjunto_cxc['Observaciones'] == 'VINCULACIÓN CONFIRMADA']
subconjunto_cxp_confirmadas = subconjunto_cxp[subconjunto_cxp['Observaciones'] == 'VINCULACIÓN CONFIRMADA']
#print(subconjunto_cxp_confirmadas)

correctos = 0
#Iteramos sobre los elementos del primer subconjunto
for index, row in subconjunto_cxc.iterrows():
    #Para cada registro ejecutamos el algoritmo, primero extraemos el UUID de la factura
    uuidFactura = str(row["UUIDFactura"])
    #Tambien extraemos el id de movimiento que concilia correctamente
    id_movimiento = str(row['IdTransaccion'])
    
    print(uuidFactura)
    
    #Ahora ejecutamos el algoritmo
    bandera, conciliacion = api.realizar_conciliacion(uuidFactura)
    
    if bandera == 3:
        print('No fue posible realizar la conciliacion pues no hay movimientos emitidos')

    if bandera == 0:
        es_correcto = any(obj.id_transaccion == id_movimiento for obj in conciliacion)
        if es_correcto:
            correctos = correctos + 1
        else:
            print("La conciliación no es correcta")
            for movimiento in conciliacion:
                print('\n')
                print(movimiento.id_transaccion)
                print(movimiento.monto)
                pass
            pass
        
    elif bandera == 1:
        correctos = correctos + 1
    elif bandera == 2:
        es_correcto = any(obj.id_transaccion == id_movimiento for obj in conciliacion)
        if es_correcto:
            correctos = correctos + 1
        else:
            print("La conciliación no es correcta")
            for movimiento in conciliacion:
                print('\n')
                print(movimiento.id_transaccion)
                print(movimiento.monto)
                pass
            pass
            
        
for index, row in subconjunto_cxp.iterrows():
    #Para cada registro ejecutamos el algoritmo, primero extraemos el UUID de la factura
    uuidFactura = str(row["UUIDFactura"])
    #Tambien extraemos el id de movimiento que concilia correctamente
    id_movimiento = str(row['IdTransaccion'])
    
    
    print(uuidFactura)
    
    #Ahora ejecutamos el algoritmo
    bandera, conciliacion = api.realizar_conciliacion(uuidFactura)
    
    if bandera == 6:
        print('No fue posible realizar la conciliacion pues no hay movimientos emitidos')

    if bandera == 4:
        es_correcto = any(obj.id_transaccion == id_movimiento for obj in conciliacion)
        if es_correcto:
            correctos = correctos + 1
        
    elif bandera == 5:
        correctos = correctos + 1
    elif bandera == 7:
        es_correcto = any(obj.id_transaccion == id_movimiento for obj in conciliacion)
        if es_correcto:
            correctos = correctos + 1
            
print(subconjunto_cxc.shape[0])
print(subconjunto_cxp.shape[0])
print(correctos)