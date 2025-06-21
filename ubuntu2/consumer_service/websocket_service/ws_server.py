import asyncio
import websockets
from websocket_service.fila import fila_mensagens

print("Fila ID:", id(fila_mensagens))

# Lista de clientes WebSocket conectados
clientes_conectados = set()

# Enviar mensagens da fila para todos os clientes conectados
async def distribuir_mensagens():
    print("Iniciado loop de distribuição")
    while True:
        print("À espera de mensagem na fila...")
        mensagem = await fila_mensagens.get()
        print("Mensagem recebida na fila:", mensagem)
        if clientes_conectados:
            print(f"A enviar para {len(clientes_conectados)} cliente(s):", mensagem)
            await asyncio.gather(*[cliente.send(mensagem) for cliente in clientes_conectados])
        else:
            print("Nenhum cliente ligado. Mensagem descartada.")

# Lida com a ligação de cada cliente WebSocket
async def handler(websocket):
    print("Cliente conectado.")
    clientes_conectados.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        print("Cliente desconectado.")
        clientes_conectados.remove(websocket)

# Iniciar o servidor WebSocket
async def arrancar_servidor_ws():
    print("Servidor WebSocket ativo em ws://0.0.0.0:8765")
    return await websockets.serve(handler, "0.0.0.0", 8765)

# Loop principal: servidor + distribuição
async def main():
    servidor = await arrancar_servidor_ws()

    await asyncio.gather(
        distribuir_mensagens(),
        servidor.wait_closed()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor WebSocket encerrado.")
