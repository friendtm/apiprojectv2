import pika
import asyncio
import json
from datetime import datetime
from websocket_service.fila import fila_mensagens

RABBITMQ_HOST = "192.168.246.38"
FILAS = ["nova_esteroide_ws", "remocao_esteroide_ws", "novo_utilizador_ws"]

def criar_callback(tipo_fila, loop):
    def callback(ch, method, properties, body):
        try:
            dados = json.loads(body)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mensagem = f"[{timestamp}] {tipo_fila.upper()} → {json.dumps(dados)}"
            print("RabbitMQ:", mensagem)
            asyncio.run_coroutine_threadsafe(fila_mensagens.put(mensagem), loop)
        except Exception as e:
            print("Erro:", e)
    return callback

async def iniciar_consumidor():
    loop = asyncio.get_event_loop()
    conexao = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    canal = conexao.channel()

    for fila in FILAS:
        canal.queue_declare(queue=fila, durable=True)
        canal.basic_consume(queue=fila, on_message_callback=criar_callback(fila, loop), auto_ack=True)

    print("A escutar RabbitMQ...")
    await loop.run_in_executor(None, canal.start_consuming)
