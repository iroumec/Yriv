# ----------------------------------------------------------------------------------------------- #
#                                 Directivas del Procesador                                       #
# ----------------------------------------------------------------------------------------------- #

import re
import random
import googleapiclient.discovery

# ----------------------------------------------------------------------------------------------- #
#                              Declaración de Variables Globales                                  #
# ----------------------------------------------------------------------------------------------- #

api_key = 'AIzaSyBMfcd8lHusUnNvT8c1Nd7Dbc8LNtQ9wLk'
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

# ----------------------------------------------------------------------------------------------- #
#                                         FUNCIONES                                               #
# ----------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #
#                                       Buscar Videos                                             #
# ----------------------------------------------------------------------------------------------- #

def buscar_videos(tema, max_results=10):

    try:
        # Se realiza una búsqueda de videos en YouTube
        search_response = youtube.search().list(
            q=tema,
            type='video',
            part='id,snippet',
            maxResults=max_results
        ).execute()
        
        videos = []
        
        for item in search_response['items']:
            video = {
                'Título' : item['snippet']['title'],
                'ID' : item['id']['videoId'],
                'Description' : item['snippet']['description'],
                'Enlace' : 'https://www.youtube.com/watch?v=' + item['id']['videoId']
            }
            videos.append(video)
        
        # Se retorna la lista con los videos obtenidos
        return videos

    except Exception as e:
        print(f'Error al buscar videos en YouTube: {str(e)}')
        return[]

# ----------------------------------------------------------------------------------------------- #
#                                Video en Tendencia al Azar                                       #
# ----------------------------------------------------------------------------------------------- #

def buscar_video_aleatorio():
    
    try:
        
        # Se realiza una solicitud a la API de YouTube para obtener los videos en tendencia
        tendencias = youtube.videos().list(
            part='snippet',
            chart='mostPopular',
            regionCode='AR',
            maxResults=25
        ).execute()

        # Se selecciona un video al azar de la lista de videos en tendencia
        video_seleccionado = random.choice(tendencias['items'])

        # Se obtiene el título y la ID del video seleccionado
        video_id = video_seleccionado['id']

        video = {
            'Título': video_seleccionado['snippet']['title'],
            'ID': video_id,
            'Enlace': f'https://www.youtube.com/watch?v={video_id}'
        }

        # Se retorna el video
        return video

    except Exception as e:
        return (f'Error al obtener el video: {str(e)}')

# ----------------------------------------------------------------------------------------------- #
#                                       Buscar Canales                                            #
# ----------------------------------------------------------------------------------------------- #

def buscar_canales(tema, max_results=10):
    
    try:
        # Se realiza la solicitud a la API de YouTube
        request = youtube.search().list(
            q=tema,
            type='channel',
            part='snippet',
            maxResults=max_results
        )
        response = request.execute()

        canales = []
        
        # Se extrae la información de los canales encontrados
        for item in response['items']:
            canal = {
                'Nombre': item['snippet']['channelTitle'],
                'ID': item['snippet']['channelId'],
                'Enlace': 'https://youtube.com/channel/' + item['snippet']['channelId'].replace(' ', '')
            }
            canales.append(canal)
        
        # Se retorna la lista con los canales hallados
        return canales
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return []

# ----------------------------------------------------------------------------------------------- #
#                                     Buscar Playlists                                            #
# ----------------------------------------------------------------------------------------------- #

def buscar_playlists(tema, max_results=10):
    
    try:
        
        # Se realiza la solicitud a la API de YouTube
        request = youtube.search().list(
            q = tema,
            type = 'playlist',
            part = 'id, snippet',
            maxResults = max_results
        )
        response = request.execute()

        # Se extrae la información de las playlists encontradas
        playlists = []
        for item in response['items']:
            playlist = {
                'Título': item['snippet']['title'],
                'ID': item['id']['playlistId'],
                'Enlace': 'https://youtube.com/playlist?list=' + item['id']['playlistId']
            }
            playlists.append(playlist)
        
        # Se retorna la lista de playlists
        return playlists
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return []

# ----------------------------------------------------------------------------------------------- #
#                                      Obtener ID Video                                           #
# ----------------------------------------------------------------------------------------------- #

def obtener_ID(message):
    try:
        # Se compruebo que el enlace se halle en el formato correcto
        if '/https://www.youtube.com/watch?v=' in message:
            
            # Se extrae del mensaje la ID del video
            index = message.index('https://www.youtube.com/watch?v=')
            message = message[index + len('https://www.youtube.com/watch?v='):]
            
            # Se busca el carácter especial delimitador
            if '/' in message:
                
                # Se obtiene el mensaje anterior al delimitador y se retorna
                index = message.index('/')
                message = message[0:index]
                return message
            
        return []
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return []

# ----------------------------------------------------------------------------------------------- #
#                                        Obtener Tags                                             #
# ----------------------------------------------------------------------------------------------- #

def obtener_tags_video(video_id):

    try:
        
        # Se realiza la solicitud a la API de YouTube
        request = youtube.videos().list(
            part='snippet',
            id=video_id
        )

        response = request.execute()

        if 'items' in response and response['items']:
            tags = response['items'][0]['snippet']['tags']
            return tags
        else:
            return []
    
    except Exception as e:
        # De no tener tags el video, se devuelve una lista vacía
        return []
    
# ----------------------------------------------------------------------------------------------- #

def obtener_tags_canal(channel_id):

    try:
        # Se realiza la solicitud a la API de YouTube
        request = youtube.channels().list(
            part="snippet,brandingSettings",
            id=channel_id
        ).execute()

        # Intenta obtener las etiquetas del objeto "snippet" primero
        tags = request["items"][0]["snippet"].get("tags", [])
        
        if not tags:
            
            tags = request["items"][0]["brandingSettings"]["channel"].get("keywords", " - ").split('"')
            
            # Se filtran las etiquetas no vacías y se dividen por comillas dobles
            tags = [parte.strip() for etiqueta in tags if etiqueta for parte in re.split('["]+', etiqueta)]
            
            while "" in tags:
                tags.remove("")

        return tags

    except Exception as e:
        # El canal no tiene tags
        return []
    
# ----------------------------------------------------------------------------------------------- #
    
def obtener_tags_playlist(playlist_id):

    try:
        # Se realiza una solicitud a la API de YouTube
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            # Con obtener las tags de los primeros 10 videos es suficiente
            maxResults=10
        ).execute()

        # Se recupera las IDs de los videos en la playlist
        video_ids = [item['contentDetails']['videoId'] for item in request['items']]

        # Se obtiene la información de los videos para obtener las etiquetas en una única solicitud
        request = youtube.videos().list(
            part="snippet",
            id=",".join(video_ids)
        ).execute()

        # Se extraen las etiquetas de los videos
        tags = [video['snippet']['tags'] for video in request['items']]

        # Se combinan todas las etiquetas en una lista
        tags = [tag for sublist in tags for tag in sublist]

        return tags

    except Exception as e:
        # La playlist no tiene tags
        return []
    
# ----------------------------------------------------------------------------------------------- #