from fastapi import APIRouter
from typing import Dict, Any

# Importações internas
# IMPORTANTE: Importamos o dicionário de estados ATUALIZADO do módulo MQTT
from app.mqtt.client import estados_atualizados 

# O módulo 'app.core.database' e 'app.db.models' não são mais necessários
# pois a rota de DB foi removida.

router = APIRouter(prefix="/api/v1", tags=["Dados e Status da Bancada"])

# Mapeamento das chaves internas (variáveis MQTT) para as chaves de saída do GET
# AS CHAVES DA ESQUERDA SÃO OS NOMES DAS VARIÁVEIS ENVIADAS PELA MÁQUINA NO MQTT!
STATUS_MAPPING = {
    "estoque_status": "operacao_estoque",
    "manipulacao_status": "operacao_manipulacao",
    "separacao_status": "operacao_separacao",
    "status_geral": "operacao_string",
    "pecas_aguardando": "aguardando",
    "qualidade_sensor": "qualidade",
    "temperatura": "temperatura",
    "umidade": "umidade",
}

@router.get("/status", response_model=Dict[str, Any])
def get_latest_real_status():
    """
    Retorna o JSON de status mais recente da bancada lido diretamente
    do dicionário global 'estados_atualizados', que é atualizado pelo cliente MQTT.
    """
    
    # Dicionário de saída com valores padrão
    output_status = {
        "operacao_estoque": "AGUARDANDO",
        "operacao_manipulacao": "AGUARDANDO",
        "operacao_separacao": "AGUARDANDO",
        "operacao_string": "AGUARDANDO",
        "aguardando": 0,
        "qualidade": "N/A",
        "temperatura": 0,
        "umidade": 0
    }
    
    # Itera sobre o mapeamento e atualiza os valores com base no MQTT
    for mqtt_key, api_key in STATUS_MAPPING.items():
        if mqtt_key in estados_atualizados:
            raw_value = estados_atualizados[mqtt_key]
            
            # Tenta converter para int/float se for um campo numérico esperado
            if api_key in ["aguardando", "temperatura", "umidade"]:
                try:
                    # Tenta converter para float (para aceitar decimais) e depois para int (se necessário)
                    output_status[api_key] = int(float(raw_value))
                except (ValueError, TypeError):
                    # Se falhar, usa o valor bruto
                    output_status[api_key] = raw_value
            else:
                # Para campos de texto/status
                output_status[api_key] = str(raw_value)

    return output_status