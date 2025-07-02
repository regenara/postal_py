import logging
from uuid import uuid4

try:
    from aiosmtplib import (SMTP,
                            SMTPResponse)
except ImportError:
    SMTP = None
    SMTPResponse = None

from .base import PostalPySMTPBase
from .schemas import SMTPMessageSchema


class PostalPySMTP(PostalPySMTPBase):
    def __init__(self, hostname: str, username: str, password: str, port: int = 25, use_tls: bool = True,
                 timeout: int = 5, level: logging = logging.INFO):
        """
        Asynchronous SMTP client for sending messages via a configured SMTP relay.
        Requires `aiosmtplib`. Install with `pip install postal_py[smtp]`.
        """
        if SMTP is None:
            raise ImportError(
                'Async SMTP support is not available. To enable it, install extra dependencies with:\n'
                '    pip install postal_py[smtp]'
            )
        super().__init__(hostname=hostname, port=port, username=username, password=password, use_tls=use_tls,
                         timeout=timeout, level=level)

    async def send_message(self, data: SMTPMessageSchema) -> tuple[dict[str, SMTPResponse], str]:
        request_id = uuid4().hex
        self._logger.info('Request=%s data=%s', request_id, data.model_dump(
            exclude_none=True, exclude={'plain_body', 'html_body', 'attachments'}
        ))
        message = self._prepare_message(data=data)
        smtp = SMTP(hostname=self._hostname, port=self._port, timeout=self._timeout, start_tls=self._use_tls)
        await smtp.connect()
        await smtp.login(self._username, self._password)
        result = await smtp.sendmail(data.from_, data.to + data.cc + data.bcc, message.as_string())
        await smtp.quit()
        self._logger.info('Response=%s result=%s', request_id, result)
        return result
