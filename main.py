from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai_client import chat_openai

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (como HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Modelo de datos para recibir preguntas
class Question(BaseModel):
    question: str

# Ruta de prueba
@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        with open("static/index.html", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Página no encontrada</h1>", status_code=404)

# Ruta para recibir preguntas y responder
@app.post("/chat")
def chat_question(q: Question):
    print("La pregunta es:", q.question)
    response = chat_openai(q.question)
    return {"answer": response}
