"""Waylay Rest Services"""
from .analytics import AnalyticsService
from ._base import WaylayService, WaylayResource, WaylayServiceContext
from .byoml import ByomlService
from . import _decorators as decorators

SERVICES = [
    AnalyticsService, ByomlService
]
