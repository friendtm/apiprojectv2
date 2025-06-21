import asyncio

# Fila partilhada entre WebSocket e consumidor RabbitMQ
fila_mensagens = asyncio.Queue()
