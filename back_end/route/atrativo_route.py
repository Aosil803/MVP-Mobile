from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from back_end.create_db import get_db
from back_end.dtos.atrativo_dtos import AtrativoNaturalCreateDTO, AtrativoNaturalResponseDTO
from back_end.models.atrativo_models import AtrativoNatural

router = APIRouter()

# GET /atrativos - Lista todos os atrativos naturais
@router.get("/atrativos/", response_model=List[AtrativoNaturalResponseDTO])
async def listar_atrativos(db: Session = Depends(get_db)):
    atrativos = db.query(AtrativoNatural).all()
    if not atrativos:
        raise HTTPException(status_code=404, detail="Nenhum atrativo natural encontrado.")
    return atrativos

# GET /atrativos/{id} - Retorna um atrativo natural por ID
@router.get("/atrativos/{atrativo_id}", response_model=AtrativoNaturalResponseDTO)
async def obter_atrativo(atrativo_id: int, db: Session = Depends(get_db)):
    atrativo = db.query(AtrativoNatural).filter(AtrativoNatural.id == atrativo_id).first()
    if not atrativo:
        raise HTTPException(status_code=404, detail=f"Atrativo com ID {atrativo_id} não encontrado.")
    return atrativo

# POST /atrativos - Cria novo atrativo natural
@router.post("/atrativos/", response_model=AtrativoNaturalResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_atrativo(atrativo: AtrativoNaturalCreateDTO, db: Session = Depends(get_db)):
    novo_atrativo = AtrativoNatural(
        nome=atrativo.nome,
        descricao=atrativo.descricao,
        tipo=atrativo.tipo,
        parque_id=atrativo.parque_id
    )
    db.add(novo_atrativo)
    db.commit()
    db.refresh(novo_atrativo)
    return novo_atrativo

# PUT /atrativos/{id} - Atualiza atrativo natural existente
@router.put("/atrativos/{atrativo_id}", response_model=AtrativoNaturalResponseDTO)
async def atualizar_atrativo(atrativo_id: int, atrativo_data: AtrativoNaturalCreateDTO, db: Session = Depends(get_db)):
    atrativo = db.query(AtrativoNatural).filter(AtrativoNatural.id == atrativo_id).first()

    if not atrativo:
        raise HTTPException(status_code=404, detail="Atrativo não encontrado.")

    for field, value in atrativo_data.dict(exclude_unset=True).items():
        setattr(atrativo, field, value)

    db.commit()
    db.refresh(atrativo)

    return AtrativoNaturalResponseDTO.from_orm(atrativo)

# DELETE /atrativos/{id} - Remove um atrativo natural
@router.delete("/atrativos/{atrativo_id}", status_code=200)
async def deletar_atrativo(atrativo_id: int, db: Session = Depends(get_db)):
    atrativo = db.query(AtrativoNatural).filter(AtrativoNatural.id == atrativo_id).first()

    if not atrativo:
        raise HTTPException(status_code=404, detail=f"Atrativo com ID {atrativo_id} não encontrado.")

    db.delete(atrativo)
    db.commit()

    return {"message": f"Atrativo com ID {atrativo_id} deletado com sucesso!"}
