import asyncio
import websockets

connected_clients = set()

import asyncio
import websockets

connected_clients = set()

async def handle_websocket(websocket):
    """
    A callback function to handle incoming WebSocket connections.
    """
    print(f"WebSocket client connected: {websocket.remote_address}")
    connected_clients.add(websocket)

    try:
        while True:
            message = await websocket.recv()
            print(f"Received message from client")

            # Broadcast the message to all connected clients except the sender
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.ConnectionClosedError as e:
        print(f"WebSocket client disconnected: {websocket.remote_address} with exception: {e}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)
        print(f"WebSocket client disconnected: {websocket.remote_address}")


async def start_websocket_server():
    """
    Start the WebSocket server on localhost:2000.
    """
    server = await websockets.serve(handle_websocket, "localhost", 2000)
    try:
        await server.wait_closed()
    except asyncio.CancelledError:
        pass
    finally:
        server.close()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(start_websocket_server())
    print("✔ WebSocket server started!")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
