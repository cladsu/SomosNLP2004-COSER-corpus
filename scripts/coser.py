import pandas as pd
import matplotlib.pyplot as plt
import re

# Función para cargar un archivo CSV en un DataFrame
def csv2Df(archivo_csv):
    try:
        # Cargar el archivo CSV en un DataFrame
        df = pd.read_csv(archivo_csv, sep=',', encoding='utf-8', on_bad_lines='warn')
        return df
    except FileNotFoundError:
        print("El archivo CSV no fue encontrado.")
        return None
    except Exception as e:
        print("Ocurrió un error al cargar el archivo CSV:", e)
        return None

# Función para filtrar un DataFrame por un valor específico en la primera columna
def filtrarPorEntrevista(dataframe, valor):
    try:
        # Filtrar el DataFrame por el valor específico en la primera columna
        df_filtrado = dataframe[dataframe.iloc[:, 0] == valor]
        return df_filtrado
    except Exception as e:
        print("Ocurrió un error al filtrar por valor en la primera columna:", e)
        return None
    
# Función para visualizar cada x turnos de un DataFrame
def visualizarCadaXTurnos(dataframe, x):
    try:
        # Iterar sobre el DataFrame y visualizar una fila cada x filas
        for index, row in dataframe.iterrows():
            if index % x == 0:
                # Extraer los valores de las columnas "speaker_id" y "text"
                speaker_id = row['speaker_id']
                text = row['text']
                
                # Mostrar los valores en pantalla
                print("speaker_id:", speaker_id)
                print("text:", text)
                print()  # Separador de líneas para mejor legibilidad
    except Exception as e:
        print("Ocurrió un error al visualizar las filas:", e)

def obtenerFragmentoEntrevista(dataframe, filename, turn_ini, turn_fin):
    df_entrevista = dataframe.loc[dataframe.filename == filename].reset_index()
    texto = ''

    for row in df_entrevista.loc[turn_ini:turn_fin, ['speaker_id', 'text']].iterrows():
        texto += f'{row[1].speaker_id} {row[1].text}'
        texto += '\n'

    return texto

def obtenerProvincia(dataframe, filename):
    return dataframe.loc[dataframe.filename == filename].iloc[0].provincia

# Función para quitar o poner regionalismos del dataframe.
def distribucionLongitudDataframe(dataframe, umbral=None):
    try:
        lista = []
        # Calcular la longitud de la columna de texto en cada fila
        longitudes = dataframe['text'].apply(len)
        
        # Iterar sobre las filas del DataFrame
        for index, row in dataframe.iterrows():
            text = row['text']
            if umbral is None or len(text) >= umbral:
                lista.append(len(text))
        
        # Calcular el rango para los ejes x del histograma
        min_longitud = min(lista)
        max_longitud = max(lista)
        
        # Imprimir los valores mínimo y máximo
        print("Longitud mínima:", min_longitud)
        print("Longitud máxima:", max_longitud)

        # Crear un histograma con la distribución de las longitudes
        plt.hist(lista, bins=30, color='skyblue', edgecolor='black', range=(min_longitud, max_longitud), density=True)
        plt.xlabel('Longitud del texto')
        plt.ylabel('Frecuencia')
        plt.title('Distribución de longitudes de texto en el DataFrame')
        plt.show()
    except Exception as e:
        print("Ocurrió un error al calcular la distribución de longitudes:", e)
        
# Función para visualizar cada x turnos de un DataFrame
def elegirRegionalismos(dataframe, regionalismos):

    textos_modificados = []  # Lista para almacenar los textos modificados
    try:
        # Iterar sobre el DataFrame y visualizar una fila cada x filas
        dataframe['text']= dataframe['text'].apply(str)

        for index, row in dataframe.iterrows():
            # Extraer los valores de las columnas "text"
            text = row['text']
            fila = row.copy()  # Copiar la fila original

            if re.search(r'[a-zA-Z´¨\'`]*=', text):                    
                if (regionalismos): # Se queda con la estándar
                    subcadenas = re.split(r'=', text)
                    # Las subcadenas antes y después del patrón
                    subcadena_anterior = subcadenas[0]
                    subcadena_posterior = subcadenas[1]
                    palabras = subcadena_posterior.split()
                    primera_palabra = palabras[0]
                    subcadena_posterior_sin_primera_palabra = ' '.join(palabras[1:])
                    if(re.search(r'[.,?!;:¿¡\-—–\'\"“”‘’()[\]{}<>«»@#\$%&*_\\/]', primera_palabra)):
                        match = re.search(r'[.,?!;:¿¡\-—–\'\"“”‘’()[\]{}<>«»@#\$%&*_\\/]', primera_palabra)
                        simbolo_puntuacion = match.group()
                        subcadena_posterior_sin_primera_palabra = simbolo_puntuacion + " " + subcadena_posterior_sin_primera_palabra

                    cadena = subcadena_anterior + " " + subcadena_posterior_sin_primera_palabra
                    fila['text'] = cadena

                else : # Se queda con el regionalismo                           
                    subcadenas = re.split(r'=', text)
                    # Las subcadenas antes y después del patrón
                    subcadena_anterior = subcadenas[0]
                    subcadena_posterior = subcadenas[1]
                    # print(subcadena_anterior)
                    # print(subcadena_posterior)
                    palabras = subcadena_anterior.split()
                    subcadena_anterior_sin_ultima_palabra = ' '.join(palabras[:-1])
                    # print(subcadena_anterior_sin_ultima_palabra)
                    cadena = subcadena_anterior_sin_ultima_palabra + " " + subcadena_posterior
                    fila['text'] = cadena
                    
            textos_modificados.append(fila)
                    
        # Crear un nuevo DataFrame con los textos modificados
        df_modificado = pd.DataFrame(textos_modificados)
        return df_modificado         

    except Exception as e:
        print("Ocurrió un error al visualizar las filas:", e)
        
# Función para eliminar hablante del texto
def eliminarHablanteTexto(dataframe):
    filas_modificadas  = []  # Lista para almacenar los textos modificados
    try:
        dataframe['text']=dataframe['text'].apply(str)
        
        for index, row in dataframe.iterrows():
                # Extraer los valores de las columnas "speaker_id" y "text"
                speaker_id = row['speaker_id']
                text = row['text']

                # Crear una nueva fila con la columna 'text' modificada y conservando las demás columnas
                fila_modificada = row.copy()  # Copiar la fila original
                
                #Eliminar hablante del texto
                text_modificado = text[len(speaker_id)+1:]
                text_modificado.strip() # Elimina espacios al principio y al final
                
                fila_modificada['text'] = text_modificado  # Modificar la columna 'text'
                

                # Agregar la fila modificada a la lista
                filas_modificadas.append(fila_modificada)
        
                
                
                # print(text_modificado)  # Separador de líneas para mejor legibilidad              
        df_modificado = pd.DataFrame(filas_modificadas)
        print(df_modificado)
        
        return df_modificado
    except Exception as e:
        print("Ocurrió un error al visualizar las filas:", e)



def agregar_columna_topics(dataframe):
    # Inicializar la nueva columna
    dataframe['topics'] = None
    current_topic = None

    # Recorrer el DataFrame
    current_file = dataframe.at[0, 'filename']
    for index, row in dataframe.iterrows():
        if row['filename'] != current_file:
            current_topic = None # Al llegar a un nuevo fichero, reiniciamos topic
        
        # Buscar la etiqueta en el texto
        match = re.search(r'\bT[1-9][0-9]?\b', row['text'])
        if match:
            current_topic = match.group()
        if current_topic is not None:
            dataframe.at[index, 'text'] = row['text'].replace(current_topic, '')
            dataframe.at[index, 'topics'] = current_topic
        else:
            dataframe.at[index, 'topics'] = 0  # Asignar 0 si no se encuentra una etiqueta válida
 
        current_file = dataframe.at[index, 'filename']

    return dataframe