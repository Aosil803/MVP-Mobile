from pydantic import BaseModel
from datetime import datetime

# DTO para criação de nova disponibilidade
class DisponibilidadeCreateDTO(BaseModel):
    tipo_recurso: str  # esperado: "evento" ou "atrativo"
    referencia_id: int
    data_inicio: datetime
    data_fim: datetime

# DTO para resposta (GET)
class DisponibilidadeResponseDTO(BaseModel):
    id: int
    tipo_recurso: str
    referencia_id: int
    data_inicio: datetime
    data_fim: datetime

    class Config:
        orm_mode = True
