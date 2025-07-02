from pydantic import (BaseModel as PydanticBaseModel,
                      Field)


class BaseModel(PydanticBaseModel):
    model_config = {
        'populate_by_name': True
    }


class SMTPAttachmentSchema(BaseModel):
    filename: str
    content_type: str = 'application/octet-stream'
    data: str | bytes


class SMTPMessageSchema(BaseModel):
    to: list[str] = Field(default_factory=list)
    cc: list[str] = Field(default_factory=list)
    bcc: list[str] = Field(default_factory=list)
    from_: str = Field(None, alias='from')
    subject: str | None = None
    reply_to: str | None = None
    plain_body: str | None = None
    html_body: str | None = None
    attachments: list[SMTPAttachmentSchema] = Field(default_factory=list)
    headers: dict[str, str] = Field(default_factory=dict)
