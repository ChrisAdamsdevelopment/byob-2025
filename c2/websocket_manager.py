from fastapi import WebSocket
clients = {}

async def connect_bot(bot_id: str, websocket: WebSocket):
    await websocket.accept()
    clients[bot_id] = websocket

async def send_command(bot_id: str, command: str):
    ws = clients.get(bot_id)
    if ws:
        await ws.send_text(command)

async def receive_output(bot_id: str):
    ws = clients.get(bot_id)
    if ws:
        return await ws.receive_text()
