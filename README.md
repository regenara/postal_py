# [PostalPy](https://pypi.org/project/postal-py/)

**PostalPy** is a Python library for integrating with the [Postal server](https://github.com/postalserver/postal) for
email delivery. It supports sending messages via the Postal API and SMTP in both synchronous and asynchronous modes.

**PostalPy** — это Python-библиотека для интеграции с [Postal server](https://github.com/postalserver/postal) для
email-рассылки. Библиотека поддерживает отправку сообщений через Postal API и SMTP в синхронном и асинхронном режимах.

## Features / Возможности

- Postal API
- SMTP
- Synchronous and asynchronous modes / Синхронный и асинхронный режимы
- Python 3.10+ compatible / Совместимость с Python 3.10+

## Installation / Установка

### Basic Installation (API + synchronous SMTP) / Базовая установка (API + синхронный SMTP)

```bash
pip install postal_py
```

### Installation with asynchronous SMTP Support / Установка с поддержкой асинхронного SMTP

```bash
pip install postal_py[smtp]
```

## Dependencies / Зависимости

- [`pydantic>=2.0.0,<3.0.0`](https://pydantic-docs.helpmanual.io/)
- [`niquests>=3.0.0,<4.0.0`](https://niquests.readthedocs.io/)
- [`aiosmtplib>=4.0.0,<5.0.0`](https://aiosmtplib.readthedocs.io/) *(only for async SMTP / только для асинхронного SMTP)*

## Usage Examples / Примеры использования

<details>
<summary><strong>Sync API client usage / Использование синхронного API-клиента</strong></summary>

```python
from postal_py import PostalPyAPI
from postal_py.api.schemas import (RequestMessageSchema,
                                   RequestAttachmentSchema,
                                   RequestRawMessageSchema,
                                   RequestMessageDetailsSchema,
                                   MessageExpansion)

API_KEY = 'your_api_key'


def main():
    postal = PostalPyAPI(base_url='https://example.com/', api_key=API_KEY, timeout=10)

    # Get message details
    result = postal.get_message_details(
        RequestMessageDetailsSchema(id=2362354, expansions=[MessageExpansion.all])
    )
    print(result)

    # Get deliveries for a message
    result = postal.get_message_deliveries(id=5168706)
    print(result)

    # Send a message
    data = RequestMessageSchema(
        to=['example_1@mail.com', 'example_2@mail.com'],
        cc=['example_3@mail.com'],
        bcc=['example_4@mail.com'],
        from_='MyCompany <mail@example.com>',
        sender='mail@example.com',
        subject='Subject',
        tag='my-tag',
        reply_to='reply@example.com',
        plain_body="This is the plain version",
        html_body='<p>This is the <b>HTML</b> version</p>',
        headers={
            'X-Tracking': True,
            'X-Postal-Tag': 'postal-tag'
        },
        attachments=[
            RequestAttachmentSchema(
                name='img.png',
                content_type='image/png',
                data='iVBesb...PaII='  # bytes or base64-encoded file
            )
        ]
    )
    result = postal.send_message(data=data)
    print(result)

    # Send a raw RFC2822 message
    data = RequestRawMessageSchema(
        mail_from='mail@example.com',
        rcpt_to=['example_1@mail.com', 'example_2@mail.com'],
        data="RnJvb...nZS4K"  # base64 encoded RFC2822 message
    )
    result = postal.send_raw_message(data=data)
    print(result)

    postal.close()


if __name__ == '__main__':
    main()
```

</details>

---


<details>
<summary><strong>Async API client usage / Использование асинхронного API-клиента</strong></summary>

```python
import asyncio

from postal_py import AsyncPostalPyAPI
from postal_py.api.schemas import (RequestMessageSchema,
                                   RequestAttachmentSchema,
                                   RequestRawMessageSchema,
                                   RequestMessageDetailsSchema,
                                   MessageExpansion)

API_KEY = 'your_api_key'


async def main():
    postal = AsyncPostalPyAPI(base_url='https://example.com/', api_key=API_KEY, timeout=10)

    # Get message details
    result = await postal.get_message_details(
        RequestMessageDetailsSchema(id=2362354, expansions=[MessageExpansion.all])
    )
    print(result)

    # Get deliveries for a message
    result = await postal.get_message_deliveries(id=5168706)
    print(result)

    # Send a message
    data = RequestMessageSchema(
        to=['example_1@mail.com', 'example_2@mail.com'],
        cc=['example_3@mail.com'],
        bcc=['example_4@mail.com'],
        from_='MyCompany <mail@example.com>',
        sender='mail@example.com',
        subject='Subject',
        tag='my-tag',
        reply_to='reply@example.com',
        plain_body="This is the plain version",
        html_body='<p>This is the <b>HTML</b> version</p>',
        headers={
            'X-Tracking': True,
            'X-Postal-Tag': 'postal-tag'
        },
        attachments=[
            RequestAttachmentSchema(
                name='img.png',
                content_type='image/png',
                data='iVBesb...PaII='  # bytes or base64-encoded file
            )
        ]
    )
    result = await postal.send_message(data=data)
    print(result)

    # Send a raw RFC2822 message
    data = RequestRawMessageSchema(
        mail_from='mail@example.com',
        rcpt_to=['example_1@mail.com', 'example_2@mail.com'],
        data="RnJvb...nZS4K"  # base64 encoded RFC2822 message
    )
    result = await postal.send_raw_message(data=data)
    print(result)

    await postal.close()


if __name__ == '__main__':
    asyncio.run(main())
```

</details>

---

<details>
<summary><strong>Sync SMTP client usage / Использование синхронного SMTP-клиента</strong></summary>

```python
from postal_py import PostalPySMTP
from postal_py.smtp.schemas import (SMTPAttachmentSchema,
                                    SMTPMessageSchema)

USERNAME = 'your_smtp_user'
PASSWORD = 'your_smtp_password'


def main():
    postal = PostalPySMTP(
        hostname='example.com',
        port=25,
        username=USERNAME,
        password=PASSWORD
    )

    data = SMTPMessageSchema(
        to=['example_1@mail.com', 'example_2@mail.com'],
        cc=['example_3@mail.com'],
        bcc=['example_4@mail.com'],
        from_='MyCompany <mail@example.com>',
        subject='Subject',
        plain_body="This is the plain version",
        html_body='<p>This is the <b>HTML</b> version</p>',
        headers={
            'X-Tracking': 'true',
            'X-Postal-Tag': 'postal-tag'
        },
        attachments=[
            SMTPAttachmentSchema(
                filename='img.png',
                content_type='image/png',
                data='bytes or base64-encoded file'
            )
        ]
    )

    postal.send_message(data=data)


if __name__ == '__main__':
    main()
```

</details>

---

<details>
<summary><strong>Async SMTP client usage / Использование асинхронного SMTP-клиента</strong></summary>

```python
import asyncio

from postal_py import AsyncPostalPySMTP
from postal_py.smtp.schemas import (SMTPAttachmentSchema,
                                    SMTPMessageSchema)

USERNAME = 'your_smtp_user'
PASSWORD = 'your_smtp_password'


async def main():
    postal = AsyncPostalPySMTP(
        hostname='example.com',
        port=25,
        username=USERNAME,
        password=PASSWORD
    )

    data = SMTPMessageSchema(
        to=['example_1@mail.com', 'example_2@mail.com'],
        cc=['example_3@mail.com'],
        bcc=['example_4@mail.com'],
        from_='MyCompany <mail@example.com>',
        subject='Subject',
        plain_body="This is the plain version",
        html_body='<p>This is the <b>HTML</b> version</p>',
        headers={
            'X-Tracking': 'true',
            'X-Postal-Tag': 'postal-tag'
        },
        attachments=[
            SMTPAttachmentSchema(
                filename='img.png',
                content_type='image/png',
                data='bytes or base64-encoded file'
            )
        ]
    )

    await postal.send_message(data=data)


if __name__ == '__main__':
    asyncio.run(main())
```

</details>


