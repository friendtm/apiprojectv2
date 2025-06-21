# Projeto Final - Sistema de Gestão de Esteroides

Este projeto implementa um sistema distribuído baseado em microserviços que gere esteroides anabolizantes. Utiliza Flask (REST API), MongoDB para persistência, RabbitMQ para comunicação assíncrona e WebSockets para notificação em tempo real.

## Tecnologias

- Python 3.12
- Flask
- MongoDB 4.4
- RabbitMQ 3 (com management)
- WebSockets (via `websockets`)
- Docker e Docker Compose

## Como correr

### 1. Criação da rede Docker externa

```bash
docker network create projeto_final
```

### 2. Lançar os serviços

```bash
docker-compose up --build
```

> Isto irá construir e lançar:
> - `rest_api`: API Flask para gerir esteroides
> - `projeto_mongodb`: MongoDB 4.4
> - `projeto_rabbitmq`: RabbitMQ com UI em `http://localhost:15672`
> - `consumer_service`: WebSocket + Consumer de mensagens

### 3. Testes

- Aceder à API em `http://localhost:5050/esteroides` (necessário token JWT)
- RabbitMQ dashboard: `http://localhost:15672` (user: guest / guest)

## Endpoints

- `GET /esteroides` – Listar todos os esteroides
- `POST /esteroides` – Adicionar novo esteroide (envia mensagens ao RabbitMQ)
- `DELETE /esteroides/<nome>` – Remove esteroide e publica evento

## Observações

- O `consumer.py` regista as mensagens recebidas em ficheiros `.log` (log_handler.py).
- O `websocket_main.py` distribui as notificações recebidas por WebSocket aos clientes ligados.

## Autor

- Projeto Académico de Sistemas de Informação (2025)
