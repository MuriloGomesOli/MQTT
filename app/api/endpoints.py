from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

# Importações do Projeto
from app.core.database import get_db
from app.db.models import BancadaData
from app.db.schemas import BancadaDataSchema

# 1. Configurar o Roteador
router = APIRouter(
    prefix="/api/v1/data",
    tags=["Dados da Bancada Camila"],
)

# 2. Função Auxiliar de Mapeamento (CORREÇÃO 1)
# Mapeia o objeto do DB (BancadaData) para o Schema de resposta (BancadaDataSchema)
def map_db_to_schema(db_data: BancadaData) -> BancadaDataSchema:
    """Mapeia o modelo DB para o Schema de resposta unificando o valor."""
    
    # Determina o valor: usa o numérico se existir, senão usa o string
    value = db_data.value_numeric if db_data.value_numeric is not None else db_data.value_string
    
    return BancadaDataSchema(
        id=db_data.id,
        timestamp=db_data.timestamp,
        topic=db_data.topic,
        category=db_data.category,
        # CORREÇÃO 1: O schema da API usa 'key', mas o DB agora usa 'data_key'
        key=db_data.data_key, 
        value=value
    )

# 3. Definir o Endpoint de Consulta (Controller)
@router.get(
    "/",
    response_model=List[BancadaDataSchema],
    summary="Listar registros da Bancada 4.0",
    description="Consulta dados persistidos no MySQL, permitindo filtros por tópico, categoria, chave e limite de resultados."
)
def read_data(
    # Injeção de Dependência da Sessão do Banco de Dados
    db: Session = Depends(get_db),
    
    # Parâmetros de Filtro (Validação de Entrada)
    limit: int = Query(20, ge=1, le=100, description="Número máximo de registros a retornar (1 a 100)."),
    category: Optional[str] = Query(None, description="Filtrar por categoria do dado (ex: 'producao', 'ambiental')."),
    # CORREÇÃO 2: O parâmetro de consulta é 'key', mas a consulta no DB usará 'data_key'
    key: Optional[str] = Query(None, description="Filtrar pela chave do dado (ex: 'temperatura', 'pecas_produzidas')."),
    start_time: Optional[datetime] = Query(None, description="Filtrar registros a partir desta data/hora."),
):
    """
    Controlador principal para buscar os dados da bancada.
    Aplica filtros de categoria, chave e intervalo de tempo, ordenando por data decrescente.
    """
    
    # 3.1. Construção da Query
    query = db.query(BancadaData)

    # 3.2. Aplicação dos Filtros
    if category:
        query = query.filter(BancadaData.category == category)
    
    if key:
        # CORREÇÃO 3: Filtra pela coluna correta no DB: data_key
        query = query.filter(BancadaData.data_key == key)

    if start_time:
        query = query.filter(BancadaData.timestamp >= start_time)

    # 3.3. Ordenação e Limite
    data_list = query.order_by(BancadaData.timestamp.desc()).limit(limit).all()

    # 3.4. Tratamento de Erro (Se necessário, mas listar vazio não é um erro 404)
    if not data_list and (category or key or start_time):
        print("Nenhum dado encontrado com os filtros fornecidos.")


    # 3.5. Mapeamento e Retorno
    return [map_db_to_schema(d) for d in data_list]

# 4. Outros Endpoints (Ex: Consulta por ID específico)
@router.get(
    "/{record_id}",
    response_model=BancadaDataSchema,
    summary="Buscar registro por ID",
    description="Busca um registro específico utilizando seu ID único."
)
def read_data_by_id(
    record_id: int,
    db: Session = Depends(get_db),
):
    """
    Controlador para buscar um registro específico pelo seu ID.
    """
    data = db.query(BancadaData).filter(BancadaData.id == record_id).first()
    
    if data is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
    
    return map_db_to_schema(data)