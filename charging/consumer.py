import asyncio
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from .ocpp_server import ChargePoint  # Import your OCPP ChargePoint class

logging.basicConfig(level=logging.INFO)


class OCPPConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.company_id = self.scope['url_route']['kwargs']['company_id']
        self.charge_point_id = self.scope['url_route']['kwargs']['charge_point_id']
        logging.info(f"Company {self.company_id}, ChargePoint {self.charge_point_id} connected")

        await self.accept(subprotocols=["ocpp1.6"])

        # Initialize your ChargePoint instance with both the company ID and charge point ID
        self.charge_point = ChargePoint(self.charge_point_id, self)

        # Start handling incoming OCPP messages
        asyncio.create_task(self.charge_point.start())

    async def disconnect(self, close_code):
        logging.info(f"ChargePoint {self.charge_point_id} disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        # Forward the received message to the ChargePoint
        await self.charge_point.route_message(text_data or bytes_data)

    async def send_message(self, message):
        await self.send(text_data=message)