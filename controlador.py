import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Configurar la clave API de Gemini desde la variable de entorno
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("La clave API de Gemini no se encontró. Asegúrate de configurar 'GENAI_API_KEY' en tu archivo .env")

genai.configure(api_key=api_key)

def limpiar_respuesta(respuesta):
    """
    Limpia la respuesta generada por el modelo para eliminar caracteres no deseados.
    """
    # Eliminar caracteres no deseados como listas o comillas externas
    respuesta = re.sub(r"^\[|\]$", "", respuesta)  # Eliminar corchetes exteriores
    respuesta = re.sub(r"['\"]", "", respuesta)   # Eliminar comillas simples o dobles
    respuesta = respuesta.strip()  # Eliminar espacios en blanco adicionales
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

        return respuesta_limpia
    except Exception as e:
        return f"Ha ocurrido un error: {e}"
