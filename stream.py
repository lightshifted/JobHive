from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import json
import asyncio
import websockets
import threading
import queue

from typing import List, Dict, Callable


class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration: raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)


async def send_to_websocket(parsed_data: Dict):
    uri = "ws://localhost:2000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(parsed_data))


def push_to_client(data: ThreadedGenerator):
    try:
        print("Data loaded successfully: ", data.queue.get())
        if data.queue.empty():
            return "No data to send"
    except json.JSONDecodeError:
        raise ValueError('Invalid JSON data')
    
    data.close()
    return


class MyEventHandler(FileSystemEventHandler):
    push_to_client: Callable[[List[str]], None]
    send_to_websocket: Callable[[Dict], None]

    def on_modified(self, event):
        print(f"File modified: {event.src_path}")

    def on_created(self, event):
        print(f"File created: {event.src_path}")
        # open json file and read contents
        with open(event.src_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print("JSONDecodeError")
        g = ThreadedGenerator()
        g.send(data)
        threading.Thread(target=send_to_websocket, args=(g,)).start()
        return push_to_client(g)

    def on_deleted(self, event):
        print(f"File deleted: {event.src_path}")


def monitor_directory(path):
    print("Monitoring directory " + path)
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    directory_to_monitor = "./client_data/agent_interactions"
    monitor_directory(directory_to_monitor)