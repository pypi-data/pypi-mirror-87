"""Base classes for Waylay REST Services and Resources"""

from typing import (
    Optional, Type, TypeVar,
    Mapping
)
try:
    from typing import Protocol
except ImportError:
    # typing.Protocol is a 3.8 feature ...
    # ... but typing_extensions provides forward compatibility.
    from typing_extensions import Protocol  # type: ignore

from simple_rest_client.api import Resource, API
from waylay.config import WaylayConfig

S = TypeVar('S', bound='WaylayService')
R = TypeVar('R', bound='WaylayResource')


class WaylayServiceContext(Protocol):
    """view protocol for the dynamic service context"""

    def get(self, service_class: Type[S]) -> Optional[S]:
        """returns the service instances for the given class, if available"""

    def require(self, service_class: Type[S]) -> S:
        """returns the service instances for the given class, raise ConfigError otherwise"""


DEFAULT_SEVICE_TIMEOUT = 10


class WaylayResource(Resource):
    """
    Client object representing a Waylay Resource, i.e. a collection of REST
    operations that have a single Waylay Entity as subject.
    """

    def add_action(self, action_name: str):
        """add action, and expect whether any decorators need to be applied"""
        super().add_action(action_name)
        self.decorate_action(action_name)

    def decorate_action(self, action_name):
        """decorates the action if a 'decorators' definition exist"""
        action = self.get_action(action_name)
        decorators = action.get('decorators', None)
        if decorators:
            for decorator in decorators:
                setattr(self, action_name, decorator(getattr(self, action_name)))

    def __repr__(self):
        actions_repr = ', '.join(
            f"{name}: '{action_def['method']} {action_def['url']}'"
            for name, action_def in self.actions.items()
        )
        return (
            f"<{self.__class__.__name__}("
            f"actions=[{actions_repr}]"
            ")>"
        )


class WaylayService(API):
    """
    Client object representing a Waylay Service, i.e. a collection of
    Resources with their operations.
    """
    service_key: str = ''
    config_key: str = 'api'
    default_root_url: str = ''
    config: Optional[WaylayConfig] = None
    resource_definitions: Mapping[str, Type[Resource]] = {}
    plugin_priority = 0

    def __init__(self, *args, **kwargs):
        timeout = kwargs.pop('timeout', DEFAULT_SEVICE_TIMEOUT)
        super().__init__(*args, timeout=timeout, **kwargs)
        for name, resource_class in self.resource_definitions.items():
            self.add_resource(resource_name=name, resource_class=resource_class)

    def _add_waylay_resource(self, resource_name: str, resource_class: Type[R], **kwargs) -> R:
        """add resource and return the initialized result"""
        self.add_resource(resource_name=resource_name, resource_class=resource_class, **kwargs)
        waylay_resource: R = self._resources[self.correct_attribute_name(resource_name)]
        return waylay_resource

    def set_root_url(self, root_url):
        self.config.set_root_url(self.config_key, root_url)
        self.reconfigure()

    def get_root_url(self) -> Optional[str]:
        if self.config is None:
            return self.default_root_url
        return self.config.get_root_url(self.config_key, self.default_root_url)

    def configure(self: S, config: WaylayConfig, context: WaylayServiceContext) -> S:
        """configure endpoints and authentication with given config. Returns self"""
        self.config = config
        return self.reconfigure()

    def reconfigure(self: S) -> S:
        if self.config is None:
            return self
        root_url = self.get_root_url()
        for resource in self._resources.values():
            resource.api_root_url = root_url
            resource.client.auth = self.config.auth
        return self

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"service_key={self.service_key},"
            f"config_key={self.config_key},"
            f"root_url={self.get_root_url()},"
            f"resources=[{', '.join(self._resources.keys())}]"
            ")>"
        )
