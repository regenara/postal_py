import logging
from typing import Any
from uuid import uuid4

from niquests import AsyncSession
from niquests.exceptions import ConnectTimeout

from .base import PostalPyAPIBase
from .exceptions import PostalPyConnectTimeoutError
from .schemas import (MessageExpansion,
                      RequestMessageDetailsSchema,
                      RequestMessageSchema,
                      RequestRawMessageSchema,
                      ResponseSchema)


class PostalPyAPI(PostalPyAPIBase):
    def __init__(self, base_url: str, api_key: str, timeout: int = 5, level: logging = logging.INFO):
        super().__init__(base_url=base_url, api_key=api_key, timeout=timeout, level=level)
        self._session = AsyncSession(base_url=self._base_url, timeout=self._timeout)
        self._session.headers = self._headers

    async def _send_request(self, url: str, json: dict[str, Any]) -> ResponseSchema:
        request_id = uuid4().hex
        self._logger.info('Request=%s url=%s json=%s', request_id, url, json)
        try:
            response = await self._session.post(url=url, json=json)
        except ConnectTimeout as e:
            self._logger.exception('Response=%s: %s', request_id, PostalPyConnectTimeoutError.__doc__)
            raise PostalPyConnectTimeoutError(e)
        return self._handle_response(response=response, request_id=request_id)

    async def get_message_details(self, data: RequestMessageDetailsSchema) -> ResponseSchema:
        """
        https://apiv1.postalserver.io/controllers/messages/message.html
        """
        url = '/api/v1/messages/message'
        expansions = [e for e in data.expansions or ()]
        if MessageExpansion.all in data.expansions:
            expansions = True
        json = {
            'id': data.id,
            '_expansions': expansions
        }
        return await self._send_request(url=url, json=json)

    async def get_message_deliveries(self, id: int) -> ResponseSchema:
        """
        https://apiv1.postalserver.io/controllers/messages/deliveries.html
        """
        url = '/api/v1/messages/deliveries'
        json = {'id': id}
        return await self._send_request(url=url, json=json)

    async def send_message(self, data: RequestMessageSchema) -> ResponseSchema:
        """
        https://apiv1.postalserver.io/controllers/send/message.html
        """
        url = '/api/v1/send/message'
        json = data.model_dump(exclude_none=True, by_alias=True)
        return await self._send_request(url=url, json=json)

    async def send_raw_message(self, data: RequestRawMessageSchema) -> ResponseSchema:
        """
        https://apiv1.postalserver.io/controllers/send/raw.html
        """
        url = '/api/v1/send/raw'
        json = data.model_dump(exclude_none=True)
        return await self._send_request(url=url, json=json)

    async def close(self):
        await self._session.close()
