from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv

load_dotenv(dotenv_path='backend_chatbot_public-desarrollo2/.env')

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("La clave OPENAI_API_KEY no está configurada en el archivo .env")

client = openai.OpenAI(api_key=api_key)
app = FastAPI()

# CORSMiddleware corregido:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OJO!!!!!!!!!!!!!!!!!!Cambiar esto por URLs específicas en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
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
