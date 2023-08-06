"""REST definitions for version status of Waylay Analytics service"""

from .._base import WaylayResource
from .._decorators import (
    exception_decorator,
    return_body_decorator
)

DEFAULT_DECORATORS = [exception_decorator, return_body_decorator]


class AboutResource(WaylayResource):
    """static information about version and feature flags"""
    actions = {
        'version': {
            'method': 'GET',
            'url': '/',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Version info of the <em>Analytics Service</em> at this endpoint.'}
    }
