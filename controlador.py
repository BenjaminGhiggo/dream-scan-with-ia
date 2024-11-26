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

def interpretar_suenio(user_input, messages):
    """
    Función para interpretar un sueño utilizando la API de Gemini.
    Incluye el historial de la conversación para generar respuestas contextuales.
    Divide la respuesta en 3 partes con un máximo de 3 párrafos cada una.
    """
    if not user_input:
        return ["Por favor, describe tu sueño para que pueda ayudarte con la interpretación."]

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
        respuesta_completa = response.text.strip()

        # Dividir la respuesta en hasta 3 partes con un máximo de 3 párrafos por parte
        partes = respuesta_completa.split("\n\n")  # Dividir por párrafos
        partes = [p.strip() for p in partes if p.strip()]  # Limpiar espacios en blanco
        respuesta_dividida = []
        for i in range(0, len(partes), 3):  # Agrupar en bloques de 3 párrafos
            respuesta_dividida.append("\n\n".join(partes[i:i+3]))

        return respuesta_dividida[:3]  # Devolver hasta 3 partes
    except Exception as e:
        return [f"Ha ocurrido un error: {e}"]
