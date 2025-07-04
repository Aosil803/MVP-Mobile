from pydantic import BaseModel
from typing import Optional

# DTO para criação de novo atrativo natural
class AtrativoNaturalCreateDTO(BaseModel):
    nome: str
    descricao: Optional[str] = None
    tipo: str
    parque_id: int

# DTO para resposta (GET)
class AtrativoNaturalResponseDTO(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    tipo: str
    parque_id: int

    class Config:
        orm_mode = True
