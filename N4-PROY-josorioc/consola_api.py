#Para correr el programa en Spyder toca instalar el paquete nest_asyncio
import nest_asyncio
#nest_asyncio.apply()
import discord
import contratos as con
from discord.ext import commands
import pandas as pd
import time





intents = discord.Intents.all()





#Instance of a bot
client = commands.Bot(command_prefix='!', intents=intents)





#first event, function decorator
"""
Un evento es código que corre cuando el bot detecta cierta actividad ocurrida.
"""




@client.event
async def on_ready():
    print('El bot está listo.')






@client.event
async def on_member_join(member):

    await member.send("""
    Bienvenid@ {0}!

    Para interactuar conmigo en el servidor ProyectoN4 Server debes utilizar el signo de exclamación "!" antes de una orden (command) SIN LAS COMILLAS,
    acuerdate de registrarte y unirte al canal de voz.

    -Primero debes registrarte, utiliza "!registrar login" para hacerlo.

    -Utiliza "!correr" para correr el Proyecto N4 de Juan José Osorio.

    - !borrar elimina mensajes en el canal de texto.

    - !cache elimina el cache y apaga al bot.

    

    -Solo los usuarios registrados pueden realizar las acciones sobre el canal de interacción con la aplicación y para unirse a un canal de voz. 

    
    """.format(member))





@client.command(aliases=["registrar login"])
async def registrar(ctx):
    """
    Para registrar al usuario.
    """

    #dataframe estudiantes

    df_estudiantes = pd.read_csv('estudiantes.csv')

    await ctx.send("Ingrese su correo uniandes")

    time.sleep(2)

    correo_input = await client.wait_for('message')

    df_estudiantes = df_estudiantes.append({"correo": str(correo_input.content), "apodo": str(correo_input.author.name), "usuario": str(correo_input.author)}, ignore_index=True)

    df_estudiantes.to_csv("estudiantes.csv", index=False)


    await ctx.send("Se ha ingresado su correo, apodo y perfil a la base de datos!")





@client.event
async def on_message(message):
    """
    Cada vez que alguien escribe un mensaje
    """
    
    

    df_estudiantes = pd.read_csv('estudiantes.csv')


    if message.author != client.user:
        

        if (str(message.author) not in df_estudiantes.usuario.tolist()) and str(message.content) != "!registrar login":
            
            await message.delete()

            await message.channel.send("No está registrado, regístrese haciendo !registrar login para enviar mensajes o utilizar al bot")
            

        elif (str(message.author) not in df_estudiantes.usuario.tolist()) and str(message.content) == "!registrar login":

            await client.process_commands(message)
        

        elif (str(message.author) in df_estudiantes.usuario.tolist()) and str(message.content) != "!registrar login":

            await client.process_commands(message)
        

        elif (str(message.author) in df_estudiantes.usuario.tolist()) and str(message.content) == "!registrar login":

            await message.delete()

            indice_lista = df_estudiantes.index[df_estudiantes["usuario"] == str(message.author)].tolist()

            await message.author.edit(nick=str(df_estudiantes.iloc[indice_lista[0]]['apodo']))





"""
Command is a piece of code that is triggered when the user tells the bot to trigger it
"""




@client.command(aliases=['sonido'])
async def sonar_grafica(ctx):
    """
    Emite un sonido en el canal de voz cuando se crea una gráfica.
    """
    channel_voz = client.get_channel(788250058818584580)
    

    if ctx.author.voice != None and str(ctx.author.voice.channel) == str(channel_voz.name):

        voice_client = await channel_voz.connect()



        voice_client.play(discord.FFmpegPCMAudio(executable="C:/ProgramData/Anaconda3/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win64-v4.2.2.exe",source='Recording.mp3'))

        

        #Para que el voice client no se desconecte
        if voice_client.is_playing() == True:


            time.sleep(5)

        await voice_client.disconnect()
    
    else:

        await ctx.send("El usuario no está en el canal de voz!")
        





#agregar () context ctx
#Para borrar los mensajes
@client.command(aliases=['borrar'])
async def clearm(ctx, amount=5):
    """
    Elimina mensajes en el canal.
    """
    await ctx.channel.purge(limit=amount)
    print(f'Se borraron {amount} mensajes.')





@client.command(aliases=['menu'])
async def mostrar_menu(ctx):
    """
    Imprime las opciones de ejecución disponibles para el usuario.
    """

    await ctx.send('''
    Opciones:
        1. Cargar el archivo de los datos registrados en el SECOP II.
        2. Consultar los contratos más costosos.
        3. Consultar los departamentos que más dinero deben de los contratos celebrados.
        4. Consultar la gráfica de los valores de los contratos por cada rama del Estado.
        5. Consultar la repartición porcentual del valor de los contratos entre las diferentes ramas del Estado.
        6. Consultar la gráfica de la distribución de los valores de los contratos.
        7. Cargar la matriz de Departamentos vs Sectores.
        8. Consultar los sectores en los que el estado invierte más o menos, de acuerdo al valor de sus contratos.
        9. Consultar el valor total de los contratos de un departamento.
        10. Consultar la gráfica con los diez departamentos con mayor gasto.
        11. Consultar el mapa de los departamentos más dedicados a un sector.
        12. Salir de la aplicación.
    ''')





@client.command(aliases=['Cargar', '1'])
async def ejecutar_cargar_datos(ctx) -> pd.DataFrame:
    """
    Solicita al usuario que ingrese el nombre de un archivo CSV con los datos registrados en el SECOP II y los carga.
    Retorno: pd.DataFrame
        El DataFrame con la información
    """
    
    await ctx.send('Ingrese el nombre del archivo (default es 2019.csv): ')
    archivo = await client.wait_for('message')

    datos = con.cargar_datos(archivo= archivo.content)
    

    await ctx.send("El archivo {0} tiene {1} filas y {2} columnas.".format(str(archivo.content), datos.shape[0], datos.shape[1]))


    return datos





@client.command(aliases=['2'])
async def ejecutar_contratos_con_mayor_valor(ctx, datos):
    """
    Ejecuta la opción de mostrar los primeros 10 contratos más costosos.
    """

    mas_costosos = con.contratos_con_mayor_valor(datos)

    for columna in mas_costosos:

        await ctx.send("\n El nombre de la columna es: {0}".format(columna))

        await ctx.send(mas_costosos[columna])





@client.command(aliases=['3'])
async def ejecutar_deuda_por_departamento(ctx, datos):
    """
    Muestra la gráfica de las 10 primeras deudas más altas por departamento.
    """


    con.deuda_por_departamento(datos)

    await ctx.invoke(client.get_command('sonido'))

    
    await ctx.send(file=discord.File('deuda_por_departamento.png'))





@client.command(aliases=['4'])
async def ejecutar_valor_total_contratos_cada_rama(ctx, datos):
    """
    Muestra la gráfica del valor total de los contratos por cada rama
    """


    await ctx.send('Ingrese el límite (un entero) inferior del rango que desea visualizar: ')
    inferior = (await client.wait_for('message'))


    await ctx.send('Ingrese el límite (un entero) superior del rango que desea visualizar: ')
    superior = (await client.wait_for('message'))

    con.valor_total_contratos_cada_rama(datos, int(inferior.content), int(superior.content))

    await ctx.invoke(client.get_command('sonido'))


    await ctx.send(file=discord.File('valor_total_contratos_cada_rama.png'))





@client.command(aliases=['5'])
async def ejecutar_reparticion_porcentual_valor_total_contratos_ramas(ctx, datos):
    """
    Muestra la gráfica de la repartición porcentual del valor total de los contratos.
    """


    con.reparticion_porcentual_valor_total_contratos_ramas(datos)

    await ctx.invoke(client.get_command('sonido'))

    await ctx.send(file=discord.File('reparticion_porcentual_valor_total_contratos_ramas.png'))





@client.command(aliases=['6'])
async def ejecutar_distribucion_valores_contratos(ctx, datos):
    """
    Muestra la gráfica de la distribución de los valores de los contratos.
    """


    con.distribucion_valores_contratos(datos)

    await ctx.invoke(client.get_command('sonido'))

    await ctx.send(file=discord.File('distribucion_valores_contratos.png'))





@client.command(aliases=['7'])
async def ejecutar_construccion_matriz_departamentos_vs_sectores(ctx, datos):
    """
    Ejecuta la construcción de la matriz de departamentes vs sectores.
    Retorno:
        Una lista que es la matriz.
    """


    matriz = con.construccion_matriz_departamentos_vs_sectores(datos)

    await ctx.send('Cargue de matriz: EXITOSO')

    return matriz





@client.command(aliases=['8'])
async def ejecutar_sectores_invierte_mas_menos(ctx, matriz):
    """
    Ejecuta la opción de mostrarle al usuario los sectores en los que el estado invierte más o menos.
    """

    await ctx.send("Desea conocer el sector de mayor o menor gasto (escriba 'mayor' o 'menor'):")

    indicador = await client.wait_for('message')

    if str(indicador.content).lower() == 'menor' or str(indicador.content).lower() == 'mayor':

        tupla = con.sectores_invierte_mas_menos(matriz, str(indicador.content))

        await ctx.send("El nombre del sector con {0} gasto es {1} con un valor total de: {2}".format(str(indicador.content), tupla[0], tupla[1]))

    else:
        await ctx.send("Ese indicador no es válido. Asegúrese de escribir 'mayor' o 'menor'.")





@client.command(aliases=['9'])
async def ejecutar_valor_total_contratos_departamento(ctx, matriz, datos):
    """
    Ejecuta la opción de ver el valor total de los contratos de un departamento

    Recibe el DataFrame para revisar que el departamento exista, ya que es más rápido que hacer un loop según la matriz.
    """


    lista_con_departamentos = datos['Departamento'].unique().tolist()

    await ctx.send("Los departamentos disponibles son:")

    for dep in lista_con_departamentos:

        await ctx.send("-{0}".format(str(dep)))





    await ctx.send('Ingrese el nombre del departamento que desea:')

    departamento = await client.wait_for('message')






    if con.valor_total_contratos_departamento(matriz, str(departamento.content)) != 0 or departamento in lista_con_departamentos:

        await ctx.send("El valor total de los contratos de {0} es: {1}". format(str(departamento.content), con.valor_total_contratos_departamento(matriz, str(departamento.content))))

    else:
        await ctx.send('El departamento no se encuentra en la matriz.')





@client.command(aliases=['10'])
async def ejecutar_departamentos_mayor_gasto(ctx, matriz):
    """
    Ejecuta la opción de mostrar la gráfica con los departamentos con mayor gasto.
    """


    diccionario_departamentos = con.departamentos_mayor_gasto(matriz)

    con.grafica_departamentos_mayor_gasto(diccionario_departamentos)

    await ctx.invoke(client.get_command('sonido'))

    await ctx.send(file=discord.File('grafica_departamentos_mayor_gasto.png'))





@client.command(aliases=['11'])
async def ejecutar_departamentos_mas_dedicados_sector(ctx, matriz):
    """
    Ejecuta la opción de mostrar la ubicación en el mapa de los departamentos más dedicados a un sector en particular.

    Recibe el DataFrame para revisar que el sector exista, ya que es más rápido que hacer un loop según la matriz.
    """
    

    await ctx.send("Los sectores disponibles son: ")

    for sector in matriz[0]:

        await ctx.send("-{0}".format(sector))


    await ctx.send('Ingrese el sector de interés exactamente como aparece:')

    #Evitar error
    sector_interes = None
    sector_interes = await client.wait_for('message')

    




    if str(sector_interes.content) not in matriz[0]:

        await ctx.send('El sector no se encuentra en la matriz')
    
    else:

        #Para que no salga error
        diccionario_departamentos_mas_dedicados = None

        diccionario_departamentos_mas_dedicados = con.departamentos_mas_dedicados_sector(matriz, str(sector_interes.content))
        print(diccionario_departamentos_mas_dedicados)


        
        await ctx.send('Ingrese EXACTAMENTE el nombre del archivo con el mapa de los departamentos (default: mapa.png):')
        time.sleep(2)
        

        archivo_imagen = await client.wait_for('message')

        lista_imagen = None
        


        #Para el error
        

        lista_imagen = con.cargar_imagen_como_matriz(str(archivo_imagen.content).replace(" ",""))

        

        #lista_imagen = con.cargar_imagen_como_matriz('mapa.png')

        print(len(lista_imagen))
        
        await ctx.send('Ingrese EXACTAMENTE el nombre del archivo con las coordenadas de los departamentos (default: coordenadas.txt): ')

        time.sleep(2)


        archivo_coordenadas = await client.wait_for('message')


        #Error
        dict_coordenadas = None
        dict_coordenadas = con.cargar_coordenadas(str(archivo_coordenadas.content).replace(" ",""))
        

        #dict_coordenadas = con.cargar_coordenadas('coordenadas.txt')
        print(dict_coordenadas)




        con.pintar_cuadrados_imagen(coordenadas= dict_coordenadas, departamentos= diccionario_departamentos_mas_dedicados, matriz= lista_imagen)

        await ctx.invoke(client.get_command('sonido'))

        await ctx.send(file=discord.File('pintar_cuadrados_imagen.png'))





@client.command(aliases=['clear', 'cache', 'off'])
async def cache_todo(ctx):
    """
    Borra el cache y apaga al Bot.
    """

    client.clear()

    await ctx.send("Se borró el Cache")

    await ctx.send("Se apagó la conexión entre el Bot y el Servidor.")
    await client.close()





@client.command(aliases=['correr'])
async def iniciar_apliacion(ctx):
    """
    Ejecuta el programa para el usuario
    """


    continuar = True

    datos = None

    matriz = None


    while continuar:

        await ctx.invoke(client.get_command('menu'))

        await ctx.send('\n Seleccione una opción')
        ingreso =  await client.wait_for('message')

        opcion_usuario = str(ingreso.content)


        if opcion_usuario == '1':

            datos = await ctx.invoke(client.get_command('1'))
        

        elif opcion_usuario == '2':
            await ctx.invoke(client.get_command('2'), datos=datos)
        

        elif opcion_usuario == '3':

            await ctx.invoke(client.get_command('3'), datos = datos)
        

        elif opcion_usuario == '4':
            await ctx.invoke(client.get_command('4'), datos = datos)
        

        elif opcion_usuario == '5':

            await ctx.invoke(client.get_command('5'), datos = datos)


        elif opcion_usuario == '6':
            await ctx.invoke(client.get_command('6'), datos = datos)


        elif opcion_usuario == '7':

            matriz = await ctx.invoke(client.get_command('7'), datos = datos)
        

        elif opcion_usuario == '8':
          
            await ctx.invoke(client.get_command('8'), matriz= matriz)
        

        elif opcion_usuario == '9':
            
            await ctx.invoke(client.get_command('9'), matriz= matriz, datos = datos)
        

        elif opcion_usuario == '10':
           
            await ctx.invoke(client.get_command('10'), matriz= matriz)
        

        elif opcion_usuario == '11':
           
            await ctx.invoke(client.get_command('11'), matriz= matriz)
       

        elif opcion_usuario == '12':
            
            continuar = False
            

            await ctx.send('Terminó el loop!')
            
        
        else:

            await ctx.send("Por favor seleccione una opción válida.")





#Pasar el token
client.run('Nzg4MjQ3OTE4OTIyNTYzNTg0.X9gvFA.gHO70Uq5ICWoEbDG9P8bA3HONsY')