from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# DTO para criação de novo evento
class EventoCreateDTO(BaseModel):
    nome: str
    descricao: Optional[str] = None
    data_inicio: datetime
    data_fim: datetime
    parque_id: int

# DTO para resposta (GET)
class EventoResponseDTO(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    data_inicio: datetime
    data_fim: datetime
    parque_id: int

    class Config:
        orm_mode = True
