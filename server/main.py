from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize DB connection
# Initialize model
# Listen to DB for model changes
# Update model when changes are made

@app.get("/", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
async def read_root(request: Request):
    return templates.TemplateResponse("form.jinja", {"request": request})

@app.post("/")
def submit_form(num1: int = Form(...), num2: int = Form(...)):
    print(num1)
    print(num2)
    # make prediction
    # save inputs in db
    # return prediction
    return { "salary": 100000 }