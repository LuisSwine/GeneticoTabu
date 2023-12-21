import pandas as pd
from datetime import timedelta

import preprocesamiento
import genetic_algorithm


def realizar_conciliacion(uuid):
    
    #Primero vamos a abrimos todos los datasets
    movimientos = pd.read_csv('Data/movimientos_normalized_3.csv')
    facturasCxC = pd.read_csv('Data/reportCXC_20231113.csv')
    facturasCxP = pd.read_csv('Data/reportCXP_20231113.csv')

    #Procedemos a limpiar la información y a guardarlo en los datasets correspondientes
    cuentas_por_cobrar = preprocesamiento.clean_cuentas(facturasCxC)
    cuentas_por_pagar = preprocesamiento.clean_cuentas(facturasCxP)
    ingresos, egresos = preprocesamiento.clean_movimientos(movimientos)
    
    
    #Recibir el UUID de la factura y buscams la factura en los datasets de facturas
    #Ahora buscamos la el uuid en las cuentas por pagar y por cobrar
    resultado_cuentas_pp = list(filter(lambda obj: obj.uuid == uuid, cuentas_por_pagar))
    resultado_cuentas_pc = list(filter(lambda obj: obj.uuid == uuid, cuentas_por_cobrar))
    
    #Instanciamos las variables que serán los datos de entrada para el algoritmo
    factura = None
    movimientos_candidatos = None
    flag_flujo = 0
    """
    PARA LA BANDERA DE TIPO DE PAGO TENEMOS LOS SIGUIENTES VALORES:
    0. Cuenta por cobrar
    1. Cuenta por pagar
    """

    #Inicialiazamos los espacios de búqueda
    if resultado_cuentas_pp:
        factura = resultado_cuentas_pp[0]
        movimientos_candidatos = egresos
        flag_flujo = 1
        
    if resultado_cuentas_pc:
        factura = resultado_cuentas_pc[0]
        movimientos_candidatos = ingresos
        
    factura.showFactura()
    #En las cuentas por cobrar filtramos los movimientos que en el valor de 'Empresa' tengan al emisor de la factura
    if flag_flujo == 0:
        movimientos_candidatos = list(filter(lambda obj: obj.empresa == factura.nombre_emisor, movimientos_candidatos))
        #Ahora filtramos al receptor de la factura
        #Mediante el RFC
        filtro_1 = lambda obj: obj.rfc_receptor == factura.rfc_emisor
        filtro_2 = lambda obj: obj.comprobante.rfc_receptor == factura.rfc_emisor
        filtro_3 = lambda obj: obj.nombre_receptor == factura.nombre_remisor
        filtro_4 = lambda obj: obj.comprobante.nombre_receptor == factura.nombre_emisor
        filtro_5 = lambda obj: obj.rfc_emisor == factura.rfc_receptor
        filtro_6 = lambda obj: obj.comprobante.rfc_emisor == factura.rfc_receptor
        filtro_7 = lambda obj: obj.nombre_emisor == factura.nombre_receptor
        filtro_8 = lambda obj: obj.comprobante.nombre_emisor == factura.nombre_receptor
        filtro_9 = lambda obj: pd.isna(obj.rfc_emisor)
        filtro_10 = lambda obj: pd.isna(obj.comprobante.rfc_emisor)
        filtro_11 = lambda obj: pd.isna(obj.nombre_emisor)
        filtro_12 = lambda obj: pd.isna(obj.comprobante.nombre_emisor)
        filtro_13 = lambda obj: pd.isna(obj.rfc_receptor)
        filtro_14 = lambda obj: pd.isna(obj.comprobante.rfc_receptor)
        filtro_15 = lambda obj: pd.isna(obj.nombre_receptor)
        filtro_16 = lambda obj: pd.isna(obj.comprobante.nombre_receptor)
        
        #Aplicamos primero los filtros de emisor
        movimientos_candidatos = list(filter(lambda obj: filtro_1(obj) or filtro_2(obj) or filtro_3(obj) or filtro_4(obj) or filtro_9(obj) or filtro_10(obj) or filtro_11(obj) or filtro_12(obj), movimientos_candidatos))
        movimientos_candidatos = list(filter(lambda obj: filtro_5(obj) or filtro_6(obj) or filtro_7(obj) or filtro_8(obj) or filtro_13(obj) or filtro_14(obj) or filtro_15(obj) or filtro_16(obj), movimientos_candidatos))
        
        if len(movimientos_candidatos) == 0:
            print('No se tiene registro de movimientos emitidos por la empresa ', factura.nombre_receptor)
            return 3, []
        
        #Ahora verificamos si es pue o ppd
        if factura.metodo_pago == 'PUE':
            #Filtramos solo las facturas que sean de monto igual o mayor al de la factura
            movimientos_candidatos = list(filter(lambda obj: obj.monto >= factura.monto, movimientos_candidatos))
            #Filtramos por fecha solo aquellas que sean del primero del mes anterior en adelante
            # Obtener la fecha del primer día del mes anterior a la fecha del objeto
            fecha_inicio = (factura.fecha_emision - timedelta(days=factura.fecha_emision.day)).replace(day=1)
            # Filtrar los objetos que cumplen con la condición
            movimientos_candidatos = [obj for obj in movimientos_candidatos if obj.fecha >= fecha_inicio]
            
            if len(movimientos_candidatos) > 1:
                #Verificamos si en la lista existe un movimiento con el monto exacto de la factura
                movimientos_exactos = list(filter(lambda obj: obj.monto == factura.monto, movimientos_candidatos))
                if len(movimientos_exactos) == 1:
                    return 1, movimientos_exactos[0]
                else:
                    return 0, movimientos_candidatos
            elif len(movimientos_candidatos) == 1:
                return 1, movimientos_candidatos[0]
        
        elif factura.metodo_pago == 'PPD':
            
            if len(movimientos_candidatos) == 1 and movimientos_candidatos[0].monto == factura.monto:
                return 1, movimientos_candidatos[0]
            elif len(movimientos_candidatos) > 1:
                movimientos_exactos = list(filter(lambda obj: obj.monto == factura.monto, movimientos_candidatos))
                if len(movimientos_exactos) == 1:
                    return 1, movimientos_exactos[0]
                elif len(movimientos_candidatos) > 4:
                    #Aquí si ejecutamos el algoritmo de búsqueda tabú con genético
                    print('Ejecutando algoritmo')
                    #Ahora ordenamos los movimientos por monto de mayor a menor
                    movimientos_candidatos = sorted(movimientos_candidatos, key=lambda movimiento: movimiento.monto, reverse=True)

                    #Definimos los hiperparametros del algoritmo
                    tam_poblacion = len(movimientos_candidatos)
                    porcentaje_mutacion = 0.5
                    global_solution = 1
                    
                    propuesta, best_fitness, worst_fitness, generacion, iteraciones_tabu = genetic_algorithm.algoritmoGeneticoHibrido(
                        tam_poblacion,
                        porcentaje_mutacion,
                        global_solution,
                        factura.monto,
                        movimientos_candidatos
                        )
                    
                    conciliacion_creada = []
                    for i in range(0, len(propuesta)):
                        if propuesta[i] == 1:
                            conciliacion_creada.append(movimientos_candidatos[i])
                            
                    return 2, conciliacion_creada
                    
                else:
                    return 0, movimientos_candidatos    
            elif len(movimientos_candidatos) == 0:
                return 3, []
            
            
            
        
    elif flag_flujo == 1:
        #Tomando en cuenta que la empresa del movimiento puede ser tanto el emisor como el receptor de la factura entonces
        movimientos_candidatos = list(filter(lambda obj: (obj.empresa == factura.nombre_emisor or obj.empresa == factura.nombre_receptor), movimientos_candidatos))
        #Ahora filtramos al receptor y al emisor de la factura
        #Mediante el RFC y el nombre
        #Definimos los filtros a aplicar
        filtro_1 = lambda obj: obj.rfc_emisor == factura.rfc_receptor
        filtro_2 = lambda obj: obj.comprobante.rfc_emisor == factura.rfc_receptor
        filtro_3 = lambda obj: obj.nombre_emisor == factura.nombre_receptor 
        filtro_4 = lambda obj: obj.comprobante.nombre_emisor == factura.nombre_receptor
        filtro_5 = lambda obj: obj.rfc_receptor == factura.rfc_emisor
        filtro_6 = lambda obj: obj.comprobante.rfc_receptor == factura.rfc_emisor
        filtro_7 = lambda obj: obj.nombre_receptor == factura.nombre_emisor
        filtro_8 = lambda obj: obj.comprobante.nombre_receptor == factura.nombre_emisor
        filtro_9 = lambda obj: pd.isna(obj.rfc_emisor)
        filtro_10 = lambda obj: pd.isna(obj.comprobante.rfc_emisor)
        filtro_11 = lambda obj: pd.isna(obj.nombre_emisor)
        filtro_12 = lambda obj: pd.isna(obj.comprobante.nombre_emisor)
        filtro_13 = lambda obj: pd.isna(obj.rfc_receptor)
        filtro_14 = lambda obj: pd.isna(obj.comprobante.rfc_receptor)
        filtro_15 = lambda obj: pd.isna(obj.nombre_receptor)
        filtro_16 = lambda obj: pd.isna(obj.comprobante.nombre_receptor)
        
        #Aplicamos primero los filtros de emisor
        movimientos_candidatos = list(filter(lambda obj: filtro_1(obj) or filtro_2(obj) or filtro_3(obj) or filtro_4(obj) or filtro_9(obj) or filtro_10(obj) or filtro_11(obj) or filtro_12(obj), movimientos_candidatos))
        movimientos_candidatos = list(filter(lambda obj: filtro_5(obj) or filtro_6(obj) or filtro_7(obj) or filtro_8(obj) or filtro_13(obj) or filtro_14(obj) or filtro_15(obj) or filtro_16(obj), movimientos_candidatos))
        
        if len(movimientos_candidatos) == 0:
            print('No se tiene registro de movimientos emitidos o recibidos por la empresa ', factura.nombre_receptor)
            return 6, []
        
        #Ahora verificamos si es pue o ppd
        if factura.metodo_pago == 'PUE':
            #Filtramos solo las facturas que sean de monto igual o mayor al de la factura
            movimientos_candidatos = list(filter(lambda obj: obj.monto >= factura.monto, movimientos_candidatos))
            #Filtramos por fecha solo aquellas que sean del primero del mes anterior en adelante
            # Obtener la fecha del primer día del mes anterior a la fecha del objeto
            fecha_inicio = (factura.fecha_emision - timedelta(days=factura.fecha_emision.day)).replace(day=1)
            # Filtrar los objetos que cumplen con la condición
            movimientos_candidatos = [obj for obj in movimientos_candidatos if obj.fecha >= fecha_inicio]
            
            if len(movimientos_candidatos) > 1:
                #Verificamos si en la lista existe un movimiento con el monto exacto de la factura
                movimientos_exactos = list(filter(lambda obj: obj.monto == factura.monto, movimientos_candidatos))
                if len(movimientos_exactos) == 1:
                    return 5, movimientos_exactos[0]
                else:
                    return 4, movimientos_candidatos
            elif len(movimientos_candidatos) == 1:
                return 5, movimientos_candidatos[0]
            
        elif factura.metodo_pago == 'PPD':
            
            if len(movimientos_candidatos) == 1 and movimientos_candidatos[0].monto == factura.monto:
                return 5, movimientos_candidatos[0]
            elif len(movimientos_candidatos) > 1:
                movimientos_exactos = list(filter(lambda obj: obj.monto == factura.monto, movimientos_candidatos))
                if len(movimientos_exactos) == 1:
                    return 5, movimientos_exactos[0]
                elif len(movimientos_candidatos) > 4:
                    #Aquí si ejecutamos el algoritmo de búsqueda tabú con genético
                    print('Ejecutando algoritmo')
                    #Ahora ordenamos los movimientos por monto de mayor a menor
                    movimientos_candidatos = sorted(movimientos_candidatos, key=lambda movimiento: movimiento.monto, reverse=True)

                    #Definimos los hiperparametros del algoritmo
                    tam_poblacion = len(movimientos_candidatos)
                    porcentaje_mutacion = 0.5
                    global_solution = 1
                    
                    propuesta, best_fitness, worst_fitness, generacion, iteraciones_tabu = genetic_algorithm.algoritmoGeneticoHibrido(
                        tam_poblacion,
                        porcentaje_mutacion,
                        global_solution,
                        factura.monto,
                        movimientos_candidatos
                        )
                    
                    conciliacion_creada = []
                    for i in range(0, len(propuesta)):
                        if propuesta[i] == 1:
                            conciliacion_creada.append(movimientos_candidatos[i])
                            
                    return 7, conciliacion_creada
                else:
                    return 4, movimientos_candidatos    
            elif len(movimientos_candidatos) == 0:
                return 6, []
    

bandera, conciliacion = realizar_conciliacion('F4A0496C56E248E3998C8D5CDB91712A')

if bandera == 3:
    print('No fue posible realizar la conciliacion pues no hay movimientos emitidos')

if bandera == 0:
    print('No se logró hacer una conciliación, pero se encontraron los siguientes movimientos posibles: ')
    for movimiento in conciliacion:
        print('\n')
        print(movimiento.id_transaccion)
        print(movimiento.monto)
        pass
    pass
elif bandera == 1:
    print("Se ha realizado correctamente la conciliación con el movimiento: ")
    conciliacion.printMovimiento()
elif bandera == 2:
    print('Propuesta de conciliación generada por algoritmo hibrido: ')
    for movimiento in conciliacion:
        print('\n')
        print(movimiento.id_transaccion)
        pass
    pass

if bandera == 6:
    print('No fue posible realizar la conciliacion pues no hay movimientos emitidos')

if bandera == 4:
    print('No se logró hacer una conciliación, pero se encontraron los siguientes movimientos posibles: ')
    for movimiento in conciliacion:
        print('\n')
        print(movimiento.id_transaccion)
        pass
    pass
elif bandera == 5:
    print("Se ha realizado correctamente la conciliación con el movimiento: ")
    conciliacion.printMovimiento()
elif bandera == 7:
    print('Propuesta de conciliación generada por algoritmo hibrido: ')
    for movimiento in conciliacion:
        print('\n')
        print(movimiento.id_transaccion)
        pass
    pass