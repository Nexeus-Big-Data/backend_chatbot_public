from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv(dotenv_path='backend_chatbot_public-desarrollo2\.env')

# Obtener la clave de API de OpenAI
api_key = os.getenv("OPENAI_API_KEY")
#print(f"API Key cargada: {api_key}")

# Para verificar si se muestran las variables de entorno
#print("Loaded environment variables:")
#print(os.environ)

if not api_key:
    raise ValueError("La clave OPENAI_API_KEY no está configurada en el archivo .env")

# Inicializar el cliente de OpenAI
client = openai.OpenAI(api_key=api_key)

# Inicializar la aplicación FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mi-frontend-js.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de solicitud
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Llamar a OpenAI correctamente usando el cliente
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request.message}],
            max_tokens=150,
        )
        return {"response": response.choices[0].message.content}

    except openai.OpenAIError as e:
        print(f"Error OpenAI: {e}")
        raise HTTPException(status_code=500, detail=f"Error OpenAI: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Chatbot API Running!"}
