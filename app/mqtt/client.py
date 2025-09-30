import paho.mqtt.client as mqtt
import ssl
import json
import logging
from threading import Thread
from typing import Dict, Any, Optional

# Importações do Projeto
from app.core.config import settings 
# Dependências de DB (crud, SessionLocal, BancadaData) foram removidas, focando em estado em memória.

# --- Configuração de Logging ---
# Configuração de logging em INFO
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Variável Global de Estado ---
# Dicionário global para armazenar o estado atual (variável: valor)
# ESTA É A ÚNICA FONTE DE DADOS para o endpoint /api/v1/status.
estados_atualizados: Dict[str, Any] = {}

# --- Função de Processamento da Mensagem ---

def process_mqtt_message(msg: mqtt.MQTTMessage):
    """
    Processa a mensagem MQTT, decodifica o payload e atualiza o estado global em memória.
    Executado em uma thread separada.
    """
    topic = msg.topic
    
    try:
        raw = msg.payload.decode("utf-8")
    except Exception:
        raw = str(msg.payload)

    payload_obj = None
    try:
        payload_obj = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning(f"Payload não é JSON para tópico {topic}: {raw[:50]}...")
    except Exception as e:
        logger.error(f"Erro ao decodificar payload: {e}")
        
    # 1. Atualiza o Estado Global (Usado pelo endpoint /status)
    # Assume que o payload é {"variable": "nome_da_variavel", "value": "valor"}
    if isinstance(payload_obj, dict) and "variable" in payload_obj and "value" in payload_obj:
        variable_name = str(payload_obj["variable"])
        variable_value = payload_obj["value"]
        
        # ATUALIZAÇÃO CRÍTICA: Atualiza o dicionário global
        estados_atualizados[variable_name] = variable_value
        logger.info(f"[STATE] Atualizado {variable_name}: {variable_value} no tópico {topic}")
    else:
        logger.debug(f"Mensagem recebida, mas não pôde atualizar o estado: {raw[:30]}...")

    # A lógica de persistência (DB) foi removida.

# --- Funções do Cliente MQTT ---

def on_connect(client, userdata, flags, rc, properties=None):
    """Chamado quando a conexão é estabelecida.

    A assinatura aceita `properties` para compatibilidade com MQTT v5 (paho passa 5 args).
    """
    if rc == 0:
        logger.info("MQTT Conectado com sucesso.")
        # Usa o tópico exatamente como configurado no .env.
        topic = settings.MQTT_TOPIC_SUBSCRIPTION
        client.subscribe(topic)
        logger.info(f"Inscrito em: {topic}")
    else:
        # Tenta obter uma descrição do código de retorno; em MQTTv5 o valor ainda é um inteiro
        try:
            error_string = mqtt.connack_string(rc)
        except Exception:
            error_string = str(rc)
        logger.error(f"Falha na conexão MQTT. Código de retorno: {rc} ({error_string})")

def on_message(client, userdata, msg):
    """Chamado quando uma mensagem é recebida."""
    # Processa a mensagem em uma thread separada para evitar bloqueios
    Thread(target=process_mqtt_message, args=(msg,)).start()

def run_mqtt_client():
    """Cria e inicia o cliente MQTT em uma thread de fundo."""
    global mqtt_client_instance
    try:
        # Usando o protocolo MQTT v5 (recomendado para brokers modernos)
        client = mqtt.Client(
            client_id=settings.MQTT_CLIENT_ID,
            protocol=mqtt.MQTTv5, 
            transport="tcp"
        )
        
        # Define as funções de callback
        client.on_connect = on_connect
        client.on_message = on_message
        
        # Configura credenciais
        client.username_pw_set(
            username=settings.MQTT_USERNAME,
            password=settings.MQTT_PASSWORD
        )
        
        # --- Configuração TLS/SSL (Corrigida e Limpa para HiveMQ) ---
        # 1. Cria o contexto TLS/SSL explicitamente com TLSv1_2 e carrega CAs padrão
        # Não tente atribuir `ssl_context.protocol` — é read-only e causa AttributeError.
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # Carrega certificados confiáveis do sistema
        try:
            ssl_context.load_default_certs()
        except Exception:
            # Em ambientes minimalistas essa chamada pode falhar; continuar sem crash
            logger.debug("Não foi possível carregar certificados padrão do sistema (load_default_certs falhou).")

        # Configura a verificação de hostname (SNI) e o modo de verificação
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED

        # Opcional: define a versão mínima de TLS quando disponível (API moderna)
        try:
            if hasattr(ssl, 'TLSVersion'):
                ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        except Exception:
            # Silenciar se não suportado
            logger.debug("Não foi possível ajustar minimum_version no SSLContext (compatibilidade).")

        # 2. Aplica o contexto TLS/SSL ao cliente
        client.tls_set_context(ssl_context)

        # A chamada tls_set_options pode não existir em todas as versões do paho-mqtt;
        # proteja-a para manter compatibilidade.
        if hasattr(client, 'tls_set_options'):
            try:
                client.tls_set_options(tls_version=ssl.PROTOCOL_TLSv1_2, cert_reqs=ssl.CERT_REQUIRED)
            except Exception:
                logger.debug('tls_set_options não aplicada (incompatibilidade ou erro silencioso).')

        logger.info("TLS/SSL configurado de forma robusta (MQTTv5, SNI via Contexto).")
        
        # Conecta ao broker
        logger.info(f"Tentando conectar a: {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT} com usuário: {settings.MQTT_USERNAME}")
        # A informação do Host é usada aqui e pelo contexto SSL para o SNI.
        client.connect(
            host=settings.MQTT_BROKER_HOST,
            port=settings.MQTT_BROKER_PORT,
            keepalive=60
        )

        # Inicia o loop do cliente MQTT
        client.loop_start() 
        logger.info("Cliente MQTT iniciado em thread de fundo.")
        
        mqtt_client_instance = client
        return client

    except AttributeError as e:
        # A AttributeError pode vir de APIs do ssl/paho; não assumir que é .env ausente
        logger.critical(f"Erro crítico ao inicializar o cliente MQTT (AttributeError): {e}")
        logger.error("Verifique configuração TLS/versões de bibliotecas e variáveis de ambiente.")
        return None
    except Exception as e:
        logger.critical(f"Falha ao iniciar o Cliente MQTT: {e}")
        logger.error("Verifique as configurações no .env.")
        return None

mqtt_client_instance = None
