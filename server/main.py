from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tensorflow import keras
import numpy as np

model = keras.models.load_model('./dnn_model_keras')
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize DB connection
# Listen to DB for model changes
# Update model when changes are made

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("form.jinja", {"request": request})

@app.post("/")
def submit_form(num1: int = Form(...), num2: int = Form(...)):
    prediction = model.predict(np.array([num1, num2]))

    # save inputs in db (if salary given)

    return { "salary": prediction.item() }