from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Cria o engine de conexão com o MySQL
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Cria a classe base para os modelos ORM
class Base(DeclarativeBase):
    pass

# Cria a sessão de acesso ao banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependência para o FastAPI injetar a sessão do DB nas rotas."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()