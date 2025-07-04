import logging
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from back_end.create_db import create_tables

# Importando o router diretamente de cada arquivo de rota
from back_end.route.parque_route import router as parque_route
from back_end.route.atrativo_route import router as atrativo_route
from back_end.route.evento_route import router as evento_route
from back_end.route.disponibilidade_route import router as disponibilidade_route
from back_end.route.administrator_route import router as administrator_route

from back_end.utils.error_handlers import http_exception_handler, validation_exception_handler

app = FastAPI(
    title="Circuito Terê Verde Online",
    description="API para consulta de informações sobre trilhas, eventos e atrativos dos parques de Teresópolis.",
    version="1.0.0"
)

# Logger
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Criação das tabelas ao iniciar
@app.on_event("startup")
async def startup():
    create_tables()

# Registro dos handlers de exceção
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Inclusão das rotas
app.include_router(parque_route)
app.include_router(atrativo_route)
app.include_router(evento_route)
app.include_router(disponibilidade_route)
app.include_router(administrator_route)
