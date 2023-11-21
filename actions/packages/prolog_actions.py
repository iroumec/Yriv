# ----------------------------------------------------------------------------------------------- #
#                                 Directivas del Procesador                                       #
# ----------------------------------------------------------------------------------------------- #

from pyswip import Prolog

# ----------------------------------------------------------------------------------------------- #
#                                         FUNCIONES                                               #
# ----------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #
#                    Obtener Aleatoriamente uno de los Videos Favoritos del Bot                   #
# ----------------------------------------------------------------------------------------------- #

def obtener_video_favorito():
    
    try:
        prolog = Prolog()
        prolog.consult('C:/Users/inaki/OneDrive/Documentos/Yriv/actions/packages/prolog/best_videos.pl')

        # Se consulta un hecho al azar
        videos = list(prolog.query("random_tematica(X)"))
        
        # Se obtiene el elemento obtenido a partir de la aleatoriedad
        topic = videos[0]["X"]
        
        # Mediante next, se obtienen los valores reales de la consulta
        enlace_query = next(prolog.query(f"enlace('{topic}', X)"))
        descripcion_query = next(prolog.query(f"descripcion('{topic}', X)"))
        
        # Se obtiene el enlace y la descripción del video obtenido
        enlace = enlace_query["X"]
        descripcion = descripcion_query["X"]
        
        video_favorito = {
            'Enlace' : enlace,
            'Descripcion' : descripcion
        }
            
        return video_favorito
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

# ----------------------------------------------------------------------------------------------- #
#                                   Obtener las Funciones del Bot                                 #
# ----------------------------------------------------------------------------------------------- #

def obtener_funciones_bot():
    
    try:   
        prolog = Prolog()
        prolog.consult('C:/Users/inaki/OneDrive/Documentos/Yriv/actions/packages/prolog/bot_functions.pl')

        # Se realiza una consulta por las funciones del bot
        funciones = list(prolog.query("function(X)"))
        
        # Se obtiene una lista con estas
        list_of_functions = list()
        
        for funcion in funciones:
            list_of_functions.append(funcion["X"])
        
        return list_of_functions
    
    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    
# ----------------------------------------------------------------------------------------------- #