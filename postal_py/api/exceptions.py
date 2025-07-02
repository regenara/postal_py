class PostalPyAPIError(Exception):
    """Base exception class for all PostalPy API-related errors."""


class PostalPyInvalidServerAPIKeyError(PostalPyAPIError):
    """The API token provided in X-Server-API-Key was not valid."""


class PostalPyAccessDeniedError(PostalPyAPIError):
    """Must be authenticated as a server"""


class PostalPyMessageNotFoundError(PostalPyAPIError):
    """No message found matching provided ID"""


class PostalPyValidationError(PostalPyAPIError):
    """The provided data was not sufficient to send an email"""


class PostalPyNoRecipientsError(PostalPyAPIError):
    """There are no recipients defined to received this message"""


class PostalPyNoContentError(PostalPyAPIError):
    """There is no content defined for this e-mail"""


class PostalPyTooManyToAddressesError(PostalPyAPIError):
    """The maximum number of To addresses has been reached (maximum 50)"""


class PostalPyTooManyCCAddressesError(PostalPyAPIError):
    """The maximum number of CC addresses has been reached (maximum 50)"""


class PostalPyTooManyBCCAddressesError(PostalPyAPIError):
    """The maximum number of BCC addresses has been reached (maximum 50)"""


class PostalPyFromAddressMissingError(PostalPyAPIError):
    """The From address is missing and is required"""


class PostalPyUnauthenticatedFromAddressError(PostalPyAPIError):
    """The From address is not authorised to send mail from this server"""


class PostalPyAttachmentMissingNameError(PostalPyAPIError):
    """An attachment is missing a name"""


class PostalPyAttachmentMissingDataError(PostalPyAPIError):
    """An attachment is missing data"""


class PostalPyConnectTimeoutError(PostalPyAPIError):
    """The request to the Postal API timed out while attempting to connect."""


class PostalPyMovedPermanentlyError(PostalPyAPIError):
    """The resource has been permanently moved (HTTP 301). Try using HTTPS instead of HTTP."""


class PostalPyPermanentRedirectError(PostalPyAPIError):
    """The resource has been permanently redirected (HTTP 308). Try using HTTPS instead of HTTP."""


class PostalPyInternalServerError(PostalPyAPIError):
    """The Postal server encountered an internal error (HTTP 500)."""


class PostalPyServiceUnavailableError(PostalPyAPIError):
    """The Postal service is temporarily unavailable (HTTP 503)."""


class PostalPyUnknownError(PostalPyAPIError):
    """An unknown error occurred while communicating with the Postal API."""
