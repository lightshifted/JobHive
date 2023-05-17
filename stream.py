<<<<<<< HEAD
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
=======
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import json
import queue
import threading
import websocket
from fastapi import FastAPI

from typing import List, Dict, Callable

app = FastAPI()

data_queue = queue.Queue() # For threadsafe communication between threads
data_available = threading.Condition() # We use condition variables to detect when data is available
ws_url = "ws://localhost:2000/"

class FileEventHandler(FileSystemEventHandler):
    """
    A custom event handler for file system events.

    Parameters:
    -----------
    data_queue : queue.Queue
        A queue to send data from the file to a separate thread.
    """
    def __init__(self, data_queue: queue.Queue):
        self.data_queue = data_queue

    def on_created(self, event):
        """
        Handler function for file creation events.
        """
        print(f"File created: {event.src_path}")
        # open json file and read contents
        with open(event.src_path, "r") as file:
            try:
                data = json.load(file)
                with data_available:
                    self.data_queue.put(data)
                    data_available.notify()
            except json.JSONDecodeError:
                print("JSONDecodeError")


def on_open(ws):
    print("WebSocket connection opened.")

def on_message(ws, message):
    print("WebSocket received message: " + message)

def on_error(ws, error):
    print("WebSocket encountered an error: " + str(error))

def on_close(ws):
    print("WebSocket connection closed.")

global ws
ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
ws_thread = threading.Thread(target=ws.run_forever)
ws_thread.start()

def monitor_directory(path: str, data_queue: queue.Queue = data_queue):
    """
    Monitor a directory for file system events.

    Parameters:
    -----------
    path : str
        The path of the directory to monitor.
    data_queue : queue.Queue, optional
        A queue to send data from the file to a separate thread.
    """
    print("Monitoring directory " + path)

    event_handler = FileEventHandler(data_queue)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            try:
                data = data_queue.get(timeout=1)
                print("Data received: " + str(data))
                ws.send(json.dumps(data))
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        observer.stop()
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    finally:
          # Close the WebSocket connection properly
        observer.join()


if __name__ == "__main__":
    directory_to_monitor = "./client_data/agent_interactions"
    monitor_directory(directory_to_monitor)
>>>>>>> stream
