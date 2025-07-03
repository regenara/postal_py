import logging
from email.message import EmailMessage

from .schemas import SMTPMessageSchema


class PostalPySMTPBase:
    def __init__(self, hostname: str, port: int, username: str, password: str, use_tls: bool, timeout: int,
                 level: logging):
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password
        self._use_tls = use_tls
        self._timeout = timeout
        self._logger = logging.getLogger('PostalPySMTP')
        self._logger.setLevel(level)

    @staticmethod
    def _prepare_message(data: SMTPMessageSchema) -> EmailMessage:
        message = EmailMessage()
        message['From'] = data.from_
        if data.to:
            message['To'] = ', '.join(data.to)
        if data.cc:
            message['Cc'] = ', '.join(data.cc)
        if data.subject is not None:
            message['Subject'] = data.subject
        if data.reply_to is not None:
            message['Reply-To'] = data.reply_to
        if data.plain_body is not None:
            message.set_content(data.plain_body)
        if data.html_body is not None:
            message.add_alternative(data.html_body, subtype='html')
        for attachment in data.attachments:
            maintype, subtype = attachment.content_type.split('/')
            message.add_attachment(attachment.data, maintype=maintype, subtype=subtype, filename=attachment.name)
        for k, v in data.headers.items():
            message[k] = v
        return message
