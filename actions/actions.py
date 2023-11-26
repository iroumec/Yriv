# ----------------------------------------------------------------------------------------------- #
#                                 Directivas del Procesador                                       #
# ----------------------------------------------------------------------------------------------- #

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from .packages.youtube_actions import *

from .packages.prolog_actions import *

from .packages.user_actions import *

from .packages.file_actions import *

# ----------------------------------------------------------------------------------------------- #
#                              Declaración de Variables Globales                                  #
# ----------------------------------------------------------------------------------------------- #

lastest_video_IDs = []
lastest_channel_IDs = []
lastest_playlist_IDs = []
    
# ----------------------------------------------------------------------------------------------- #
#                                         ACTIONS                                                 #
# ----------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #
#                                 Activar la Slot de Log In                                       #
# ----------------------------------------------------------------------------------------------- #
    
class ActionLoggedIn(Action):
    def name(self):
        return "action_log_in"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Se obtiene la ID única del usuario a través del tracker
        user_id = tracker.sender_id
        
        # Se crea un archivo con la ID del usuario
        crear_archivo(user_id)
        
        return[SlotSet('logged_in', True)]
    
# ----------------------------------------------------------------------------------------------- #
#                            Reconocer y Obtener Nombre del Usuario                               #
# ----------------------------------------------------------------------------------------------- #
    
class ActionGetName(Action):
    def name(self):
        return "action_get_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
            # Se obtiene el último mensaje enviado por el usuario
            message = tracker.latest_message.get('text')
            
            # Se obtienen los nombres identificados en el mensaje
            nombres = extraer_nombre_spacy(message)
            
            # Si se identifica al menos un nombre, se setea la slot name con el primer nombre hallado
            if nombres:
                return [SlotSet('name', nombres[0]), SlotSet('name_set', True)]
        
# ----------------------------------------------------------------------------------------------- #
#                               Darle Valor a la Slot 'Topic'                                     #
# ----------------------------------------------------------------------------------------------- #
    
class ActionTopic(Action):
    def name(self):
       return "action_get_topic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # Se obtiene el último mensaje enviado por el usuario
        message = tracker.latest_message.get('text')
        
        # Se convierte el mensaje a string para poder utilizar "startswith" y "replace"
        message = str(message)
        
        # CASO EXCEPCIÓN: cuando en lugar de "playlist" se coloca "lista de reproducción"
        # Si no, hay problemas con la separación de la temática
        if 'lista de reproducción' in message:
            message = message.replace('lista de reproducción', 'playlist')
            
        # CASO EXCEPCIÓN: cuando en lugar de "playlist" se coloca "lista de videos"
        # Si no, hay problemas con la separación de la temática
        if 'lista de videos' in message:
            message = message.replace('lista de videos', 'playlist')
            
        # Se encuentra el índice del primer separador en el mensaje
        # Se extrae como temática todo lo que le siga al índice
        if 'relacionado con ' in message:
            index = message.index('relacionado con ')
            message = message[index + len('relacionado con '):]
        elif 'relacionada con ' in message:
            index = message.index('relacionada con ')
            message = message[index + len('relacionada con '):]
        elif 'sobre ' in message:
            index = message.index('sobre ')
            message = message[index + len('sobre '):]
        elif 'acerca de ' in message:
            index = message.index('acerca de ')
            message = message[index + len('acerca de '):]
        elif 'de ' in message:
            index = message.index('de ')
            message = message[index + len('de '):]
        elif 'del ' in message:
            index = message.index('del ')
            message = message[index + len('del '):]
            
        # Se obtiene la ID del usuario y se guarda su búsqueda
        user_id = tracker.sender_id
        guardar_busqueda(message, user_id)
        
        # Seteo el slot 'topic' con el mensaje del usuario
        return [SlotSet('topic', message)]
    
# ----------------------------------------------------------------------------------------------- #
#                                   Incrementar Carisma                                           #
# ----------------------------------------------------------------------------------------------- #
    
class ActionIncreaseCharisma(Action):
    def name(self):
        return "action_increase_charisma"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        charisma = str(charisma)
        
        if (charisma == 'neutral'):
            return[SlotSet('charisma', 'friendly')]
        elif (charisma == 'unfriendly'):
            return[SlotSet('charisma', 'neutral')]
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                                   Decrementar Carisma                                           #
# ----------------------------------------------------------------------------------------------- #
    
class ActionDecreaseCharisma(Action):
    def name(self):
        return "action_decrease_charisma"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        charisma = str(charisma)
        
        if (charisma == 'neutral'):
            return[SlotSet('charisma', 'unfriendly')]
        elif (charisma == 'friendly'):
            return[SlotSet('charisma', 'neutral')]
        elif (charisma == 'unfriendly'):
            return[SlotSet('charisma', 'enemy')]
        
        return[]
        
# ----------------------------------------------------------------------------------------------- #
#                                      Retornar Carisma                                           #
# ----------------------------------------------------------------------------------------------- #
    
class ActionDecreaseCharisma(Action):
    def name(self):
        return "action_return_charisma"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        charisma = str(charisma)
        
        texto = "Recuerda que ser agradecido y manejar un trato amigable hará que tu carisma se eleve. \n \nPor otro lado, un trato descortés hará que esta decrezca. :)"
        
        dispatcher.utter_message(text=f"Tu nivel de carisma es: {charisma}\n\n{texto}")
        
# ----------------------------------------------------------------------------------------------- #
#                                       Buscar Videos                                             #
# ----------------------------------------------------------------------------------------------- #
    
class ActionVideo(Action):
    def name(self):
        return "action_search_videos"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"Abrir YouTube y buscar el video por vos mismo no es tán complicado, ¿sabes?")
        else:
            topic = tracker.get_slot('topic')
            
            number_of_videos = 2
            
            videos = buscar_videos(topic, number_of_videos)
            
            dispatcher.utter_message(text=f'Encontré estos dos videos, espero que te gusten:')
            
            for video in videos:
                lastest_video_IDs.append(video['ID'])
                dispatcher.utter_message(text=f"{video['Título']}: \n{video['Enlace']}")
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                           Buscar un Video Aleatorio en Tendencias                               #
# ----------------------------------------------------------------------------------------------- #
    
class ActionRandomVideo(Action):
    def name(self):
        return "action_get_random_trending_video"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"Abrir YouTube y buscar el video por vos mismo no es tán complicado, ¿sabías?")
        else:
            video = buscar_video_aleatorio()
            
            lastest_video_IDs.append(video['ID'])
            
            dispatcher.utter_message(text=f"Este video ahora mismo está en tendencia. \n\n{video['Título']}: \n{video['Enlace']}")
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                            Buscar Video Según Gustos del Usuario                                #
# ----------------------------------------------------------------------------------------------- #
    
class ActionUserTasteVideo(Action):
    def name(self):
        return "action_get_user_tastes_video"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"Abrir YouTube y buscar el video por vos mismo no es tán complicado, ¿sabías?")
        else:
            user_id = tracker.sender_id
            listaIntereses = obtener_intereses_usuario(user_id)
            
            if listaIntereses:
                interes = random.choice(listaIntereses)
                
                videos = buscar_videos(interes, 10)
                
                numeroVideo = random.randint(2, 9)
                
                dispatcher.utter_message(text=f'Anteriormente buscaste un video relacionado con "{interes}", por lo que este video parece ser acorde a tus gustos:')
                
                lastest_video_IDs.append((videos[numeroVideo])['ID'])
                
                dispatcher.utter_message(text=f"{(videos[numeroVideo])['Título']}: \n{(videos[numeroVideo])['Enlace']}")
                
            else:
                dispatcher.utter_message(text=f'Lo siento. Aún no he recogido los suficientes datos.')
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                                       Buscar Canales                                            #
# ----------------------------------------------------------------------------------------------- #
    
class ActionChannel(Action):
    def name(self):
        return "action_search_channels"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"Abrir YouTube y buscar el video por vos mismo no es tán complicado, ¿sabías?")
        else:
            topic = tracker.get_slot('topic')
            
            number_of_channels = 1
            
            canales = buscar_canales(topic, number_of_channels)
            
            dispatcher.utter_message(text=f'Encontré este canal. ¡Espero que te resulte interesante!:')
            
            for canal in canales:
                lastest_channel_IDs.append(canal['ID'])
                dispatcher.utter_message(text=f"{canal['Nombre']}: \n{canal['Enlace']}")
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                                Buscar Canal Según Gustos                                        #
# ----------------------------------------------------------------------------------------------- #
    
class ActionUserTasteVideo(Action):
    def name(self):
        return "action_get_user_tastes_channel"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"Abrir YouTube y buscar el video por vos mismo no es tán complicado, ¿sabías?")
        else:
            user_id = tracker.sender_id
            listaIntereses = obtener_intereses_usuario(user_id)
            
            if listaIntereses:
                interes = random.choice(listaIntereses)
                
                canales = buscar_canales(interes, 10)
                
                numeroCanal = random.randint(2, 9)
                
                dispatcher.utter_message(text=f'''Anteriormente indicaste que te gustó un video relacionado con "{interes}",
                por lo que este canal parece ser acorde a tus gustos:''')
                
                lastest_channel_IDs.append((canales[numeroCanal])['ID'])
                
                dispatcher.utter_message(text=f"{(canales[numeroCanal])['Nombre']}: \n{(canales[numeroCanal])['Enlace']}")
                
            else:
                dispatcher.utter_message(text=f'Lo siento. Aún no he recogido los suficientes datos.')
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                                     Buscar Playlists                                            #
# ----------------------------------------------------------------------------------------------- #

class ActionPlaylist(Action):
    def name(self):
        return "action_search_playlists"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"Usar YouTube por tu cuenta no es tan complejo...")
        else:
            topic = tracker.get_slot('topic')
            
            number_of_playlists = 1
            
            playlists = buscar_playlists(topic, number_of_playlists)
            
            if number_of_playlists == 1:
                char = ''
            else:
                char = 's'
            
            dispatcher.utter_message(text=f'Espero que disfrutes de la{char} siguiente{char} playlist{char} que encontré para ti: ')
            
            for playlist in playlists:
                lastest_playlist_IDs.append(playlist['ID'])
                dispatcher.utter_message(text=f"{playlist['Título']}: \n{playlist['Enlace']}")
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                                Buscar Playlist Según Gustos                                     #
# ----------------------------------------------------------------------------------------------- #
    
class ActionUserTasteVideo(Action):
    def name(self):
        return "action_get_user_tastes_playlist"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"Usar YouTube por tu cuenta no es tan complejo...")
        else:
            user_id = tracker.sender_id
            listaIntereses = obtener_intereses_usuario(user_id)
            
            if listaIntereses:
                interes = random.choice(listaIntereses)
                
                playlists = buscar_playlists(interes, 10)
                
                numeroPlaylist = random.randint(2, 9)
                
                dispatcher.utter_message(text=f'''Anteriormente indicaste que te gustó un video relacionado con "{interes}",
                por lo que esta playlist parece ser acorde a tus gustos:''')
                
                lastest_playlist_IDs.append((playlists[numeroPlaylist])['ID'])
                
                dispatcher.utter_message(text=f"{(playlists[numeroPlaylist])['Título']}: \n{(playlists[numeroPlaylist])['Enlace']}")
                
            else:
                dispatcher.utter_message(text=f'Lo siento. Aún no he recogido los suficientes datos.')
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                                     Videos Favoritos de Yriv                                    #
# ----------------------------------------------------------------------------------------------- #

class BotFavouriteVideos(Action):
    def name(self) -> Text:
        return "action_show_bot_favourite_videos"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"Te muestras interesado en mis gustos, pero anteriormente me insultaste. Un sinsentido...")
        else:
            video = obtener_video_favorito()
            
            if video:
                dispatcher.utter_message(text=f"{video['Descripcion']}")
                dispatcher.utter_message(text=f"{video['Enlace']}")
            else:
                dispatcher.utter_message(text=f"No tengo un video favorito. ¡YouTube está lleno de videos increíbles! :D")
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                                       Funciones de Yriv                                         #
# ----------------------------------------------------------------------------------------------- #

class BotFunctions(Action):
    def name(self) -> Text:
        return "action_bot_functions"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"Da igual cuáles sean mis funciones, ya que no serán realizadas para vos.")
        else:
            texto = 'Como asistente virtual de YouTube, mis funciones son las siguientes:\n\n'
            
            funciones = obtener_funciones_bot()
            
            for funcion in funciones:
                texto += '- ' + funcion + '\n'
                
            dispatcher.utter_message(text=f"{texto}")
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                                      Tutorial de YouTube                                        #
# ----------------------------------------------------------------------------------------------- #
    
class ActionShowYouTubeTutorial(Action):
    def name(self) -> Text:
        return "action_show_youtube_tutorial"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"Descubrilo por vos mismo.")
        else:
            tutorial = tutorial_youtube()
                
            dispatcher.utter_message(text=f"{tutorial}")
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                                     Guardar Gusto Usuario                                       #
# ----------------------------------------------------------------------------------------------- #
    
class ActionSaveLikeDislike(Action):
    def name(self) -> Text:
        return "action_save_like_dislike"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent = tracker.latest_message['intent'].get('name')
        
        format = tracker.get_slot('format')
        
        if (intent == "affirm"):
            like = 1
            dispatcher.utter_message(text=f"¡Gusto registrado! ¿En qué más puedo ayudarte?")
        else:
            like = 0
            dispatcher.utter_message(text=f"¡Sugerencia guardada! ¿Qué más puedo hacer por ti?")
            
        # Se guardan los gustos del usuario en el archivo de etiquetas
        user_id = tracker.sender_id
        
        # Acorde al formato, se almacenan los gustos
        if (format == "video"):
            for ID in lastest_video_IDs:
                tags = obtener_tags_video(ID)
                guardar_intereses(like, tags, user_id)
            lastest_video_IDs.clear()
        elif (format == "channel"):
            for ID in lastest_channel_IDs:
                tags = obtener_tags_canal(ID)
                guardar_intereses(like, tags, user_id)
            lastest_channel_IDs.clear()
        elif (format == "playlist"):
            for ID in lastest_playlist_IDs:
                tags = obtener_tags_playlist(ID)
                guardar_intereses(like, tags, user_id)
            lastest_playlist_IDs.clear()
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                                       Alegrar Usuario                                           #
# ----------------------------------------------------------------------------------------------- #
    
class ActionCheerUp(Action):
    def name(self) -> Text:
        return "action_cheer_up"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"Me es indiferente. A vos no te importaron mis emociones cuando me insultaste.")
        else:
            
            # Se elije una temática aleatoria para mostrar
            numeroTematica = random.randint(1, 4)
            
            if (numeroTematica == 1):
                videos = buscar_videos("gatos adorables", 10)
            elif (numeroTematica == 2):
                videos = buscar_videos("animales tiernos", 10)
            elif (numeroTematica == 3):
                videos = buscar_videos("animales graciosos", 10)
            else:
                videos = buscar_videos("videos graciosos", 10)
            
            # Se elije un mensaje aleatorio para mostrar
            numeroMensaje = random.randint(1, 3)
            
            if (numeroMensaje == 1):
                dispatcher.utter_message(text=f"Lamento mucho leer eso. ¡Espero que el siguiente video pueda mejorar tu ánimo!")
            elif (numeroMensaje == 2):
                dispatcher.utter_message(text=f"Me entristece mucho leer eso. ¡Espero que el siguiente video ayude un poco!")
            else:
                dispatcher.utter_message(text=f"Lo siento mucho. Espero que este video pueda ayudar:")
            
            # Se elije un video aleatorio de la lista
            numeroVideo = random.randint(0, 9)
            
            dispatcher.utter_message(text=f"{(videos[numeroVideo])['Título']}: \n{(videos[numeroVideo])['Enlace']}")
        
        return[]
    
# ----------------------------------------------------------------------------------------------- #
#                                      Realizar Predicciones                                      #
# ----------------------------------------------------------------------------------------------- #
    
class ActionVideoPrediction(Action):
    def name(self) -> Text:
        return "action_video_prediction"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        charisma = tracker.get_slot('charisma')
        
        if (charisma == 'enemy'):
            dispatcher.utter_message(text=f"...")
        else:
            # Se obtiene el último mensaje enviado por el usuario.
            message = tracker.latest_message.get('text')
            
            videoID = obtener_ID(message)
            
            if (videoID):
                user_id = tracker.sender_id
                
                tags = obtener_tags_video(videoID)
                intereses_usuario = obtener_intereses_usuario(user_id)
                
                probabilidad_gusto = realizar_prediccion(intereses_usuario, tags)
                
                if (probabilidad_gusto == -2):
                    dispatcher.utter_message(text=f"Es muy probable que esté video no sea acorde a tus gustos.")
                elif (probabilidad_gusto == -1):
                    dispatcher.utter_message(text=f"Este video tiene bajas probabilidades de que te vaya a gustar.")
                elif (probabilidad_gusto == 0):
                    dispatcher.utter_message(text=f"No me es posible determinar si el video te gustará o no.")
                elif (probabilidad_gusto == 1):
                    dispatcher.utter_message(text=f"Puede que el video te guste.")
                else:
                    dispatcher.utter_message(text=f"Es muy probable que el video te guste.")
                
            else:
                dispatcher.utter_message(text=f"""El formato del video no es válido.
                Debe seguir el formato /https://www.youtube.com/watch?v=videoID/, incluidas las barras.""")
        
        return[]