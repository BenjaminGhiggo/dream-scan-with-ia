import os
import google.generativeai as genai
from dotenv import load_dotenv
import re
import random

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Configurar la clave API de Gemini desde la variable de entorno
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("La clave API de Gemini no se encontró. Asegúrate de configurar 'GENAI_API_KEY' en tu archivo .env")

genai.configure(api_key=api_key)

def limpiar_respuesta(respuesta):
    """
    Limpia la respuesta generada por el modelo para eliminar caracteres no deseados
    y el prefijo "Tobi: ".
    """
    # Eliminar corchetes, comillas y espacios innecesarios
    respuesta = re.sub(r"^\[|\]$", "", respuesta)  # Eliminar corchetes exteriores
    respuesta = re.sub(r"['\"]", "", respuesta)   # Eliminar comillas simples o dobles
    respuesta = respuesta.strip()  # Eliminar espacios en blanco adicionales

    # Eliminar el prefijo "Tobi: " si existe
    respuesta = re.sub(r"^Tobi:\s*", "", respuesta, flags=re.IGNORECASE)

    return respuesta

def agregar_emojis(respuesta):
    """
    Agrega emojis a la respuesta de manera variada y coherente.
    """

    # Diccionario de palabras clave y conjuntos de emojis relacionados
    emojis = {
        "felicidad": ["😃", "😄", "😊", "🙂", "🥰"],
        "tristeza": ["😢", "😭", "😔", "☹️"],
        "miedo": ["😱", "😨", "😧"],
        "calma": ["😌", "😇", "🫠"],
        "reflexión": ["🤔", "💭", "🧐"],
        "cambio": ["🔄", "🌟", "💫"],
        "libertad": ["✈️", "🦅", "🌈"],
        "agua": ["🌊", "🐟", "🐬"],
        "sueño": ["🌌", "🌙", "💤"],
        "éxito": ["🏆", "🌟", "🎯"],
        "transformación": ["🔄", "🦋", "🔥"],
        "amor": ["❤️", "💖", "💕"],
        "pasión": ["🔥", "❤️‍🔥"],
        "fuerza": ["💪", "🦾"],
    }

    # Usar emojis solo una vez por palabra clave
    usados = set()
    for palabra, lista_emojis in emojis.items():
        if palabra in respuesta.lower():
            if palabra not in usados:
                # Crear un patrón para encontrar palabras completas (asegurarse de que no esté dentro de otras palabras)
                patron = rf"\b{palabra}\b"
                emoji = random.choice(lista_emojis)  # Seleccionar un emoji aleatorio de la lista
                respuesta = re.sub(patron, f"{palabra} {emoji}", respuesta, count=1)  # Reemplazar solo la primera ocurrencia
                usados.add(palabra)

    return respuesta

def interpretar_suenio(user_input, messages):
    """
    Función para interpretar un sueño utilizando la API de Gemini.
    Incluye el historial de la conversación para generar respuestas contextuales.
    """
    if not user_input:
        return "Por favor, describe tu sueño para que pueda ayudarte con la interpretación."

    # Construir el historial de conversación como texto para el prompt
    historial_texto = ""
    for message in messages:
        role = "Usuario" if message["role"] == "user" else "Tobi"
        historial_texto += f"{role}: {message['content']}\n"

    # Crear el prompt para el modelo
    prompt = f"""
    Eres Tobi, un experto en interpretación de sueños. Mantén una conversación empática y profesional con el usuario.
    Historial de la conversación:
    {historial_texto}
    Usuario: {user_input}
    Tobi:"""

    try:
        model_name = "models/gemini-1.5-flash"  # Asegúrate de que este modelo esté disponible
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        respuesta_limpia = limpiar_respuesta(response.text)

        if not respuesta_limpia:
            return "Lo siento, no pude interpretar tu sueño en este momento. Por favor, intenta de nuevo más tarde."

        # Agregar emojis a la respuesta
        respuesta_con_emojis = agregar_emojis(respuesta_limpia)
        return respuesta_con_emojis
    except Exception as e:
        return f"Ha ocurrido un error: {e}"
