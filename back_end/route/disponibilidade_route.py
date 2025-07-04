from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from back_end.create_db import get_db
from back_end.dtos.disponibilidade_dtos import DisponibilidadeCreateDTO, DisponibilidadeResponseDTO
from back_end.models.disponibilidade_models import Disponibilidade

router = APIRouter()

# GET /disponibilidades - Lista todas as disponibilidades
@router.get("/disponibilidades/", response_model=List[DisponibilidadeResponseDTO])
async def listar_disponibilidades(db: Session = Depends(get_db)):
    disponibilidades = db.query(Disponibilidade).all()
    if not disponibilidades:
        raise HTTPException(status_code=404, detail="Nenhuma disponibilidade encontrada.")
    return disponibilidades

# GET /disponibilidades/{id} - Retorna uma disponibilidade por ID
@router.get("/disponibilidades/{disponibilidade_id}", response_model=DisponibilidadeResponseDTO)
async def obter_disponibilidade(disponibilidade_id: int, db: Session = Depends(get_db)):
    disponibilidade = db.query(Disponibilidade).filter(Disponibilidade.id == disponibilidade_id).first()
    if not disponibilidade:
        raise HTTPException(status_code=404, detail=f"Disponibilidade com ID {disponibilidade_id} não encontrada.")
    return disponibilidade

# POST /disponibilidades - Cria nova disponibilidade
@router.post("/disponibilidades/", response_model=DisponibilidadeResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_disponibilidade(disponibilidade: DisponibilidadeCreateDTO, db: Session = Depends(get_db)):
    nova_disponibilidade = Disponibilidade(
        tipo_recurso=disponibilidade.tipo_recurso,
        referencia_id=disponibilidade.referencia_id,
        data_inicio=disponibilidade.data_inicio,
        data_fim=disponibilidade.data_fim
    )
    db.add(nova_disponibilidade)
    db.commit()
    db.refresh(nova_disponibilidade)
    return nova_disponibilidade

# PUT /disponibilidades/{id} - Atualiza disponibilidade existente
@router.put("/disponibilidades/{disponibilidade_id}", response_model=DisponibilidadeResponseDTO)
async def atualizar_disponibilidade(disponibilidade_id: int, disponibilidade_data: DisponibilidadeCreateDTO, db: Session = Depends(get_db)):
    disponibilidade = db.query(Disponibilidade).filter(Disponibilidade.id == disponibilidade_id).first()

    if not disponibilidade:
        raise HTTPException(status_code=404, detail="Disponibilidade não encontrada.")

    for field, value in disponibilidade_data.dict(exclude_unset=True).items():
        setattr(disponibilidade, field, value)

    db.commit()
    db.refresh(disponibilidade)

    return DisponibilidadeResponseDTO.from_orm(disponibilidade)

# DELETE /disponibilidades/{id} - Remove uma disponibilidade
@router.delete("/disponibilidades/{disponibilidade_id}", status_code=200)
async def deletar_disponibilidade(disponibilidade_id: int, db: Session = Depends(get_db)):
    disponibilidade = db.query(Disponibilidade).filter(Disponibilidade.id == disponibilidade_id).first()

    if not disponibilidade:
        raise HTTPException(status_code=404, detail=f"Disponibilidade com ID {disponibilidade_id} não encontrada.")

    db.delete(disponibilidade)
    db.commit()

    return {"message": f"Disponibilidade com ID {disponibilidade_id} deletada com sucesso!"}
