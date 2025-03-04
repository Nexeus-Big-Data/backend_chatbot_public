from fastapi import FastAPI
from dotenv import load_dotenv
import openai
import os
from models.model import Model

# Inicializamos FastAPI
app = FastAPI() #Creamos nuestra estanci FastAPI

# Cargamos las variables de entorno
load_dotenv()

openai.api_key = os.getenv('SECRET_KEY')

# Ruta POST para generar una respuesta usando OpenAI
@app.post('/chat/')
def generate_response(prompt: "Model"): #Model va a ser la clase que va a tener el modelo de la estructura de lo que estamos enviando para hacer la petición
    model = "gpt-3.5-turbo"

    # Hacemos la solicitud a la API de OpenAI
    response = openai.Completion.create(
        engine=model,
        prompt=prompt.text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.3
    )

    # Retornamos la respuesta generada por el modelo
    return {"response": response.choices[0].text.strip()}  # Usamos .strip() para eliminar espacios extras