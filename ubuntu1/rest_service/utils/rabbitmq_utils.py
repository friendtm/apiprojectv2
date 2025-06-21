import pika
import json

def publicar_mensagem(queue, dados):
    try:
        conexao = pika.BlockingConnection(pika.ConnectionParameters(host='projeto_rabbitmq'))
        canal = conexao.channel()

        canal.queue_declare(queue=queue, durable=True)
        canal.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(dados),
            properties=pika.BasicProperties(delivery_mode=2)  # Mensagem persistente
        )

        conexao.close()
        print(f"Publicado na fila '{queue}':", dados)

    except Exception as e:
        print("Erro ao publicar mensagem:", str(e))
