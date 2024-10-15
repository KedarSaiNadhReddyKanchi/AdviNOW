from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Business(Base):
    __tablename__ = "business"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)  
    name = Column(String(100), nullable=False)
    symptoms = relationship("Symptom", back_populates="business")

class Symptom(Base):
    __tablename__ = "symptom"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    code = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    diagnostic = Column(String(200), nullable=True)
    business_id = Column(Integer, ForeignKey('business.id'))
    business = relationship("Business", back_populates="symptoms")