import pandas as pd
from matplotlib import pyplot as plt 
from matplotlib import image as mpimg



def cargar_datos(archivo: str) -> pd.DataFrame:
    """
    Parte 1 - Requerimiento 0 - Cargar Datos: Crea un DataFrame del archivo CSV.
    
    Recibe como parametro el nombre del archivo CSV y retorna un DataFrame.
    """

    #Se utiliza read_csv para crear el DataFrame
    datos = pd.read_csv(archivo)


    return datos



def cinco_modalidades_mayor_cantidad_contratos(datos: pd.DataFrame, indice: int) -> pd.DataFrame:



    mayor_indice = datos.loc[(datos.ValordelContrato > indice) & (datos.EsGrupo == True), ['ModalidaddeContratacion', 'EsGrupo']]


    contados = mayor_indice.groupby('ModalidaddeContratacion')['EsGrupo'].value_counts().to_frame('counts')

    ordenados = contados.sort_values(by=['counts'], ascending=False)

    
    

    return ordenados[['counts']].iloc[:5]



print(cinco_modalidades_mayor_cantidad_contratos(cargar_datos('2019.csv'), 0))


def box_tipo_contrato(datos: pd.DataFrame, inferior: int, superior: int) -> None:

    
    rango = datos.loc[(datos.ValordelContrato >= inferior) & (datos.ValordelContrato <= superior), ['TipodeContrato', 'ValordelContrato']]
    
    
    nuevo_index = rango.set_index('TipodeContrato')

    nuevo_index.boxplot(by='TipodeContrato', column=['ValordelContrato'])
    
    plt.title('Valor de contratos por tipo de contrato')
    plt.xticks(rotation=90)
    plt.ylabel('Valor del Contrato')
    plt.show()
    






def scatter_valores(datos: pd.DataFrame, inferior: int, superior: int) -> None:

    rango_contrato = datos.loc[(datos.ValordelContrato >= inferior) & (datos.ValordelContrato <= superior), ['ValordelContrato', 'ValorPendientedePago', 'ValorPagado']]

    rango_pendiente = rango_contrato.loc[(rango_contrato.ValorPendientedePago >= inferior) & (rango_contrato.ValorPendientedePago <= superior), ['ValordelContrato', 'ValorPendientedePago', 'ValorPagado']]

    rango_pagado = rango_pendiente.loc[(rango_pendiente.ValorPagado >= inferior) & (rango_pendiente.ValorPagado <= superior), ['ValordelContrato', 'ValorPendientedePago', 'ValorPagado']]


    contrato = rango_pagado.plot(kind='scatter', x='ValordelContrato', y='ValorPagado', color='b', label='Total vs Pagado')

    pagado = rango_pagado.plot(kind='scatter', x='ValordelContrato', y='ValorPendientedePago', color='g', ax = contrato, label = 'Total vs Pendiente')

    

    plt.show()
    return rango_pagado

#print(scatter_valores(cargar_datos('2019.csv'), 1, 50))

def dar_base_bandera()->list:
    bandera=[]

    for i in range(300):
        fila =[]

        for j in range(300):
            fila.append([0]*3)
        
        bandera.append(fila)
    
    return bandera





def bandera_casanare() ->list:

    matriz = dar_base_bandera()

    colores = {
        'rojo': [218, 18, 26],
        'verde': [7, 137, 48],
        'amarillo': [252, 221, 9]
    }

    for x in range(len(matriz)):

        for y in range(len(matriz[0])):

            matriz[x][y] = colores['rojo']

    for x in range(len(matriz)//2):

        for y in range(len(matriz[0])//2):

            matriz[-x][-y] = colores['verde']

    return matriz



def pintar_bandera(bandera:list) -> None:
    

    plt.imshow(bandera)
    plt.show()

#pintar_bandera(bandera_casanare())