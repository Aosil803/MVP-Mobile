import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Caminho absoluto para o banco de dados "tereverde.db"
db_path = os.path.join(os.path.dirname(__file__), '..', 'tereverde.db')

# Configuração do banco de dados SQLite
try:
    # Cria o engine para conexão com o SQLite
    db = create_engine(f"sqlite:///{db_path}", echo=True)

    # Sessão e base declarativa para os modelos
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)
    Base = declarative_base()

    # Função que importa os modelos e cria as tabelas
    def create_tables():
        # IMPORTS corrigidos com caminho completo
        from back_end.models.parque_models import Parque
        from back_end.models.atrativo_models import AtrativoNatural
        from back_end.models.evento_models import Evento
        from back_end.models.disponibilidade_models import Disponibilidade
        from back_end.models.administrador_models import Administrador

        Base.metadata.create_all(bind=db)
        print("BANCO DE DADOS E TABELAS CRIADAS COM SUCESSO!")

    # Verifica se o arquivo .db já existe; se não, cria
    if os.path.exists(db_path):
        print("BANCO DE DADOS JÁ EXISTE!")
    else:
        print(f"{db_path} NÃO ENCONTRADO, CRIANDO...")
        create_tables()
        print("BANCO DE DADOS E TABELAS CRIADOS COM SUCESSO!")

except Exception as e:
    print(f"ERRO: FALHA AO CRIAR BANCO DE DADOS! {str(e)}")

# Função que fornece a sessão do banco (usada com Depends)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
