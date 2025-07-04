from sqlalchemy import Column, Integer, String
from back_end.create_db import Base 

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
