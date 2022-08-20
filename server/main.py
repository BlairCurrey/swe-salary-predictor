from typing import List
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from lib.database import get_db
from lib.models import EncodingsStore, PredictionInput, ModelsStore
from lib.utils import format_currency, get_raw_prediction_input, is_valid_salary
from lib.schemas import PredictFormSchema, ModelStoreSchema, UntrainedInputsEncodedResponseSchema, UntrainedInputEncodedDataSchema
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
                form_data: PredictFormSchema = Depends(PredictFormSchema.as_form)):
    raw_pred_input = get_raw_prediction_input(form_data)
    salary_actual = form_data.salary_actual
    
    # TODO validate/clean inputs

    # validate salary and conditionally save in db
    if(form_data.permission_granted and salary_actual is not None 
       and is_valid_salary(salary_actual)):
        try:
            print("Attempting to save new input in db")
            db.add(PredictionInput(years_code=raw_pred_input["years_code"],
                    years_code_pro=raw_pred_input["years_code_pro"], 
                    age=raw_pred_input["age"], 
                    age_first_code=raw_pred_input["age_first_code"], 
                    country=raw_pred_input["country"], 
                    ed_level=raw_pred_input["ed_level"], 
                    dev_type=raw_pred_input["dev_type"], 
                    languages=raw_pred_input["languages"],
                    salary_actual=salary_actual, trained=False))
            db.commit()
            print("Saved new input in db")
        except BaseException as err:
            print("Failed to save user input in db")
            print(f"Unexpected {err}, {type(err)}")

    # make prediction
    pred_input = encodings.make_input(raw_pred_input)
    prediction = model.predict(pred_input).item()

    return templates.TemplateResponse("prediction.jinja", 
            {"request": request, "prediction": format_currency(prediction)})

@app.get("/api/latest-encodings-store")
async def read_latest_encodings_store(db: Session = Depends(get_db)):
    return { "latest_encodings_store": db.query(EncodingsStore)
                                .order_by(EncodingsStore.created_at.desc())
                                .first()}

@app.get("/api/latest-model-store")
async def read_latest_model_store(db: Session = Depends(get_db)):
    return { "latest_model_store": db.query(ModelsStore)
                                .order_by(ModelsStore.created_at.desc())
                                .first()}

@app.get("/api/untrained-inputs-encoded", response_model=UntrainedInputsEncodedResponseSchema)
async def read_latest_model_store(db: Session = Depends(get_db)):
    inputs = (db.query(PredictionInput)
                .where(PredictionInput.trained==False)).all()
    print(f'Retrieved {len(inputs)} untrained inputs from db')

    response = []
    for input in inputs:
        raw_pred = get_raw_prediction_input(input)
        input_encoded = encodings.make_input(raw_pred)[0].tolist()
        response.append(UntrainedInputEncodedDataSchema(uuid=input.uuid, 
                                                input_encoded=input_encoded,
                                                salary=input.salary_actual))
    return {"data": response}


@app.post("/api/model-store")
def create_model_store(model_store: ModelStoreSchema, db: Session = Depends(get_db)):
    print('Creating model store: ', model_store)
    try:
        db.add(ModelsStore(bucket=model_store.bucket,
                           path=model_store.path))
        db.commit()
        return {"status": "OK"}
    except BaseException as err:
        print("Failed to save model store in db")
        print(f"Unexpected {err}, {type(err)}")
        return { "error": err }

@app.put("/api/mark-input-trained")
def mark_input_trained(uuids: List[str], db: Session = Depends(get_db)):
    print(f'Marking {len(uuids)} as trained')
    try:
        (db.query(PredictionInput)
          .filter(PredictionInput.uuid.in_(uuids))
          .update({PredictionInput.trained: True}))
        db.commit()
        return {"status": "OK"}
    except BaseException as err:
        print("Failed to save model store in db")
        print(f"Unexpected {err}, {type(err)}")
        return { "error": err }

@app.put("/api/refetch-latest-model")
def refetch_latest_model():
    model = store.fetch_model()
    return { "status": 200}