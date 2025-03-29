import os
from openai import OpenAI
from dotenv import load_dotenv
from unidecode import unidecode

# Cargar variables de entorno desde .env
load_dotenv()

# Leer la API Key
api_key = os.getenv("OPENAI_API_KEY")
print(api_key)
# Inicializar cliente
client = OpenAI(api_key=api_key)

# Lista global para guardar el historial de mensajes
message_history = [
    {
        "role": "system",
        "content": (
            "'Lo siento, su pregunta no entra dentro de mi campo de respuestas.'"
        ),
    }
]

# Función para eliminar los acentos y convertir a minúsculas
def normalizar_texto(texto:str) -> str:
    return unidecode(texto.lower())

# Función para validar si la pregunta es sobre tecnología
def es_pregunta_tecnologica(pregunta: str) -> bool:
    palabras_clave = [
        "programacion", "bases de datos", "big data", "inteligencia artificial", "machine learning", "deep learning", "software", "hardware",
        "hola", "adios", "buenos dias", "hasta luego", "buenas tardes", "buenas noches", "pagina web", "python", "chatbot"
    ]
    
    pregunta_normalizada = normalizar_texto(pregunta)
    
    return any(palabra in pregunta_normalizada for palabra in palabras_clave)

# Función para limitar los mensajes guardados
def limitar_historial():
    max_mensajes = 10
    if len(message_history) > max_mensajes + 1:
        del message_history [1:3]

# Función para consultar OpenAI
def chat_openai(question: str) -> str:
    try:
        # Validar si la pregunta es de tecnología
        if not es_pregunta_tecnologica(question):
            return "Lo siento, su pregunta no entra dentro de mi campo de respuestas.\n\n" \
            "Solo respondo preguntas sobre tecnología que incuyan las siguientes palabras:\n" \
            "1. Programación\n2. Bases de datos\n3. Big Data\n4. Inteligencia Artificial\n" \
            "5. Machine Learning\n6. Deep Learning\n7. Software\n8. Hardware"
        # Agregar la pregunta del usuario al historial
        message_history.append({"role": "user", "content": question})

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cambiar según Api Key
            messages=message_history,
            max_tokens=300
        )

         # Obtener respuesta del asistente
        assistant_reply = response.choices[0].message.content.strip()

        # Agregar respuesta del asistente al historial
        message_history.append({"role": "assistant", "content": assistant_reply})
        
        return assistant_reply

    except Exception as e:
        return f"Error: {e}"
