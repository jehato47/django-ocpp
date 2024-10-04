import logging
from datetime import datetime
from ocpp.v16.datatypes import IdTagInfo
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus
from ocpp.routing import on  # Import the 'on' decorator

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    async def send(self, message):
        """ Override the send method to integrate with Django WebSocket consumer. """
        await self._websocket.send_message(message)

    async def route_message(self, message):
        """ Routes incoming messages from Django WebSocket consumer. """
        await self._handle_message(message)

    @on(Action.BootNotification)
    async def on_boot_notification(
            self, charge_point_vendor: str, charge_point_model: str, **kwargs
    ):
        return call_result.BootNotification(
            current_time=datetime.now().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted,
        )

    @on(Action.heartbeat)
    async def on_heartbeat(self):
        logging.info("Got a Heartbeat!")
        return call_result.Heartbeat(
            current_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        )

    @on(Action.start_transaction)
    async def on_start_transaction(self):
        logging.info("Started transaction!")
        return call_result.StartTransaction(
            transaction_id=1000,
            id_tag_info=IdTagInfo(status=AuthorizationStatus.accepted)
        )

    @on(Action.stop_transaction)
    async def on_stop_transaction(self, transaction_id: int, **kwargs):
        logging.info(f"StopTransaction Received: transaction_id={transaction_id}")
        return call_result.StopTransaction(
            id_tag_info=IdTagInfo(status=AuthorizationStatus.accepted)
        )

    @on(Action.data_transfer)
    async def on_data_transfer(self, vendor_id: str, message_id: str = None, data: str = None):
        """
        Handle incoming DataTransfer messages from the Charge Point.
        """
        logging.info(f"Data Transfer Received: vendor_id={vendor_id}, message_id={message_id}, data={data}")
        return call_result.DataTransfer(
            status="Accepted",  # Could also be "Rejected" or "UnknownMessageId"
            data="Data received successfully"
        )

    @on(Action.meter_values)
    async def on_meter_values(self, connector_id: int, meter_value: list, **kwargs):
        logging.info(f"MeterValues Received: connector_id={connector_id}, meter_value={meter_value}")
        return call_result.MeterValues()

    @on(Action.status_notification)
    async def on_status_notification(self, connector_id: int, error_code: str, status: str, **kwargs):
        logging.info(f"Status Notification Received: connector_id={connector_id}, error_code={error_code}, status={status}")
        return call_result.StatusNotification()