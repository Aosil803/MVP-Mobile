from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from back_end.create_db import Base

class AtrativoNatural(Base):
    __tablename__ = "atrativos_naturais"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    tipo = Column(String(50), nullable=False) 
    parque_id = Column(Integer, ForeignKey("parques.id"), nullable=False)
    parque = relationship("Parque", back_populates="atrativos")
