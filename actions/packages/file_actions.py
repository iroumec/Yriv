# ----------------------------------------------------------------------------------------------- #
#                                 Directivas del Procesador                                       #
# ----------------------------------------------------------------------------------------------- #

import os
import csv

# ----------------------------------------------------------------------------------------------- #
#                                         FUNCIONES                                               #
# ----------------------------------------------------------------------------------------------- #

def limpiar_archivo_usuario(path):
    
    # Se abre el archivo en modo lectura/escritura ("r+") para que sea posible usar truncate
    with open(path, "r+") as archivo:
        # Se utiliza truncate para eliminar todo el contenido
        archivo.truncate(0)

# ----------------------------------------------------------------------------------------------- #

def crear_archivo(user_id):

    # Se crea una dirección para el archivo de intereses y de tags
    tags_file = f"actions/packages/csv/user_{user_id}_tags.csv"
    searches_file = f"actions/packages/csv/user_{user_id}_searches.csv"

    # Se verifica si el archivo de intereses para el usuario existe
    if not os.path.isfile(searches_file):
        
        # Si no existe, se crea el archivo con los encabezados
        encabezadosCSV = ['SEARCHES']
        with open(searches_file, 'w', newline='') as archivoCSV:
            escritorCSV = csv.writer(archivoCSV)
            escritorCSV.writerow(encabezadosCSV)
    
    # Se verifica si el archivo de tags para el usuario existe
    if not os.path.isfile(tags_file):
        
        # Si no existe, se crea el archivo con los encabezados
        encabezadosCSV = ['TAGS', 'LIKED']
        with open(tags_file, 'w', newline='') as archivoCSV:
            escritorCSV = csv.writer(archivoCSV)
            escritorCSV.writerow(encabezadosCSV)

# ----------------------------------------------------------------------------------------------- #
    
def obtener_intereses_usuario(user_id):
    
    try:
        # Se obtiene la dirección del archivo de tags del usuario
        path = f"actions/packages/csv/user_{user_id}_tags.csv"
        
        intereses_usuario = []

        # Se guardan en una lista las tags correspondientes a videos que el usuario
        # indicó que le gustaron
        with open(path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                if len(row) > 1 and row[1] == "1":
                    intereses_usuario.append(row[0])
        
        return intereses_usuario
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    
# ----------------------------------------------------------------------------------------------- #

def tutorial_youtube():
    
    try:
        # Se busca el archivo de texto con el tutorial de YouTube.
        with open("actions/packages/text/youtube_tutorial.txt", "r") as archivo:
            textoTutorial = archivo.read()
            
        return textoTutorial
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    
# ----------------------------------------------------------------------------------------------- #

def guardar_busqueda(busqueda, user_id):
    
    try:
        # Se obtiene la dirección del archivo de búsquedas del usuario
        path = f"actions/packages/csv/user_{user_id}_searches.csv"
        
        # Se agrega al archivo la búsqueda
        with open(path, 'a', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow([busqueda])
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    
# ----------------------------------------------------------------------------------------------- #

def guardar_intereses(like, tags, user_id):
    
    try:
        # Se obtiene la dirección del archivo de etiquetas del usuario
        path = f"actions/packages/csv/user_{user_id}_tags.csv"
        
        # Se agregan al archivo las tags
        with open(path, 'a', newline='') as archivo_csv:
            for tag in tags:
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerow([tag, like])
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    
# ----------------------------------------------------------------------------------------------- #