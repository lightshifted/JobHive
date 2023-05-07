from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import json
import queue
import threading
from fastapi import FastAPI

from typing import List, Dict, Callable

app = FastAPI()

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

    def on_modified(self, event):
        """
        Handler function for file modification events.
        """
        print(f"File modified: {event.src_path}")

    def on_created(self, event):
        """
        Handler function for file creation events.
        """
        print(f"File created: {event.src_path}")
        # open json file and read contents
        with open(event.src_path, "r") as file:
            try:
                data = json.load(file)
                self.data_queue.put(data) # Send the data to a separate thread
            except json.JSONDecodeError:
                print("JSONDecodeError")

    def on_deleted(self, event):
        """
        Handler function for file deletion events.
        """
        print(f"File deleted: {event.src_path}")


data_queue = queue.Queue() # For threadsafe communication between threads

import websocket
import io
import asyncio

ws = websocket.WebSocket()
ws.connect("ws://localhost:2000/")

def monitor_directory(path: str, data_queue: queue.Queue = data_queue, ws: websocket.WebSocket = ws):
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
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        # ws.close()
    observer.join()
    print("end of script")


if __name__ == "__main__":
    directory_to_monitor = "./client_data/agent_interactions"
    monitor_directory(directory_to_monitor)