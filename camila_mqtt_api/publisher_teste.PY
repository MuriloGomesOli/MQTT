import paho.mqtt.publish as publish
import json

broker = "broker.hivemq.com"
topic = "bancada/camila"

mensagem = {
    "estoque_status": "ativo",
    "manipulacao_status": "rodando",
    "separacao_status": "ok",
    "status_geral": "normal",
    "pecas_aguardando": "3",
    "qualidade_sensor": "alta",
    "temperatura": 24.7,
    "umidade": 61.2
}

publish.single(topic, json.dumps(mensagem), hostname=broker)
print("✅ Mensagem enviada!")
