from back_end.create_db import db, Base
from models.parque_models import Parque
from models.atrativo_models import AtrativoNatural
from models.evento_models import Evento
from models.disponibilidade_models import Disponibilidade
from models.administrador_models import Administrador
# Criar todas as tabelas
Base.metadata.create_all(bind=db)

print(f"Tabelas criadas no banco de dados {db.url.database}")
