from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from back_end.create_db import get_db
from back_end.dtos.parque_dtos import ParqueCreateDTO, ParqueResponseDTO
from back_end.models.parque_models import Parque

router = APIRouter()

# GET /parques - Lista todos os parques
@router.get("/parques/", response_model=List[ParqueResponseDTO])
async def listar_parques(db: Session = Depends(get_db)):
    parques = db.query(Parque).all()
    if not parques:
        raise HTTPException(status_code=404, detail="Nenhum parque encontrado.")
    return parques

# GET /parques/{id} - Retorna um parque por ID
@router.get("/parques/{parque_id}", response_model=ParqueResponseDTO)
async def obter_parque(parque_id: int, db: Session = Depends(get_db)):
    parque = db.query(Parque).filter(Parque.id == parque_id).first()
    if not parque:
        raise HTTPException(status_code=404, detail=f"Parque com ID {parque_id} não encontrado.")
    return parque

# POST /parques - Cria novo parque
@router.post("/parques/", response_model=ParqueResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_parque(parque: ParqueCreateDTO, db: Session = Depends(get_db)):
    parque_existente = db.query(Parque).filter(Parque.nome == parque.nome).first()
    if parque_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar a requisição! Parque '{parque.nome}' já existe."
        )

    novo_parque = Parque(
        nome=parque.nome,
        descricao=parque.descricao,
        localizacao=parque.localizacao,
    )
    db.add(novo_parque)
    db.commit()
    db.refresh(novo_parque)
    return novo_parque

# PUT /parques/{id} - Atualiza parque existente
@router.put("/parques/{parque_id}", response_model=ParqueResponseDTO)
async def atualizar_parque(parque_id: int, parque_data: ParqueCreateDTO, db: Session = Depends(get_db)):
    parque = db.query(Parque).filter(Parque.id == parque_id).first()

    if not parque:
        raise HTTPException(status_code=404, detail="Parque não encontrado.")

    # Atualiza os campos
    for field, value in parque_data.dict(exclude_unset=True).items():
        setattr(parque, field, value)

    db.commit()
    db.refresh(parque)

    return ParqueResponseDTO.from_orm(parque)

# DELETE /parques/{id} - Remove um parque
@router.delete("/parques/{parque_id}", status_code=200)
async def deletar_parque(parque_id: int, db: Session = Depends(get_db)):
    parque = db.query(Parque).filter(Parque.id == parque_id).first()

    if not parque:
        raise HTTPException(status_code=404, detail=f"Parque com ID {parque_id} não encontrado.")

    db.delete(parque)
    db.commit()

    return {"message": f"Parque com ID {parque_id} deletado com sucesso!"}
