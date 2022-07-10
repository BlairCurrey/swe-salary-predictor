from pydantic import BaseModel
from fastapi import Form
from typing import List, Optional

# https://stackoverflow.com/a/60670614
class PredictFormSchema(BaseModel):
    years_code: int
    years_code_pro: int
    age_first_code: int
    age: int
    country: str
    dev_type: List[str]
    languages: List[str]
    ed_level: str
    salary_actual: Optional[int]
    permission_granted: bool

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
        salary_actual: Optional[int] = Form(None),
        permission_granted: bool = Form(...)
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
            salary_actual=salary_actual,
            permission_granted=permission_granted
        )

class ModelStoreSchema(BaseModel):
    bucket: str
    path: str

class UntrainedInputEncodedDataSchema(BaseModel):
    input_encoded: List[float]
    salary: float
    uuid: object

class UntrainedInputsEncodedResponseSchema(BaseModel):
    data: List[UntrainedInputEncodedDataSchema]

    class Config:
        arbitrary_types_allowed = True