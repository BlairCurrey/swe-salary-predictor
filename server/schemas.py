from pydantic import BaseModel

class CreatePredictionInput(BaseModel):
    years_code: int
    years_code_pro: int
    salary_actual: int