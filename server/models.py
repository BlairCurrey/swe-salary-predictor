from sqlalchemy import Column, Integer, ARRAY, String
from database import Base

class PredictionInput(Base):
    __tablename__ = "prediction_inputs"
    id = Column('id', Integer, primary_key=True)
    years_code = Column('years_code', Integer, nullable=False)
    years_code_pro = Column('years_code_pro', Integer, nullable=False)
    age = Column('age', Integer, nullable=False)
    age_first_code = Column('age_first_code', Integer, nullable=False)
    country = Column('country', String, nullable=False)
    ed_level = Column('ed_level', String, nullable=False)
    dev_type = Column('dev_type', ARRAY(String), nullable=False)
    languages = Column('languages', ARRAY(String), nullable=False)
    salary_actual = Column('salary_actual', Integer, nullable=False)