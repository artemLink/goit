import asyncio
import logging
import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from datetime import datetime, timedelta
import aiohttp
from aiofile import AIOFile

logging.basicConfig(level=logging.INFO)

class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            await self.handle_message(ws, message)

    async def handle_message(self, ws: WebSocketServerProtocol, message: str):
        if message.startswith('exchange'):
            await self.handle_exchange_command(ws, message)
        else:
            await self.send_to_clients(f"{ws.name}: {message}")

    async def handle_exchange_command(self, ws: WebSocketServerProtocol, message: str):
        try:
            command, days = message.split()
            days = int(days)
            if days < 1:
                await ws.send("Invalid number of days")
                return
        except ValueError:
            await ws.send("Invalid command format. Use 'exchange <days>'")
            return

        # Logging the exchange command to a file
        async with AIOFile("exchange_log.txt", "a") as afp:
            await afp.write(f"{datetime.now()}: {ws.remote_address} - {message}\n")

        exchange_rates = await self.main(days)
        await ws.send(str(exchange_rates))

    async def fetch_data(self, date, session):
        try:
            async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}') as response:
                json_data = await response.json()
                return date, json_data['exchangeRate']
        except Exception as e:
            print(f"Error fetching data for date {date}: {e}")
            return date, []

    async def main(self, days: int):
        currencies = ['USD', 'EUR']
        today = datetime.now().date()
        dates_list = [today.strftime("%d.%m.%Y")]
        for i in range(1, days):
            previous_date = today - timedelta(days=i)
            dates_list.append(previous_date.strftime("%d.%m.%Y"))
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_data(date, session) for date in dates_list]
            results = await asyncio.gather(*tasks)
            answer = []
            for date, currency in results:
                tmp = {
                    date: {
                        currency['currency']: {
                            'sale': currency['saleRate'],
                            'purchase': currency['purchaseRate']
                        } for currency in currency if currency['currency'] in currencies
                    }
                }
                answer.append(tmp)
            return answer

async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
