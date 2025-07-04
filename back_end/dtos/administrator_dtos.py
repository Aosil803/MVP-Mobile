from pydantic import BaseModel, EmailStr

# DTO para criação de novo administrador
class AdministradorCreateDTO(BaseModel):
    nome: str
    email: EmailStr
    senha: str  # aqui idealmente a senha já deve vir hash ou plaintext?

# DTO para resposta (GET)
class AdministradorResponseDTO(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True
