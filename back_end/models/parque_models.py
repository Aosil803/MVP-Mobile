from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from back_end.create_db import Base

class Parque(Base):
    __tablename__ = "parques" 

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(Text, nullable=True)
    localizacao = Column(String(255), nullable=False)
    atrativos = relationship("AtrativoNatural", back_populates="parque", cascade="all, delete-orphan")
    eventos = relationship("Evento", back_populates="parque", cascade="all, delete-orphan")
