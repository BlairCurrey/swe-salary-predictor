from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tensorflow import keras
import numpy as np
from database import get_db
from sqlalchemy.orm import Session
from models import PredictionInput
from utils import isValidSalary

dnn_model = keras.models.load_model('./dnn_model_keras')
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.jinja", {"request": request})

@app.post("/")
def submit_form(request: Request, db: Session = Depends(get_db), 
                years_code: int = Form(...), years_code_pro: int = Form(...),
                salary_actual: int = Form(...)):

    print(salary_actual)

    if(isValidSalary(salary_actual)):
        db.add(PredictionInput(years_code=years_code, 
                years_code_pro=years_code_pro, 
                salary_actual=salary_actual))
        db.commit()

    prediction: np.ndarray = dnn_model.predict([years_code, years_code_pro]).item()

    return templates.TemplateResponse("prediction.jinja", {"request": request, "prediction": prediction})
