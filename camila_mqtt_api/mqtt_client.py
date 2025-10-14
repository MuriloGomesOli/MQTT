import paho.mqtt.client as mqtt
import json
from db import conectar
import os
from dotenv import load_dotenv
import threading
import time

load_dotenv()

ultimo_estado = {}  # estado atual acumulado

# Lista das variáveis que queremos salvar
variaveis_esperadas = [
    "operacao_estoque",
    "operacao_manipulacao",
    "operacao_separacao",
    "operacao_string",
    "aguardando",
    "qualidade",
    "temperatura",
    "umidade"
]

def salvar_no_banco(dados):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO sensores (
            estoque_status, manipulacao_status, separacao_status, status_geral,
            pecas_aguardando, qualidade_sensor, temperatura, umidade
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        dados.get("operacao_estoque", "N/A"),
        dados.get("operacao_manipulacao", "N/A"),
        dados.get("operacao_separacao", "N/A"),
        dados.get("operacao_string", "N/A"),
        dados.get("aguardando", 0),
        dados.get("qualidade", "Desconhecida"),
        dados.get("temperatura", 0),
        dados.get("umidade", 0)
    ))
    conexao.commit()
    cursor.close()
    conexao.close()

def on_connect(client, userdata, flags, rc):
    print("🔗 Conectado ao broker MQTT com código:", rc)
    client.subscribe(os.getenv("MQTT_TOPICS", "#"))

def on_message(client, userdata, msg):
    global ultimo_estado
    try:
        payload = json.loads(msg.payload.decode())
        var = payload.get("variable")
        val = payload.get("value")
        if var:
            ultimo_estado[var] = val
            print(f"[MQTT] atualizado estado: {ultimo_estado}")
    except Exception as e:
        print(f"[MQTT] erro ao ler mensagem: {e}")

def iniciar_mqtt():
    client = mqtt.Client()
    client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.getenv("MQTT_BROKER"), int(os.getenv("MQTT_PORT", 8883)))
    client.loop_start()

    # Gravar no banco a cada 10 segundos
    while True:
        if any(var in ultimo_estado for var in variaveis_esperadas):
            salvar_no_banco(ultimo_estado)
            print(f"[MQTT] dados salvos no banco: {ultimo_estado}")
        time.sleep(10)
