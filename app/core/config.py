from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Define as configurações da aplicação, carregadas automaticamente
    a partir do arquivo .env ou variáveis de ambiente.
    """
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"  # Ignora variáveis no .env que não estão definidas aqui
    )
    
    # --- Configurações do Banco de Dados MySQL (SQLAlchemy) ---
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Propriedade computada para a URL de conexão do banco de dados
    @property
    def DATABASE_URL(self) -> str:
        """Retorna a string de conexão completa para o MySQL."""
        # Note: Usamos 'mysql+mysqlconnector' se for necessário um driver específico
        return f"mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # --- Configurações do Broker MQTT (HiveMQ Cloud) ---
    # Estes nomes devem corresponder EXATAMENTE aos nomes no arquivo .env
    MQTT_BROKER_HOST: str
    MQTT_BROKER_PORT: int  # Porta para conexão segura TLS/SSL (8883)
    MQTT_USERNAME: str
    MQTT_PASSWORD: str
    
    # Variáveis adicionadas que estavam faltando no Pydantic, mas estavam no .env
    MQTT_CLIENT_ID: str  # <--- ESTE CAMPO ESTAVA FALTANDO E CAUSOU O ERRO
    MQTT_TOPIC_SUBSCRIPTION: str


# Instância global das configurações
settings = Settings()
