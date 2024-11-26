import streamlit as st
from controlador import interpretar_suenio

# Configuración de la página
st.set_page_config(page_title="Tobi - Intérprete de Sueños", page_icon="🛌", layout="centered")

# Título de la aplicación
st.title("🛌 Tobi - Intérprete de Sueños")

# CSS para personalizar el diseño del chat
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;
    }
    .message {
        display: flex;
        align-items: center;
        margin: 5px 0;
    }
    .message.user {
        justify-content: flex-end;
    }
    .message.assistant {
        justify-content: flex-start;
    }
    .bubble {
        max-width: 60%;
        padding: 10px;
        border-radius: 10px;
        margin: 0 10px;
    }
    .bubble.user {
        background-color: #DCF8C6;
        text-align: right;
        border-radius: 10px 10px 0 10px;
    }
    .bubble.assistant {
        background-color: #FFFFFF;
        text-align: left;
        border-radius: 10px 10px 10px 0;
        box-shadow: 0px 1px 5px rgba(0,0,0,0.1);
    }
    .icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #ccc;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        color: white;
    }
    .icon.user {
        background-color: #6c757d;
    }
    .icon.assistant {
        background-color: #007BFF;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar el historial de mensajes en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar los mensajes del historial con íconos
for message in st.session_state.messages:
    role = message["role"]
    icon_class = "user" if role == "user" else "assistant"
    bubble_class = "user" if role == "user" else "assistant"

    st.markdown(f"""
        <div class="chat-container">
            <div class="message {icon_class}">
                <div class="icon {icon_class}">{'U' if role == 'user' else 'T'}</div>
                <div class="bubble {bubble_class}">{message["content"]}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Manejo de entrada del usuario
if user_input := st.chat_input("Escribe tu sueño o consulta aquí..."):
    # Agregar el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Mostrar el mensaje del usuario en el chat
    st.markdown(f"""
        <div class="chat-container">
            <div class="message user">
                <div class="icon user">U</div>
                <div class="bubble user">{user_input}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Generar la respuesta de Tobi usando el controlador
    with st.spinner("Tobi está interpretando tu sueño..."):
        response = interpretar_suenio(user_input, st.session_state.messages)

    # Agregar la respuesta de Tobi al historial
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Mostrar la respuesta de Tobi en el chat
    st.markdown(f"""
        <div class="chat-container">
            <div class="message assistant">
                <div class="icon assistant">T</div>
                <div class="bubble assistant">{response}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
