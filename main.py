from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de API de OpenAI desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inicializar la aplicación FastAPI
app = FastAPI()

# Definir un modelo de datos para la solicitud
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Aquí se llama a la API de OpenAI
        response = openai.ChatCompletion.create(  # Verifica que sea ChatCompletion
            model="gpt-3.5-turbo",  # Modelo de chat, correcto
            messages=[{"role": "user", "content": request.message}],  # Mensaje del usuario
            max_tokens=150,  # Límite de tokens en la respuesta
        )
        return {"response": response['choices'][0]['message']['content']}

    except openai.error.OpenAIError as e:
        print(f"Error OpenAI: {e}")
        raise HTTPException(status_code=500, detail=f"Error OpenAI: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Chatbot API Running!"}
