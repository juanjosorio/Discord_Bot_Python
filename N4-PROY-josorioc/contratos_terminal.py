import pandas as pd
from matplotlib import pyplot as plt 
from matplotlib import image as mpimg

"""
PARTE 1
"""


def cargar_datos(archivo: str) -> pd.DataFrame:
    """
    Parte 1 - Requerimiento 0 - Cargar Datos: Crea un DataFrame del archivo CSV.
    
    Recibe como parametro el nombre del archivo CSV y retorna un DataFrame.
    """

    #Se utiliza read_csv para crear el DataFrame
    datos = pd.read_csv(archivo)


    return datos


"""
PARTE 2
"""


def contratos_con_mayor_valor(datos: pd.DataFrame) -> pd.DataFrame:
    """
    Parte 2-  Requerimiento 1 - Contratos más costosos: Recibe como parámetro un DataFrame.
    
    Consulta los contratos con mayor valor según la columna ValordelContrato.
    
    Retorna un DataFrame con los primeros 10 valores de ValordelContrato, con las columnas
    'NombreEntidad', 'Departamento', 'ProveedorAdjudicado', 'ValordelContrato'.
    """

    #Se organiza basado en la columna ValordelContrato
    datos.sort_values(by="ValordelContrato", ascending=False, inplace=True)

    return datos[['NombreEntidad', 'Departamento', 'ProveedorAdjudicado', 'ValordelContrato']].iloc[:10]






def deuda_por_departamento(datos: pd.DataFrame) -> None:
    """
    Parte 2 - Requerimiento 2 - Deuda por departamento: Recibe como parámetro un DataFrame, crea una gráfica de ValorPendientedePago.
    
    Genera una gráfica que da a conocer cuáles son los departamentos que más dinero deben de los contratos celebrados.
    
    Retorna un None. Muestra la gráfica.
    """
    
    #Cada departamento obtiene el valor de la suma de todos sus ValorPendientedePago
    datos = datos.groupby('Departamento')['ValorPendientedePago'].sum().reset_index()


    #Se organizan los valores de ValorPendientedePago de mayor a menor
    datos.sort_values(by='ValorPendientedePago', ascending=False, inplace=True)


    #Se cogen las diez primeras filas
    datos_iloc = datos.iloc[:10].copy()


    #ValorPendientedePago se organiza de menor a mayor
    datos_iloc.sort_values(by='ValorPendientedePago', inplace=True)

    #se hace plot a las dos columnas
    datos_iloc.plot.barh(y='ValorPendientedePago',
    x='Departamento',
    title='Departamentos más deudores',
    legend=None,
    figsize=(10,10))


    #Se ajusta la ubicación del xlabel y ylabel
    plt.subplots_adjust(bottom=.25, left=.25)


    plt.xlabel('Valor pendiente de pago', fontsize=12)
    
    
    plt.ylabel('Departamento', fontsize=12)


    #Se muestra el gráfico
    plt.show()

    #plt.savefig('deuda_por_departamento.png')


"""
PARTE 3
"""


def valor_total_contratos_cada_rama(datos: pd.DataFrame, inferior: int, superior: int)-> None:
    """
    Parte 3 - Requerimiento 3 - Valor total de los contratos por cada rama: Recibe un DataFrame, y dos ints.
    
    Genera una gráfica que permite relacionar el valor total de los contratos y la rama que los celebró.
    
    Retorna un None. Muestra la gráfica.
    """
    
    
    diccionario = {}
    

    #Por cada rama
    for rama in datos['Rama'].unique():


        #Se crea un nuevo DataFrame con una columna que contiene los datos de la rama
        nuevos_datos = datos.loc[datos['Rama'] == rama].copy()
  

        #Se calculan los valores entre los intervalos      
        valores_nuevos = nuevos_datos.query('{0} <= ValordelContrato <= {1}'.format(inferior, superior)).copy()

        
        valores_nuevos[rama] = valores_nuevos.loc[:,'ValordelContrato']
        

        #Se crea una lista con los valores de valores_nuevos['ValordelContrato']
        lista = valores_nuevos['ValordelContrato'].tolist()


        #Se agrega la lista al diccionario
        diccionario[rama] = lista
    
    
    #Se crea la gráfica
    fig, ax = plt.subplots()

    ax.boxplot(diccionario.values())
    
    ax.set_xticklabels(diccionario.keys())
    
    plt.title('Valor de contratos por Rama')
    
    plt.xlabel('Rama contratadora')
    
    plt.ylabel('Valor del Contrato')

    plt.grid(True)
    
    #Se muestra la gráfica
    plt.show()
    #plt.savefig('valor_total_contratos_cada_rama.png')





def reparticion_porcentual_valor_total_contratos_ramas(datos: pd.DataFrame) -> None:
    """
    Parte 3 - Requerimiento 4 - Repartición porcentual del valor total de los contratos: Recibe como parámetro un DataFrame. 
    
    Genera una gráfica de tipo pie que muestra la repartición porcentual del valor total de los contratos del Estado entre las diferentes ramas que los celebran.
    
    
    Retorna un None. Muestra la gráfica.
    """

    #Cada rama obtiene el valor de la suma de sus ValordelContrato
    datos = datos.groupby('Rama')['ValordelContrato'].sum().reset_index()
    

    #Se crea la gráfica
    datos.plot.pie(y='ValordelContrato', figsize=(8,8), labels=datos['Rama'], shadow=False, autopct="%1.1f%%", legend=False)
    
    
    plt.title('Distribución de valor de contratos por Rama')


    #Se muestra
    plt.show()
    #plt.savefig('reparticion_porcentual_valor_total_contratos_ramas.png')





def distribucion_valores_contratos(datos: pd.DataFrame) -> None:
    """
    Parte 3 - Requerimiento 5 - Distribución de los valores de los contratos: Recibe como parámetro un DataFrame.
    
    Genera una gráfica de tipo KDE teniendo en cuenta los valores de la columna ValordelContrato.
    
    Retorna un None. Muestra la gráfica.
    """


    #Se eliminan los valores en ValordelContrato que sean menores que 100, se guarda el nuevo DataFrame en una variable
    nuevos_datos = datos[datos['ValordelContrato'] < 100]

    
    #Se crea la gráfica
    nuevos_datos.plot.kde(y = 'ValordelContrato',xlim=(0,100), legend=False)
    
    plt.title('Distribución de los valores de los contratos')
    
    plt.xlabel('Valor Contrato')
    
    plt.ylabel('Densidad de Probabilidad')
    
    
    #Se muestra la gráfica
    plt.show()
    #plt.savefig('distribucion_valores_contratos.png')

"""
Parte 4
"""


def construccion_matriz_departamentos_vs_sectores(datos: pd.DataFrame) -> list:
    """
    Parte 4 - Requerimiento 6 - Construcción de la matriz de departamentes vs sectores: Recibe como parámetro un DataFrame.
    
    Construye una matriz que cruza los departamentos con los sectores.
    
    Retorna una lista.
    """

    #Filtro
    datos = datos[datos.Departamento != "No Definido"]


    matriz = []

    #Lista con los sectores del DataFrame
    sectores = datos['Sector'].unique().tolist()
    sectores.insert(0, 'Departamentos vs Sectores')


    matriz.append(sectores)



    #Lista con los departamentos del DataFrame
    departamentos = datos['Departamento'].unique().tolist()
    departamentos.insert(0, None)


    #[1:] porque el índice 0 es None
    for departamento in departamentos[1:]:


        lista = [departamento]
        
        
        for sector in sectores[1:]:
            

            #Se suman todos los ValordelContrato cuando Departamento == departamento y Sector a sector
            valor = datos.query("Departamento == '{0}' and Sector == '{1}'".format(departamento, sector))['ValordelContrato'].sum()
            lista.append(valor)


        #Se agrega la lista a la matriz
        matriz.append(lista)
    
    return matriz        





def sectores_invierte_mas_menos(matriz: list, indicador: str) -> tuple:
    """
    Parte 4 - Requerimiento 7 - Sectores en los que el estado invierte más o menos: Recibe una matriz y un indicador (str) diciendo si quiere ver el mayor o el menor Sector.

    Calcula en cuáles sectores el estado ha gastado más y menor dinero teniendo en cuenta todos los contratos celebrados en cada sector.

    Retorna un tuple con el nombre del sector y la suma total de la plata invertida en él.
    """

    tupla =()

    diccionario={}


    #Por cada índice en el len matriz[0][1:]
    for indice in range(len(matriz[0][1:])):

        suma=0


        #Por cada fila
        for fila in matriz[1:]:


            if indice+1 <= len(fila):


                suma += fila[indice+1]
        

        diccionario[indice] = suma
    

    #Se calcula la llave del diccionario con el máximo valor
    maximo = max(diccionario, key=diccionario.get)

    #Se calcula la llave del diccionario con el mínimo valor
    minimo = min(diccionario, key=diccionario.get)


    if indicador.lower() == 'menor':


        tupla = (matriz[0][minimo+1], diccionario[minimo])
        
    
    elif indicador.lower() == 'mayor':


        tupla = (matriz[0][maximo+1], diccionario[maximo])
        

    return tupla





def valor_total_contratos_departamento(matriz: list, departamento: str) -> float:
    """
    Parte 4 - Requerimiento 8 - Valor total de los contratos de un departamento: Recibe como parámetro una matriz y un str(departamento).
    
    Calcula el valor total de los contratos de un departamento a partir de la matriz.
    
    Retorna la suma de los contratos de ese departamento.
    """
    suma = 0

    for fila in matriz[1:]:


        #Si el primer valor de la fila es igual al departamento
        if fila[0].lower() == departamento.lower():


            #Se suma el valor de cada indice de la fila
            for valor in fila[1:]:


                suma += valor    

    return suma





def departamentos_mayor_gasto(matriz: list) -> dict:
    """
    Parte 4 - Requerimiento 9 - Departamento con mayor gasto: Recibe como parámetro una matriz.
    
    Muestra cuáles son los 10 departamentos que tienen un mayor gasto.
    
    Retorna un dict con los diez departamentos con mayor gasto.
    """


    valores_iniciales_dict = {}


    for fila in matriz[1:]:


        #Agregan al dict
        valores_iniciales_dict[fila[0]] = valor_total_contratos_departamento(matriz, fila[0])
    

    #Se crea una lista con las llaves de valores_iniciales_dict en orden según sus valores
    ordenado = sorted(valores_iniciales_dict, key=valores_iniciales_dict.get, reverse=True)


    mayor_gasto ={}


    #Diez primeros departamentos
    for departamento in ordenado[:10]:


        #Agregan a mayor_gasto
        mayor_gasto[departamento] = valores_iniciales_dict[departamento]
    

    return mayor_gasto





def grafica_departamentos_mayor_gasto(diccionario: dict) -> None:
    """
    Parte 4 - Requerimiento 9 - Mostrar gráfica de departamentos_mayor_gasto. Recibe un dict como parámetro.
    
    Muestra la gráfica de los 10 departamentos que tienen un mayor gasto.

    Retorna un None. Muestra la gráfica.
    """

    datos_df = pd.DataFrame.from_dict(diccionario, orient='index', columns=['Gasto'])


    #figsize=(6,8) para que quede similar al del documento (pdf)
    datos_df.plot(kind='bar',
    xlabel='Departamento',
    ylabel='Valor total de contratos',
    title='Departamentos con mayor gasto',
    figsize=(6,8)
    )


    #Se ajusta es subplot de abajo para que quepa el ylabel
    plt.subplots_adjust(bottom=.5)


    #Se muestra la gráfica
    plt.show()
    #plt.savefig('grafica_departamentos_mayor_gasto.png')




def departamentos_mas_dedicados_sector(matriz: list, sector_interes: str) -> dict:
    """
    Parte 4 - Requerimiento 10: Departamentos más dedicados a un sector. Recibe como parámetros una matriz (list) y  un str (sector_interes).
    
    Calcula los 5 departamentos más dedicados a un sector.

    Retorna un dict.
    """


    dict_sector_indice = {}


    #Se calcula el índice de cada Sector
    for indice in range(len(matriz[0][1:])):


        dict_sector_indice[matriz[0][indice+1]] = indice+1


    gasto_sector_dict = {}
    
    
    #Se calcula la dedicación de un departamento a un sector, se agrega a gasto_sector_dict
    for fila in matriz[1:]:


        gasto_sector = (fila[dict_sector_indice[sector_interes]]*100) / valor_total_contratos_departamento(matriz, fila[0])


        gasto_sector_dict[fila[0]] = gasto_sector


    #Se ordena gasto_secor_dict según los valores de las llaves de mayor a menor
    ordenado = sorted(gasto_sector_dict, key=gasto_sector_dict.get, reverse=True)


    mas_dedicados={}


    #Se sacan las primeras 5 llaves
    for departamento in ordenado[:5]:


        mas_dedicados[departamento] = gasto_sector_dict[departamento]


    return mas_dedicados






def cargar_imagen_como_matriz(archivo: str) -> list:
    """
    Función para cargar imagen como matriz (lista). Recibe como parámetro un str.
    
    Carga el mapa como una matriz de pixeles.
    
    Retorna una lista.
    """

    #Carga el mapa como una matriz de pixeles.
    mapa = mpimg.imread(archivo).tolist()

    return mapa





def cargar_coordenadas(nombre_archivo:str)->dict:
    """
    Función para cargar las coordenadas de los departamentos. Recibe como parámetro un str.
    
    Crea un dict con las coordenadas de cada departamento en el mapa.

    Retorna un dict con las coordenadas en un tuple.
    """


    deptos = {}
    
    
    archivo = open(nombre_archivo, encoding="utf8")
    
    
    titulos = archivo.readline()
    
    
    linea = archivo.readline()
    
    
    while len(linea) > 0:
    
        linea = linea.strip()
        
        datos = linea.split(";")
        
        deptos[datos[0]] = (int(datos[1]),int(datos[2]))
        
        linea = archivo.readline()
    
    archivo.close()
    return deptos





def pintar_cuadrados_imagen(coordenadas: dict, departamentos: dict, matriz: list) -> None:
    """
    Función para pintar en el mapa los 5 departamentos más dedicados al sector. Recibe los departamentos (dict), sus coordenadas (dict), y una matriz (list).
    
    Carga la imagen de los departamentos más dedicados a un sector teniendo en cuenta una matriz con los pixeles.
    
    Retorna un None y muestra la gráfica.
    """

    tabla_colores ={
        0: [0.94, 0.10, 0.10],
        1: [0.94, 0.10, 0.85],
        2: [0.10, 0.50, 0.94],
        3: [0.34, 0.94, 0.10],
        4: [0.99, 0.82, 0.09]
    }

    #índice para la tabla
    indice = 0


    for departamento in departamentos:


        if departamentos[departamento] != 0:


            #Coordenadas del departamento
            x, y = coordenadas[departamento]


            #Para crear el cuadrado y que sea similiar al del documento (pdf), se utiliza -6 y +6 en ambos ejes.
            for i in range(x-6, x+6):
                
                
                for j in range(y-6, y+6):


                    #Se cambia el color de esos lugares en la matriz
                    matriz[i][j] = tabla_colores[indice]
        

        indice += 1
    

    #Se crea y muestra la gráfica
    plt.imshow(matriz)


    plt.show()    
    #plt.savefig('pintar_cuadrados_imagen.png')