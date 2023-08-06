"""exceptions specific to the Byoml Service"""

from ...exceptions import RestResponseError, RestResponseParseError


class ByomlActionError(RestResponseError):
    """error that represents the json messages of a byoml response"""

    @property
    def message(self):
        """the main user error returned by an analytics error response"""
        return self._get_from_body('error', super().message)


class ByomlActionParseError(RestResponseParseError, ByomlActionError):
    """Indicates that a byoml response could not be parsed"""
