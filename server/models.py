from sqlalchemy import Column, Integer
from database import Base

class PredictionInput(Base):
    __tablename__ = "prediction_inputs"
    
    id = Column('id', Integer, primary_key=True)
    years_code = Column('years_code', Integer, nullable=False)
    years_code_pro = Column('years_code_pro', Integer, nullable=False)
    salary_actual = Column('salary_actual', Integer, nullable=False)
    