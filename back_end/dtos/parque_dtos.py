from pydantic import BaseModel
from typing import Optional

# DTO para criação de novo parque
class ParqueCreateDTO(BaseModel):
    nome: str
    descricao: Optional[str] = None
    localizacao: str

# DTO para resposta (GET)
class ParqueResponseDTO(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    localizacao: str

    class Config:
        orm_mode = True
