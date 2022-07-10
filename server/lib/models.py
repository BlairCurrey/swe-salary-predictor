from sqlalchemy import Column, Integer, ARRAY, String, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from lib.database import Base
import uuid

class PredictionInput(Base):
    __tablename__ = "prediction_inputs"
    uuid = Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    years_code = Column('years_code', Integer, nullable=False)
    years_code_pro = Column('years_code_pro', Integer, nullable=False)
    age = Column('age', Integer, nullable=False)
    age_first_code = Column('age_first_code', Integer, nullable=False)
    country = Column('country', String, nullable=False)
    ed_level = Column('ed_level', String, nullable=False)
    dev_type = Column('dev_type', ARRAY(String), nullable=False)
    languages = Column('languages', ARRAY(String), nullable=False)
    salary_actual = Column('salary_actual', Integer, nullable=False)
    created_at = Column('created_at', DateTime(timezone=True), nullable=False, default=func.now())
    trained = Column('trained', Boolean, nullable=False, default=False)

class EncodingsStore(Base):
    __tablename__ = "encodings_store"
    uuid = Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bucket = Column('bucket', String, nullable=False)
    path = Column('path', String, nullable=False)
    created_at = Column('created_at', DateTime(timezone=True), nullable=False, default=func.now())

class ModelsStore(Base):
    __tablename__ = "models_store"
    uuid = Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bucket = Column('bucket', String, nullable=False)
    path = Column('path', String, nullable=False)
    created_at = Column('created_at', DateTime(timezone=True), nullable=False, default=func.now())