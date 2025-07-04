from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from back_end.create_db import get_db
from back_end.dtos.administrator_dtos import AdministradorCreateDTO, AdministradorResponseDTO
from back_end.models.administrador_models import Administrador

router = APIRouter()

# GET /administradores - Lista todos os administradores
@router.get("/administradores/", response_model=List[AdministradorResponseDTO])
async def listar_administradores(db: Session = Depends(get_db)):
    admins = db.query(Administrador).all()
    if not admins:
        raise HTTPException(status_code=404, detail="Nenhum administrador encontrado.")
    return admins

# GET /administradores/{id} - Retorna um administrador por ID
@router.get("/administradores/{admin_id}", response_model=AdministradorResponseDTO)
async def obter_administrador(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Administrador).filter(Administrador.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail=f"Administrador com ID {admin_id} não encontrado.")
    return admin

# POST /administradores - Cria novo administrador
@router.post("/administradores/", response_model=AdministradorResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_administrador(admin_data: AdministradorCreateDTO, db: Session = Depends(get_db)):
    admin_existente = db.query(Administrador).filter(Administrador.email == admin_data.email).first()
    if admin_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um administrador com o e-mail '{admin_data.email}'."
        )

    novo_admin = Administrador(
        nome=admin_data.nome,
        email=admin_data.email,
        senha=admin_data.senha  # Em produção, isso deve ser criptografado!
    )
    db.add(novo_admin)
    db.commit()
    db.refresh(novo_admin)
    return novo_admin

# PUT /administradores/{id} - Atualiza dados do administrador
@router.put("/administradores/{admin_id}", response_model=AdministradorResponseDTO)
async def atualizar_administrador(admin_id: int, admin_data: AdministradorCreateDTO, db: Session = Depends(get_db)):
    admin = db.query(Administrador).filter(Administrador.id == admin_id).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Administrador não encontrado.")

    for field, value in admin_data.dict(exclude_unset=True).items():
        setattr(admin, field, value)

    db.commit()
    db.refresh(admin)

    return AdministradorResponseDTO.from_orm(admin)

# DELETE /administradores/{id} - Remove um administrador
@router.delete("/administradores/{admin_id}", status_code=200)
async def deletar_administrador(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Administrador).filter(Administrador.id == admin_id).first()

    if not admin:
        raise HTTPException(status_code=404, detail=f"Administrador com ID {admin_id} não encontrado.")

    db.delete(admin)
    db.commit()

    return {"message": f"Administrador com ID {admin_id} deletado com sucesso!"}
