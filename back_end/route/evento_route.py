from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from back_end.create_db import get_db
from back_end.dtos.evento_dtos import EventoCreateDTO, EventoResponseDTO
from back_end.models.evento_models import Evento

router = APIRouter()

# GET /eventos - Lista todos os eventos
@router.get("/eventos/", response_model=List[EventoResponseDTO])
async def listar_eventos(db: Session = Depends(get_db)):
    eventos = db.query(Evento).all()
    if not eventos:
        raise HTTPException(status_code=404, detail="Nenhum evento encontrado.")
    return eventos

# GET /eventos/{id} - Retorna um evento por ID
@router.get("/eventos/{evento_id}", response_model=EventoResponseDTO)
async def obter_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail=f"Evento com ID {evento_id} não encontrado.")
    return evento

# POST /eventos - Cria novo evento
@router.post("/eventos/", response_model=EventoResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_evento(evento: EventoCreateDTO, db: Session = Depends(get_db)):
    novo_evento = Evento(
        nome=evento.nome,
        descricao=evento.descricao,
        data_inicio=evento.data_inicio,
        data_fim=evento.data_fim,
        parque_id=evento.parque_id,
    )
    db.add(novo_evento)
    db.commit()
    db.refresh(novo_evento)
    return novo_evento

# PUT /eventos/{id} - Atualiza um evento existente
@router.put("/eventos/{evento_id}", response_model=EventoResponseDTO)
async def atualizar_evento(evento_id: int, evento_data: EventoCreateDTO, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()

    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")

    for field, value in evento_data.dict(exclude_unset=True).items():
        setattr(evento, field, value)

    db.commit()
    db.refresh(evento)

    return EventoResponseDTO.from_orm(evento)

# DELETE /eventos/{id} - Remove um evento
@router.delete("/eventos/{evento_id}", status_code=200)
async def deletar_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()

    if not evento:
        raise HTTPException(status_code=404, detail=f"Evento com ID {evento_id} não encontrado.")

    db.delete(evento)
    db.commit()

    return {"message": f"Evento com ID {evento_id} deletado com sucesso!"}
