import logging

from niquests.models import Response

from .exceptions import (PostalPyAccessDeniedError,
                         PostalPyAttachmentMissingDataError,
                         PostalPyAttachmentMissingNameError,
                         PostalPyFromAddressMissingError,
                         PostalPyInternalServerError,
                         PostalPyInvalidServerAPIKeyError,
                         PostalPyMessageNotFoundError,
                         PostalPyMovedPermanentlyError,
                         PostalPyNoContentError,
                         PostalPyNoRecipientsError,
                         PostalPyPermanentRedirectError,
                         PostalPyServiceUnavailableError,
                         PostalPyTooManyBCCAddressesError,
                         PostalPyTooManyCCAddressesError,
                         PostalPyTooManyToAddressesError,
                         PostalPyUnauthenticatedFromAddressError,
                         PostalPyUnknownError,
                         PostalPyValidationError)
from .schemas import (ResponseCode,
                      ResponseSchema,
                      ResponseStatus)


class PostalPyAPIBase:
    def __init__(self, base_url: str, api_key: str, timeout: int, level: logging):
        self._base_url = base_url
        self._timeout = timeout
        self._headers = {
            'X-Server-API-Key': api_key,
            'Content-Type': 'application/json'
        }
        self._logger = logging.getLogger('PostalPyAPI')
        self._logger.setLevel(level)

    def _handle_response(self, response: Response, request_id: str) -> ResponseSchema:
        if response.status_code != 200:
            exception = {
                301: PostalPyMovedPermanentlyError,
                308: PostalPyPermanentRedirectError,
                500: PostalPyInternalServerError,
                503: PostalPyServiceUnavailableError
            }.get(response.status_code, PostalPyUnknownError)
            self._logger.error('Response=%s status_code=%s reason=%s: %s', request_id, response.status_code,
                               response.reason or 'No reason', exception.__doc__)
            raise exception(exception.__doc__)
        json_response = response.json()
        result = ResponseSchema(**json_response)
        if result.status in (ResponseStatus.error, ResponseStatus.parameter_error):
            exception = {
                ResponseCode.ACCESS_DENIED: PostalPyAccessDeniedError,
                ResponseCode.INVALID_SERVER_API_KEY: PostalPyInvalidServerAPIKeyError,
                ResponseCode.MESSAGE_NOT_FOUND: PostalPyMessageNotFoundError,
                ResponseCode.VALIDATION_ERROR: PostalPyValidationError,
                ResponseCode.NO_RECIPIENTS: PostalPyNoRecipientsError,
                ResponseCode.NO_CONTENT: PostalPyNoContentError,
                ResponseCode.TOO_MANY_TO_ADDRESSES: PostalPyTooManyToAddressesError,
                ResponseCode.TOO_MANY_CC_ADDRESSES: PostalPyTooManyCCAddressesError,
                ResponseCode.TOO_MANY_BCC_ADDRESSES: PostalPyTooManyBCCAddressesError,
                ResponseCode.FROM_ADDRESS_MISSING: PostalPyFromAddressMissingError,
                ResponseCode.UNAUTHENTICATED_FROM_ADDRESS: PostalPyUnauthenticatedFromAddressError,
                ResponseCode.ATTACHMENT_MISSING_NAME: PostalPyAttachmentMissingNameError,
                ResponseCode.ATTACHMENT_MISSING_DATA: PostalPyAttachmentMissingDataError
            }[result.data.code]
            self._logger.error('Response=%s status_code=%s json_response=%s',
                               request_id, response.status_code, json_response)
            raise exception(json_response)
        self._logger.info('Response=%s status_code=%s json_response=%s',
                          request_id, response.status_code, json_response)
        return result
