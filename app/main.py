from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import logging

# Configuração do LOGGING para ver as mensagens do paho-mqtt
logging.basicConfig(level=logging.INFO)

# Importações do Projeto
from app.core.database import engine, Base # Importa engine e Base (para futura criação ou teste)
from app.mqtt.client import run_mqtt_client # Importa a função que inicia o cliente MQTT
from app.api.endpoints import router as data_router # Importa as rotas da API

# Variável global para armazenar a instância do cliente MQTT
mqtt_client_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação (startup/shutdown).
    Aqui, o cliente MQTT é iniciado e parado de forma limpa.
    """
    
    # === STARTUP (Ao iniciar o servidor) ===
    
    # 1. (Opcional) Criação de Tabelas
    # REMOVA ESTA LINHA APÓS A CRIAÇÃO BEM SUCEDIDA DA TABELA NO MYSQL WORKBENCH:
    # Base.metadata.create_all(bind=engine) 

    # 2. Inicia o Cliente MQTT
    global mqtt_client_instance
    try:
        # Chama a função para iniciar o cliente em uma thread separada
        mqtt_client_instance = run_mqtt_client()
        if mqtt_client_instance:
            logging.info("Sistema de API e Consumidor MQTT iniciado com sucesso.")
        else:
            logging.error("Falha ao iniciar o Cliente MQTT. Verifique as configurações no .env.")
    except Exception as e:
        logging.error(f"Erro no startup do MQTT: {e}")
    
    # Yield para que o servidor FastApi comece a aceitar requisições
    yield
    
    # === SHUTDOWN (Ao parar o servidor, e.g., CTRL+C) ===
    
    # 3. Para o Cliente MQTT
    if mqtt_client_instance:
        logging.info("Desligando o Cliente MQTT...")
        # Desconecta o broker e para o loop da thread
        mqtt_client_instance.loop_stop()
        mqtt_client_instance.disconnect()
        logging.info("Cliente MQTT desconectado.")
    
    logging.info("Aplicação desligada com sucesso.")


# Inicializa a aplicação FastApi
app = FastAPI(
    title="API de Consumo Bancada Didática 4.0 - Camila",
    description="API RESTful para consultar dados de sensores e produção persistidos via MQTT no MySQL.",
    version="1.0.0",
    # Anexa o gerenciador de ciclo de vida
    lifespan=lifespan 
)

# Adiciona as rotas da API
app.include_router(data_router)

# Rota de Status (Health Check) - Não é essencial, mas ajuda a confirmar que a API está viva
@app.get("/")
def read_root():
    return {"status": "ok", "service": "mqtt-data-consumer-api", "version": app.version}
