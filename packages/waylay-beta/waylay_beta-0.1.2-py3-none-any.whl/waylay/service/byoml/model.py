"""REST definitions for the 'model' entity of the 'byoml' service"""
from zipfile import ZipFile
from io import BytesIO
from functools import wraps
from typing import Callable, List
import joblib

import pandas as pd
import numpy as np

from .._base import WaylayResource
from .._decorators import (
    return_body_decorator,
    return_path_decorator,
    suppress_header_decorator
)
from ._decorators import (
    byoml_exception_decorator
)
from ...exceptions import (
    RestRequestError
)


def _input_data_as_list(input_data):
    if isinstance(input_data, list):
        return input_data
    if isinstance(input_data, pd.DataFrame):
        return input_data.values.tolist()
    # numpy nd_array
    try:
        return input_data.tolist()
    except (ValueError, TypeError):
        pass
    raise RestRequestError(
        f'input data of unsupported type {type(input_data)}'
    )


def model_execution_request_decorator(action_method):
    """
    Decorator that prepares an execution of the model (predict, regress, classify, ...)
    """
    @wraps(action_method)
    def wrapped(model_name, input_data, **kwargs):
        request_body = {
            'instances': _input_data_as_list(input_data)
        }
        return action_method(
            model_name,
            body=request_body,
            **kwargs
        )
    return wrapped


DEFAULT_DECORATORS = [byoml_exception_decorator, return_body_decorator]


def _execute_model_decorators(response_key: str) -> List[Callable]:
    return [
        byoml_exception_decorator,
        model_execution_request_decorator,
        return_path_decorator(
            [response_key],
            default_response_constructor=np.array
        )
    ]


DEFAULT_BYOML_MODEL_TIMEOUT = 60


class ModelResource(WaylayResource):
    """REST Resource for the 'model' entity of the 'byoml' service"""
    actions = {
        'list': {
            'method': 'GET',
            'url': '/models',
            'decorators': [
                byoml_exception_decorator,
                return_path_decorator(['available_models'])
            ],
            'description': 'List the metadata of the deployed <em>BYOML Models</em>'},
        'list_names': {
            'method': 'GET',
            'url': '/models',
            'decorators': [
                byoml_exception_decorator,
                return_path_decorator(['available_models', 'name'])
            ],
            'description': 'List the names of deployed <em>BYOML Models</em>'},
        '_create': {
            'method': 'POST',
            'url': '/models',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Build and create a new <em>BYOML Model</em> as specified in the request'},
        '_replace': {
            'method': 'PUT',
            'url': '/models/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Build and replace the named <em>BYOML Model</em>'},
        'get': {
            'method': 'GET',
            'url': '/models/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Fetch the metadata of the named <em>BYOML Model</em>'},
        'examples': {
            'method': 'GET',
            'url': '/models/{}/examples',
            'decorators': [
                byoml_exception_decorator,
                return_path_decorator(['example_payloads'])
            ],
            'description': 'Fetch the <em>example request input</em> of the named <em>BYOML Model</em>'},
        'predict': {
            'method': 'POST',
            'url': '/models/{}/predict',
            'decorators': _execute_model_decorators('predictions'),
            'description': 'Execute the <em>predict</em> capability of the named <em>BYOML Model</em>'},
        'regress': {
            'method': 'POST',
            'url': '/models/{}/regress',
            'decorators': _execute_model_decorators('result'),
            'description': 'Execute the <em>regress</em> capability of the named  <em>BYOML Model</em>'},
        'classify': {
            'method': 'POST',
            'url': '/models/{}/classify',
            'decorators': _execute_model_decorators('result'),
            'description': 'Execute the <em>classification</em> capability of the named <em>BYOML Model</em>'},
        'remove': {
            'method': 'DELETE',
            'url': '/models/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Remove the named <em>BYOML Model</em>'},
    }

    def __init__(self, *args, **kwargs):
        kwargs.pop('timeout', None)
        super().__init__(*args, timeout=DEFAULT_BYOML_MODEL_TIMEOUT, **kwargs)

    def _send_model_arguments(
        self, model_name, trained_model,
        framework="sklearn", description=""
    ):
        """uploads a binary model with given name, framework and description."""
        # write the model to a file, and put the file in a zipped buffer
        joblib.dump(trained_model, './model.joblib')
        model_zip_buffer = BytesIO()
        with ZipFile(model_zip_buffer, 'w') as zipper:
            zipper.write('model.joblib')
        return {
            'body': {
                "name": model_name,
                "framework": framework,
                "description": description
            },
            'files': {
                "file": ('model.zip', model_zip_buffer.getvalue())
            },
        }

    @suppress_header_decorator('Content-Type')
    def upload(
        self, model_name, trained_model,
        framework="sklearn", description="", **kwargs
    ):
        """uploads a new machine learning model with given name, framework and description."""
        return getattr(self, '_create')(
            **self._send_model_arguments(
                model_name, trained_model,
                framework=framework, description=description,
            ),
            **kwargs
        )

    @suppress_header_decorator('Content-Type')
    def replace(
        self, model_name, trained_model,
        framework="sklearn", description="", **kwargs
    ):
        """replaces a machine learning model with given name, framework and description."""
        return getattr(self, '_replace')(
            model_name,
            **self._send_model_arguments(
                model_name, trained_model,
                framework=framework, description=description,
            ),
            **kwargs
        )
