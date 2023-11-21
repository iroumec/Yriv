# ----------------------------------------------------------------------------------------------- #
#                                 Directivas del Procesador                                       #
# ----------------------------------------------------------------------------------------------- #

import spacy
import numpy as np

# ----------------------------------------------------------------------------------------------- #
#                                         FUNCIONES                                               #
# ----------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #
#                               Extraer Nombres Mediante spaCy                                    #
# ----------------------------------------------------------------------------------------------- #

def extraer_nombre_spacy(message):
    
    try:   
        # Se carga el modelo spaCy con el modelo mediano en español
        nlp = spacy.load("es_core_news_md")

        # Se procesa el texto del mensaje anterior con Spacy
        textoProcesado = nlp(message)

        # Buscamos entidades de tipo PERSON, LOCATION o MISC en el texto procesado
        # Muchos nombres, por corresponderse a ciudades o eventos, son tomados como localidades o misceláneos y no, como personas
        nombres = [ent.text for ent in textoProcesado.ents if (ent.label_ == "PER" or ent.label_ == "LOC" or ent.label_ == "MISC")]
            
        return nombres
    
    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    
# ----------------------------------------------------------------------------------------------- #
#                             Calcular Similitud entre Etiquetas                                  #
# ----------------------------------------------------------------------------------------------- #

def calcular_similitud(primera_etiqueta, segunda_etiqueta, nlp):
    
    try:
        # Se utiliza spaCy para obtener vectores de palabras y calcular su similitud
        primer_vector = nlp(primera_etiqueta).vector
        segundo_vector = nlp(segunda_etiqueta).vector
        
        norma_primer_vector = np.linalg.norm(primer_vector)
        norma_segundo_vector = np.linalg.norm(segundo_vector)
        
        # Se verifica que no se vaya a realizar una división sobre 0
        if norma_primer_vector == 0 or norma_segundo_vector == 0:
            return 0.0
        
        # Se calcula la similitud entre las etiquetas
        similitud = np.dot(primer_vector, segundo_vector) / (norma_primer_vector * norma_segundo_vector)
        return similitud

    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    
# ----------------------------------------------------------------------------------------------- #
#                           Buscar si Existen Etiquetas Similares                                 #
# ----------------------------------------------------------------------------------------------- #

def encontrar_etiquetas_similares(etiquetas_extraidas, etiquetas_totales, umbral_similitud=0.8):
    
    try:
        # Se carga el modelo spaCy con el modelo mediano en español
        nlp = spacy.load("es_core_news_md")
        
        similares = []
        
        for etiqueta_extraida in etiquetas_extraidas:
            encontrado = False
            
            for etiqueta_total in etiquetas_totales:
                # Se calcula la similitud entre las etiquetas
                similitud = calcular_similitud(etiqueta_extraida, etiqueta_total, nlp)
                
                # Se utiliza un umbral de similitud para determinar si son similares
                if similitud > umbral_similitud:
                    encontrado = True
                    break
            
            similares.append(encontrado)
        
        return similares
    
    except Exception as e:
        # Ocurrió un error
        return []

# ----------------------------------------------------------------------------------------------- #
#                                         Predecir Video                                          #
# ----------------------------------------------------------------------------------------------- #

def realizar_prediccion(intereses, tags):

    try:
        
        # Se busca si existen etiquetas similares para las tags extraidas
        existen_similares = encontrar_etiquetas_similares(tags, intereses)
        
        if (existen_similares):
        
            numero_similares = existen_similares.count(True)
            
            porcentaje_similitud = (numero_similares)/len(existen_similares)
            
            if (0 <= porcentaje_similitud < 0.2):
                return -2
            elif (0.2 <= porcentaje_similitud < 0.4):
                return -1
            elif (0.4 <= porcentaje_similitud < 0.6):
                return 0
            elif (0.6 <= porcentaje_similitud < 0.8):
                return 1
            else:
                return 2
        
        # Caso predeterminado
        return 0.5
                
    except Exception as e:
        # De ocurrir un error
        return 0.5
    
# ------------------------------------------------------------------------------------------------------------------- #