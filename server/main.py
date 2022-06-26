from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from lib.database import get_db
from lib.models import EncodingsStore, PredictionInput
from lib.utils import isValidSalary
from lib.schemas import PredictForm
from lib.StoreClient import StoreClient

app = FastAPI()
store = StoreClient()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
model = store.fetch_model()
encodings = store.fetch_encodings()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    options = encodings.get_labels()
    return templates.TemplateResponse("home.jinja", {"request": request, 
        "countries": options["countries"], "ed_levels": options["ed_levels"],
        "dev_types": options["dev_types"], "languages": options["languages"]})

@app.post("/")
def submit_form(request: Request, db: Session = Depends(get_db), 
                form_data: PredictForm = Depends(PredictForm.as_form)):
    print(form_data)
    form_pred_inputs = {
        "age_first_code": form_data.age_first_code, 
        "years_code": form_data.years_code,
        "years_code_pro": form_data.years_code_pro, 
        "age": form_data.age, 
        "country": form_data.country, 
        "dev_type": form_data.dev_type,
        "languages": form_data.languages,
        "ed_level": form_data.ed_level
    }
    salary_actual = form_data.salary_actual
    print(form_pred_inputs)
    # TODO validate/clean inputs

    # validate salary and conditionally save in db
    if(salary_actual is not None and isValidSalary(salary_actual)):
        try:
            db.add(PredictionInput(years_code=form_pred_inputs["years_code"],
                    years_code_pro=form_pred_inputs["years_code_pro"], 
                    age=form_pred_inputs["age"], 
                    age_first_code=form_pred_inputs["age_first_code"], 
                    country=form_pred_inputs["country"], 
                    ed_level=form_pred_inputs["ed_level"], 
                    dev_type=form_pred_inputs["dev_type"], 
                    languages=form_pred_inputs["languages"],
                    salary_actual=salary_actual))
            db.commit()
        except BaseException as err:
            print("Failed to save user input in db")
            print(f"Unexpected {err}, {type(err)}")

    # make prediction
    pred_input = encodings.make_input(form_pred_inputs)
    prediction = model.predict(pred_input).item()
    
    return templates.TemplateResponse("prediction.jinja", {"request": request, "prediction": prediction})
