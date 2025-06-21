import pika
import json
import time
from datetime import datetime
from utils.log_handler import guardar_em_log

# Configuração do servidor RabbitMQ
RABBITMQ_HOST = "192.168.246.38"

# Callback genérico para qualquer fila
def criar_callback(tipo_fila):
    def callback(ch, method, properties, body):
        try:
            dados = json.loads(body)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Fila: {tipo_fila.upper()} | Dados: {dados}")
            guardar_em_log(tipo_fila, dados, timestamp)
        except Exception as e:
            print(f"Erro ao processar mensagem da fila {tipo_fila}: {e}")
    return callback

def main():
    print(f"A ligar ao RabbitMQ em {RABBITMQ_HOST}...")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Filas a escutar
    filas = ["nova_esteroide", "remocao_esteroide", "novo_utilizador"]

    for fila in filas:
        channel.queue_declare(queue=fila, durable=True)
        channel.basic_consume(
            queue=fila,
            on_message_callback=criar_callback(fila),
            auto_ack=True
        )

    print("Consumidor pronto. À espera de mensagens...\n")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nConsumidor terminado manualmente.")
