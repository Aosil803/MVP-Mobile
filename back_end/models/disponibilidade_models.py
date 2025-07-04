from sqlalchemy import Column, Integer, String, DateTime
from back_end.create_db import Base

class Disponibilidade(Base):
    __tablename__ = "disponibilidades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_recurso = Column(String(50), nullable=False)  # "evento" ou "atrativo"
    referencia_id = Column(Integer, nullable=False)     # ID do Evento ou AtrativoNatural
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
