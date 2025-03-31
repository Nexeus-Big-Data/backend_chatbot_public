
from fastapi import FastAPI
from pydantic import BaseModel
from openai_client import chat_openai
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

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
    with open("static/index.html", "r", encoding="utf-8") as file:
        return file.read()

# Ruta para recibir preguntas y responder
@app.post("/chat")
def chat_question(q: Question):
    print("La pregunta es:", Question)
    response = chat_openai(q.question)
    return {"answer": response}
