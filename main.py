import pandas as pd
import preprocesamiento
import filtro
import genetic_algorithm
import funcion

print('Bienvenido a la primera prueba de conciliación automática con búsqueda tabú')

#Primero vamos a abrimos todos los datasets
movimientos = pd.read_csv('Data/movimientos.csv')
facturasCxC = pd.read_csv('Data/reportCXC_20231113.csv')
facturasCxP = pd.read_csv('Data/reportCXP_20231113.csv')

#Procedemos a limpiar la información y a guardarlo en los datasets correspondientes
cuentas_por_cobrar = preprocesamiento.clean_cuentas(facturasCxC)
cuentas_por_pagar = preprocesamiento.clean_cuentas(facturasCxP)
ingresos, egresos = preprocesamiento.clean_movimientos(movimientos)

#Solicitamos al usuario el UUID de la factura a conciliar
uuidFactura = input("Ingrese el uuid de la factura que desea conciliar: ")

#Ahora buscamos la el uuid en las cuentas por pagar y por cobrar
resultado_cuentas_pp = list(filter(lambda obj: obj.uuid == uuidFactura, cuentas_por_pagar))
resultado_cuentas_pc = list(filter(lambda obj: obj.uuid == uuidFactura, cuentas_por_cobrar))

factura = None
movimientos_candidatos = None
flag_flujo = 0

if resultado_cuentas_pp:
    factura = resultado_cuentas_pp[0]
    movimientos_candidatos = egresos
    flag_flujo = 1
    
if resultado_cuentas_pc:
    factura = resultado_cuentas_pc[0]
    movimientos_candidatos = ingresos
    
factura.showFactura()

#Ahora aplicamos los filtros para definir el espacio de búsqueda
movimientos_candidatos = filtro.filtrar_por_tipo(factura.metodo_pago, factura.monto, movimientos_candidatos)
movimientos_candidatos = filtro.filtrar_por_cuenta(factura, flag_flujo, movimientos_candidatos)
movimientos_candidatos = filtro.filtrar_por_fecha(factura.metodo_pago, factura.fecha_emision, movimientos_candidatos)

#Ahora ordenamos los movimientos por monto de mayor a menor
movimientos_candidatos = sorted(movimientos_candidatos, key=lambda movimiento: movimiento.monto, reverse=True)

tam_poblacion = len(movimientos_candidatos)
porcentaje_mutacion = 0.16

global_solution = 1

propuesta, best_fitness, worst_fitness, generacion, iteraciones_tabu = genetic_algorithm.algoritmoGeneticoHibrido(
      tam_poblacion,
      porcentaje_mutacion,
      global_solution,
      factura.monto,
      movimientos_candidatos
      )

print(propuesta)
for i in range(0, len(propuesta)):
    if propuesta[i] == 1:
        movimientos_candidatos[i].printMovimiento()








