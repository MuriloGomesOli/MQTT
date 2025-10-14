import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def conectar():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )


        
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None
def inserir_dado(temperatura, umidade):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            sql = "INSERT INTO dados (temperatura, umidade) VALUES (%s, %s)"
            valores = (temperatura, umidade)
            cursor.execute(sql, valores)
            conexao.commit()
            print("Dado inserido com sucesso")
        except Error as e:
            print(f"Erro ao inserir dado: {e}")
        finally:
            cursor.close()
            conexao.close()