from pydantic import BaseModel
from fastapi import Form
from typing import List, Optional

class CreatePredictionInput(BaseModel):
    years_code: int
    years_code_pro: int
    salary_actual: int

# https://stackoverflow.com/a/60670614
class PredictForm(BaseModel):
    years_code: int
    years_code_pro: int
    age_first_code: int
    age: int
    country: str
    dev_type: List[str]
    languages: List[str]
    ed_level: str
    salary_actual: Optional[int]

    @classmethod
    def as_form(
        cls,
        years_code: int = Form(...), # ... denotes required
        years_code_pro: int = Form(...), 
        age_first_code: int = Form(...),
        age: int = Form(...),
        country: str = Form(...),
        dev_type: List[str] = Form(...),
        languages: List[str] = Form(...),
        ed_level: str = Form(...),
        salary_actual: Optional[int] = Form(None)
    ):
        return cls(
            years_code=years_code,
            years_code_pro=years_code_pro,
            age_first_code=age_first_code,
            age=age,
            country=country,
            dev_type=dev_type,
            languages=languages,
            ed_level=ed_level,
            salary_actual=salary_actual
        )