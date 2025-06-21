import asyncio
from websocket_service.ws_server import distribuir_mensagens, arrancar_servidor_ws
from websocket_service.consumer_ws import iniciar_consumidor

async def main():
    servidor = await arrancar_servidor_ws()
    print("WebSocket ativo em ws://0.0.0.0:8765")

    await asyncio.gather(
        distribuir_mensagens(),
        iniciar_consumidor(),
        servidor.wait_closed()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Encerrado manualmente.")
