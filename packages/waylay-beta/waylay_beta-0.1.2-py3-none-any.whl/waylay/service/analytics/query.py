"""definitions for the 'query' entity of the 'analytics' Service"""

from .._base import WaylayResource
from .._decorators import (
    return_path_decorator
)
from ._decorators import (
    analytics_exception_decorator,
    analytics_return_dataframe_decorator,
    MultiFrameHandling
)


def parse_query_entity(json_dict: dict):
    """default response constructor for query config entities"""
    return json_dict


CONFIG_ENTITY_DECORATORS = [
    analytics_exception_decorator,
    return_path_decorator(['query'], parse_query_entity)
]

CONFIG_LIST_DECORATORS = [
    analytics_exception_decorator,
    return_path_decorator(['queries', 'name'])
]

DATA_RESPONSE_DECORATORS = [
    analytics_exception_decorator,
    analytics_return_dataframe_decorator(
        'data',
        default_frames_handling=MultiFrameHandling.JOIN
    )
]


class QueryResource(WaylayResource):
    """REST Resource for the 'query' entity of the 'analytics' Service"""
    actions = {
        'list': {
            'method': 'GET',
            'url': '/config/query',
            'decorators': CONFIG_LIST_DECORATORS,
            'description': 'List or search <em>Query Configurations</em>'},
        'create': {
            'method': 'POST',
            'url': '/config/query',
            'decorators': CONFIG_ENTITY_DECORATORS,
            'description': 'Create a new <em>Query Configuration</em>'},
        'get': {
            'method': 'GET',
            'url': '/config/query/{}',
            'decorators': CONFIG_ENTITY_DECORATORS,
            'description': 'Fetch the named <em>Query Configuration</em>'},
        'remove': {
            'method': 'DELETE',
            'url': '/config/query/{}',
            'decorators': CONFIG_ENTITY_DECORATORS,
            'description': 'Remove the named <em>Query Configuration</em>'},
        'replace': {
            'method': 'PUT',
            'url': '/config/query/{}',
            'decorators': CONFIG_ENTITY_DECORATORS,
            'description': 'Replace the named <em>Query Configuration</em>'},
        'data': {
            'method': 'GET',
            'url': '/data/query/{}',
            'decorators': DATA_RESPONSE_DECORATORS,
            'description': 'Execute the timeseries query specified by the named <em>Query Configuration</em>'},
        'execute': {
            'method': 'POST',
            'url': '/data/query',
            'decorators': DATA_RESPONSE_DECORATORS,
            'description': 'Execute the timeseries query specified in the request'},
    }
