import streamlit as st
from controlador import interpretar_suenio

# Configuración de la página
st.set_page_config(page_title="Tobi - Intérprete de Sueños", page_icon="🛌", layout="centered")

# Título de la aplicación
st.title("🛌 Tobi - Intérprete de Sueños")

# Inicializar el historial de mensajes en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar los mensajes del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Manejo de entrada del usuario
if user_input := st.chat_input("Escribe tu sueño o consulta aquí..."):
    # Mostrar el mensaje del usuario en el chat
    st.chat_message("user").markdown(user_input)
    # Agregar el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generar la respuesta de Tobi usando el controlador
    with st.chat_message("assistant"):
        with st.spinner("Tobi está interpretando tu sueño..."):
            response = interpretar_suenio(user_input, st.session_state.messages)
            st.markdown(response)
    # Agregar la respuesta de Tobi al historial
    st.session_state.messages.append({"role": "assistant", "content": response})
