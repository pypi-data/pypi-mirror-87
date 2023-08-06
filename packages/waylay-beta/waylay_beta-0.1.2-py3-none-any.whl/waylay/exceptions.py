"""Base exception class hierarchy for errors in the waylay client"""
from simple_rest_client.exceptions import ErrorWithResponse as _ErrorWithResponse


class WaylayError(Exception):
    """Root class for all exceptions raised by this module"""


class AuthError(WaylayError):
    """Exception class for waylay authentication errors"""


class ConfigError(WaylayError):
    """Exception class for waylay client configuration"""


class RestError(WaylayError):
    """Exception class for failures to make a rest call"""


class RestRequestError(RestError):
    """
    Exception class for failures to prepare a rest call
    (before http execution)
    """


class RestResponseError(RestError):
    """Exception class wrapping the response data of a Rest call"""

    def __init__(self, message, response):
        super().__init__(message)
        self.response = response

    @property
    def message(self):
        """basic user message for this error"""
        return self.args[0]

    def __str__(self):
        return (
            f"{self.__class__.__name__}({self.response.status_code}: " +
            f"'{self.message}'; {self.response.method} '{self.response.url}')"
        )

    def _get_from_body(self, key, default_value):
        error_resp_body = self.response.body
        if isinstance(error_resp_body, dict):
            return error_resp_body.get(key, default_value)
        return default_value

    @classmethod
    def from_cause(cls, cause: _ErrorWithResponse):
        """converts a rest client error to a waylay client error"""
        return cls(cause.message.split(',')[0], cause.response)


class RestResponseParseError(RestResponseError):
    """Exception raised when a successfull http request (200) could not be parsed succesfully."""
