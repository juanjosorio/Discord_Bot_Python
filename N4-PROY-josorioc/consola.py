"""
Proyecto N4
@author: j.osorioc@uniandes.edu.co
"""

import contratos_terminal as con

#Se importa pandas para mostrar que ejecutar_cargar_datos retorna un DataFrame y que algunas funciones reciben un DataFrame.
import pandas as pd





def ejecutar_cargar_datos() -> pd.DataFrame:
    """
    Solicita al usuario que ingrese el nombre de un archivo CSV con los datos registrados en el SECOP II y los carga.
    Retorno: pd.DataFrame
        El DataFrame con la información
    """

    archivo = input("Por favor ingrese el nombre del archivo CSV con los datos registrados en el SECOP II: ")

    datos = con.cargar_datos(archivo)

    if len(datos) == 0:

        #Si el archivo está en el directorio pero no es válido.
        print("El archivo seleccionado no es valido.")
    
    else:

        #Se le avisa al usuario que el archivo ha sido cargado y se le muestra una breve descripción de él.
        print("El archivo que cargó exitosamente \n", datos)
        

    return datos





def ejecutar_contratos_con_mayor_valor(datos: pd.DataFrame)-> None:
    """
    Ejecuta la opción de mostrar los primeros 10 contratos más costosos.
    """

    mas_costosos = con.contratos_con_mayor_valor(datos)


    print("Los contratos más costosos son los siguientes: \n", mas_costosos)

    



def ejecutar_deuda_por_departamento(datos: pd.DataFrame) -> None:
    """
    Muestra la gráfica de las 10 primeras deudas más altas por departamento.
    """

    con.deuda_por_departamento(datos)





def ejecutar_valor_total_contratos_cada_rama(datos: pd.DataFrame) -> None:
    """
    Muestra la gráfica del valor total de los contratos por cada rama
    """

    inferior = int(input('Ingrese el límite (un entero) inferior del rango que desea visualizar: '))

    superior = int(input('Ingrese el límite (un entero) superior del rango que desea visualizar: '))

    con.valor_total_contratos_cada_rama(datos, inferior, superior)





def ejecutar_reparticion_porcentual_valor_total_contratos_ramas(datos: pd.DataFrame) -> None:
    """
    Muestra la gráfica de la repartición porcentual del valor total de los contratos.
    """

    con.reparticion_porcentual_valor_total_contratos_ramas(datos)





def ejecutar_distribucion_valores_contratos(datos: pd.DataFrame) -> None:
    """
    Muestra la gráfica de la distribución de los valores de los contratos.
    """

    con.distribucion_valores_contratos(datos)





def ejecutar_construccion_matriz_departamentos_vs_sectores(datos: pd.DataFrame) -> list:
    """
    Ejecuta la construcción de la matriz de departamentes vs sectores.
    Retorno:
        Una lista que es la matriz.
    """

    matriz = con.construccion_matriz_departamentos_vs_sectores(datos)
    
    print('Cargue de matriz: EXITOSO')

    return matriz





def ejecutar_sectores_invierte_mas_menos(matriz: list) -> None:
    """
    Ejecuta la opción de mostrarle al usuario los sectores en los que el estado invierte más o menos.
    """

    indicador = input("Desea conocer el sector de mayor o menor gasto (escriba 'mayor' o 'menor'): ")


    if indicador.lower() == 'menor' or indicador.lower() == 'mayor':

        tupla = con.sectores_invierte_mas_menos(matriz, indicador)

        print('El nombre del sector con', indicador, 'gasto es', tupla[0], 'con un valor total de: ', tupla[1])


    else:
        print("Ese indicador no es válido. Asegúrese de escribir 'mayor' o 'menor'." )
        




def ejecutar_valor_total_contratos_departamento(matriz: list, datos: pd.DataFrame) -> None:
    """
    Ejecuta la opción de ver el valor total de los contratos de un departamento

    Recibe el DataFrame para revisar que el departamento exista, ya que es más rápido que hacer un loop según la matriz.
    """

    lista_con_departamentos = datos['Departamento'].unique().tolist()
    

    departamento = input('Ingrese el nombre del departamento que desea: ')
    

    #Condiciones para ver si el departamento está en la matriz (que fue creada con  .unique() y .tolist()). Se pone el or por si la suma del departamento da 0 pero sí está en la matriz.
    if con.valor_total_contratos_departamento(matriz, departamento) != 0 or departamento in lista_con_departamentos:
    
        print('El valor total de los contratos de', departamento.capitalize(), 'es: ', con.valor_total_contratos_departamento(matriz, departamento))
    
    else:

        print('El departamento no se encuentra en la matriz.')





def ejecutar_departamentos_mayor_gasto(matriz: list) -> None:
    """
    Ejecuta la opción de mostrar la gráfica con los departamentos con mayor gasto.
    """

    diccionario_departamentos = con.departamentos_mayor_gasto(matriz)

    con.grafica_departamentos_mayor_gasto(diccionario_departamentos)





def ejecutar_departamentos_mas_dedicados_sector(matriz: list, datos: pd.DataFrame) -> None:
    """
    Ejecuta la opción de mostrar la ubicación en el mapa de los departamentos más dedicados a un sector en particular.

    Recibe el DataFrame para revisar que el sector exista, ya que es más rápido que hacer un loop según la matriz.
    """

    lista_sectores = datos['Sector'].unique().tolist()


    sector_interes = input('Ingrese el sector de interés exactamente como aparece: ')

    if sector_interes not in lista_sectores:

        print('El sector no se encuentra en la matriz.')
    
    else:

        #Diccionario con los departamentos más dedicados
        diccionario_departamentos_mas_dedicados = con.departamentos_mas_dedicados_sector(matriz, sector_interes)


        #Cargar la matriz con la imagen del mapa
        archivo_imagen = input('Ingrese EXACTAMENTE el nombre del archivo con el mapa de los departamentos: ')

        lista_imagen = con.cargar_imagen_como_matriz(archivo_imagen)


        #Cargar el dict con las coordenadas de los departamentos
        archivo_coordenadas = input('Ingrese EXACTAMENTE el nombre del archivo con las coordenadas de los departamentos: ')

        dict_coordenadas = con.cargar_coordenadas(archivo_coordenadas)


        #Mostrar la gráfica
        con.pintar_cuadrados_imagen(coordenadas=dict_coordenadas, departamentos=diccionario_departamentos_mas_dedicados, matriz=lista_imagen)





def mostrar_menu():
    """
    Imprime las opciones de ejecución disponibles para el usuario.
    """

    print('\nOpciones:')
    print('1. Cargar el archivo de los datos registrados en el SECOP II.')
    print('2. Consultar los contratos más costosos.')
    print('3. Consultar los departamentos que más dinero deben de los contratos celebrados.')
    print('4. Consultar la gráfica de los valores de los contratos por cada rama del Estado.')
    print('5. Consultar la repartición porcentual del valor de los contratos entre las diferentes ramas del Estado.')
    print('6. Consultar la gráfica de la distribución de los valores de los contratos.')
    print('7. Cargar la matriz de Departamentos vs Sectores.')
    print('8. Consultar los sectores en los que el estado invierte más o menos, de acuerdo al valor de sus contratos.')
    print('9. Consultar el valor total de los contratos de un departamento.')
    print('10. Consultar la gráfica con los diez departamentos con mayor gasto.')
    print('11. Consultar el mapa de los departamentos más dedicados a un sector.')
    print('12. Salir de la aplicación.')





def iniciar_aplicacion():
    """
    Ejecuta el programa para el usuario
    """

    continuar = True

    datos = None

    matriz = None

    while continuar:
        mostrar_menu()

        opcion_seleccionada = int(input('Por favor seleccione una opción: '))

        if opcion_seleccionada == 1:
            datos = ejecutar_cargar_datos()
        
        elif opcion_seleccionada == 2:

            ejecutar_contratos_con_mayor_valor(datos)
        
        elif opcion_seleccionada == 3:

            ejecutar_deuda_por_departamento(datos)
        
        elif opcion_seleccionada == 4:

            ejecutar_valor_total_contratos_cada_rama(datos)
        
        elif opcion_seleccionada == 5:

            ejecutar_reparticion_porcentual_valor_total_contratos_ramas(datos)
        
        elif opcion_seleccionada == 6:

            ejecutar_distribucion_valores_contratos(datos)
        
        elif opcion_seleccionada == 7:

            matriz = ejecutar_construccion_matriz_departamentos_vs_sectores(datos)
        
        elif opcion_seleccionada == 8:

            ejecutar_sectores_invierte_mas_menos(matriz)
        
        elif opcion_seleccionada == 9:

            ejecutar_valor_total_contratos_departamento(matriz, datos)
        
        elif opcion_seleccionada == 10:

            ejecutar_departamentos_mayor_gasto(matriz)
        
        elif opcion_seleccionada == 11:

            ejecutar_departamentos_mas_dedicados_sector(matriz, datos)
        
        elif opcion_seleccionada == 12:

            continuar = False
        
        else:

            print("Por favor seleccione una opción válida.")





# PROGRAMA PRINCIPAL
iniciar_aplicacion()