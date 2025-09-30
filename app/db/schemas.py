from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# --- Pydantic Schema de Saída (API Response) ---
class BancadaDataSchema(BaseModel):
    """Esquema de saída para a API."""
    id: int
    timestamp: datetime = Field(..., description="Carimbo de data/hora do registro.")
    topic: str = Field(..., description="Tópico MQTT que originou a mensagem.")
    category: Optional[str] = Field(None, description="Categoria do dado (ex: produção).")
    key: str = Field(..., description="Chave do dado (ex: temperatura).")
    value: float | str | None = Field(..., description="Valor do dado (numérico ou string).")

    class Config:
        from_attributes = True # Necessário para mapeamento ORM -> Pydantic