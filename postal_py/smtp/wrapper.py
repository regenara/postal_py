import logging
import ssl
from smtplib import SMTP
from typing import Any
from uuid import uuid4

from .base import PostalPySMTPBase
from .schemas import SMTPMessageSchema


class PostalPySMTP(PostalPySMTPBase):
    def __init__(self, hostname: str, username: str, password: str, port: int = 25, use_tls: bool = True,
                 timeout: int = 5, level: logging = logging.INFO):
        super().__init__(hostname=hostname, port=port, username=username, password=password, use_tls=use_tls,
                         timeout=timeout, level=level)

    def send_message(self, data: SMTPMessageSchema) -> dict[str, Any]:
        request_id = uuid4().hex
        self._logger.info('Request=%s data=%s', request_id, data.model_dump(
            exclude_none=True, exclude={'plain_body', 'html_body', 'attachments'}
        ))
        message = self._prepare_message(data=data)
        with SMTP(host=self._hostname, port=self._port, timeout=self._timeout) as smtp:
            if self._use_tls:
                context = ssl.create_default_context()
                smtp.starttls(context=context)
            smtp.login(user=self._username, password=self._password)
            result = smtp.send_message(msg=message, from_addr=data.from_, to_addrs=data.to + data.cc + data.bcc)
            self._logger.info('Response=%s result=%s', request_id, result)
            return result
