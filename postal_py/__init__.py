from contextlib import suppress

from .api.async_wrapper import PostalPyAPI as AsyncPostalPyAPI
from .api.wrapper import PostalPyAPI
from .smtp.wrapper import PostalPySMTP

with suppress(ImportError):
    from .smtp.async_wrapper import PostalPySMTP as AsyncPostalPySMTP
