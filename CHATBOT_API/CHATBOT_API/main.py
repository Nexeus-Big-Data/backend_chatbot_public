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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = openai.completions.create(  
            model="gpt-3.5-turbo",
            prompt=request.message,
            max_tokens=150  # Puedes ajustar esto según tus necesidades
        )

        return {"response": response['choices'][0]['message']['content']}

    except openai.OpenAIError as e:  # Manejo de errores actualizado
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Chatbot API Running!"}