import os
import json
import shutil
import queue
import time
import asyncio
from pathlib import Path
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = FastAPI()

connected_clients = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except Exception as e:
        print(f"WebSocket disconnected: {e}")
    finally:
        connected_clients.remove(websocket)


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    async def on_created(self, event):
        if not event.is_directory:
            message = f"File detected: {event.src_path}"
            print(message)
            for websocket in connected_clients:
                await websocket.send_text(message)


def watch_dir(path: str):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    return observer


async def main():
    directory = "./agent_actors/client_data/agent_interactions"
    directory_path = Path(directory)

    if directory_path.exists():
        observer = watch_dir(directory)
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            observer.stop()
            observer.join()
    else:
        print(f"Directory not found: {directory}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=2000)
