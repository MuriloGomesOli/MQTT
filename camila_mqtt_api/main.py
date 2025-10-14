from fastapi import FastAPI
from mqtt_client import iniciar_mqtt, ultimo_estado
from db import conectar
import threading

app = FastAPI()

# Iniciar MQTT em thread separada
threading.Thread(target=iniciar_mqtt, daemon=True).start()

@app.get("/ultimo")
def get_ultimo():
    if ultimo_estado:
        return {"ultimo_registro": ultimo_estado}
    return {"mensagem": "Nenhum dado recebido ainda da Camila."}

@app.get("/dados")
def get_dados():
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sensores ORDER BY id DESC LIMIT 10")
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return {"resultados": resultados}
    except Exception as e:
        return {"erro": str(e)}
#oi
