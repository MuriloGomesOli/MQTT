from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class BancadaData(Base):
    """Modelo ORM para armazenar dados genéricos da bancada."""
    __tablename__ = "bancada_data"

    id = Column(Integer, primary_key=True, index=True)
    
    # Metadados MQTT
    timestamp = Column(DateTime, default=func.now())
    topic = Column(String(255), nullable=False, index=True)
    
    # Dados da Mensagem
    category = Column(String(50), index=True) # Ex: 'producao', 'estoque', 'ambiental'
    data_key = Column(String(100), nullable=False) # Ex: 'temperatura', 'pecas_produzidas'
    value_numeric = Column(Float, nullable=True) # Para dados numéricos
    value_string = Column(String(255), nullable=True) # Para dados textuais
    
    def __repr__(self):
        return f"<BancadaData topic='{self.topic}' key='{self.key}' value='{self.value_numeric or self.value_string}'>"