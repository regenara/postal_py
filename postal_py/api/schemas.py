import base64
from enum import Enum
from typing import Any

from pydantic import (BaseModel as PydanticBaseModel,
                      ConfigDict,
                      Field,
                      field_validator,
                      conlist)


class BaseModel(PydanticBaseModel):
    model_config = {
        'populate_by_name': True
    }


class ResponseStatus(str, Enum):
    success = 'success'
    parameter_error = 'parameter-error'
    error = 'error'


class ResponseCode(str, Enum):
    ACCESS_DENIED = 'AccessDenied'
    INVALID_SERVER_API_KEY = 'InvalidServerAPIKey'
    MESSAGE_NOT_FOUND = 'MessageNotFound'
    VALIDATION_ERROR = 'ValidationError'
    NO_RECIPIENTS = 'NoRecipients'
    NO_CONTENT = 'NoContent'
    TOO_MANY_TO_ADDRESSES = 'TooManyToAddresses'
    TOO_MANY_CC_ADDRESSES = 'TooManyCCAddresses'
    TOO_MANY_BCC_ADDRESSES = 'TooManyBCCAddresses'
    FROM_ADDRESS_MISSING = 'FromAddressMissing'
    UNAUTHENTICATED_FROM_ADDRESS = 'UnauthenticatedFromAddress'
    ATTACHMENT_MISSING_NAME = 'AttachmentMissingName'
    ATTACHMENT_MISSING_DATA = 'AttachmentMissingData'


class MessageExpansion(str, Enum):
    all = 'all'
    status = 'status'
    details = 'details'
    inspection = 'inspection'
    plain_body = 'plain_body'
    html_body = 'html_body'
    attachments = 'attachments'
    headers = 'headers'
    raw_message = 'raw_message'
    activity_entries = 'activity_entries'


class RequestAttachmentSchema(BaseModel):
    name: str
    content_type: str | None = None
    data: str | bytes

    @field_validator('data', mode='before')
    @classmethod
    def to_base64(cls, value: str | bytes) -> str:
        if isinstance(value, bytes):
            value = base64.b64encode(value).decode()
        return value


class ResponseAttachmentSchema(BaseModel):
    filename: str
    content_type: str | None = None
    data: str
    size: int
    hash: str


class ResponseStatusSchema(BaseModel):
    status: str
    last_delivery_attempt: float
    held: bool
    hold_expiry: Any


class ResponseDetailsSchema(BaseModel):
    rcpt_to: str
    mail_from: str
    subject: str | None
    message_id: str
    timestamp: float
    direction: str
    size: int
    bounce: bool
    bounce_for_id: int
    tag: str | None
    received_with_ssl: bool


class ResponseInspectionSchema(BaseModel):
    inspected: bool
    spam: bool
    spam_score: float
    threat: bool
    threat_details: Any | None


class ResponseHeadersSchema(BaseModel):
    model_config = ConfigDict(extra='allow')

    received: list[str]
    date: list[str]
    from_: list[str] = Field(..., alias='from')
    to: list[str]
    message_id: list[str] = Field(..., alias='message-id')
    subject: list[str] | None = None
    mime_version: list[str] = Field(..., alias='mime-version')
    content_type: list[str] = Field(..., alias='content-type')
    content_transfer_encoding: list[str] = Field(..., alias='content-transfer-encoding')


class ResponseLoadSchema(BaseModel):
    ip_address: str
    user_agent: str
    timestamp: str


class ResponseClickSchema(ResponseLoadSchema):
    url: str


class ResponseActivitySchema(BaseModel):
    loads: list[ResponseLoadSchema]
    clicks: list[ResponseClickSchema]


class ResponseMessageDataSchema(BaseModel):
    id: int | None = None
    token: str | None = None
    status: ResponseStatusSchema | None = None
    details: ResponseDetailsSchema | None = None
    inspection: ResponseInspectionSchema | None = None
    plain_body: str | None = None
    html_body: str | None = None
    attachments: list[ResponseAttachmentSchema] | None = None
    headers: ResponseHeadersSchema | None = None
    raw_message: str | None = None
    activity_entries: ResponseActivitySchema | None = None
    message: str | None = None
    code: str | None = None


class ResponseMessageEntrySchema(BaseModel):
    id: int
    token: str


class ResponseMessagesDataSchema(BaseModel):
    message_id: str
    messages: dict[str, ResponseMessageEntrySchema]


class ResponseStructureDataSchema(BaseModel):
    id: int
    status: str
    details: str
    output: str
    sent_with_ssl: bool
    log_id: str
    time: float
    timestamp: float


class ResponseSchema(BaseModel):
    status: ResponseStatus
    time: float
    flags: dict[str, Any]
    data: ResponseMessageDataSchema | list[ResponseStructureDataSchema] | ResponseMessagesDataSchema


class RequestMessageDetailsSchema(BaseModel):
    id: int
    expansions: set[MessageExpansion] | None = None


class RequestMessageSchema(BaseModel):
    to: conlist(str, max_length=50) | None = None
    cc: conlist(str, max_length=50) | None = None
    bcc: conlist(str, max_length=50) | None = None
    from_: str | None = Field(None, alias='from')
    sender: str | None = None
    subject: str | None = None
    tag: str | None = None
    reply_to: str | None = None
    plain_body: str | None = None
    html_body: str | None = None
    attachments: list[RequestAttachmentSchema] | None = None
    headers: dict[str, Any] | None = None
    bounce: bool | None = None


class RequestRawMessageSchema(BaseModel):
    mail_from: str
    rcpt_to: list[str]
    data: str
    bounce: bool | None = None
