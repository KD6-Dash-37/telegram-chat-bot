import asyncio
import os
import websockets
from api_methods import authenticate_websocket, get_account_summary
from dotenv import load_dotenv
load_dotenv()

async def test_response():
    
    async with websockets.connect(os.environ.get("ENDPOINT")) as websocket:

        await authenticate_websocket(websocket=websocket)

        await get_account_summary(websocket=websocket, currency="BTC")

asyncio.run(test_response())