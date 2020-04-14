import typing
import json
import os
import functools
from http import HTTPStatus

import pkg_resources
import fastjsonschema
from flask import current_app, request, jsonify, make_response

from .log import logger

__all__ = (
    'get_schema_validator',
    'validate_schema',
    'REGISTRY_ENTRY_SCHEMA',
)

REGISTRY_ENTRY_SCHEMA = 'schemas/registry-entry-config.schema.json'

PACKAGE_NAME = __name__.split('.', 1)[0]
RESOURCE_PACKAGE_PATH = pkg_resources.get_distribution(PACKAGE_NAME).location
# store loaded schema validators and reuse
_VALIDATOR_CACHE = {}


class UnexpectedContentType(Exception):
    pass


def validator_stub(*args, **kwargs):  # pylint: disable=unused-argument
    current_app.logger.warning('Fake validator used; Schema not validated')


def get_schema_validator(filename, encoding='utf-8'):
    # type: (str, str) -> typing.Callable
    ''''''
    if filename not in _VALIDATOR_CACHE:
        try:
            fname = os.path.join(RESOURCE_PACKAGE_PATH, PACKAGE_NAME, filename)
            with open(fname, 'rt', encoding=encoding) as fp:
                schema = json.load(fp)
            schema_validator = fastjsonschema.compile(schema)
            _VALIDATOR_CACHE[filename] = schema_validator
        except (FileNotFoundError,
                json.decoder.JSONDecodeError,
                fastjsonschema.JsonSchemaDefinitionException) as exc:
            logger.error(
                'Malformed json: %s; Dummy validator used instead \'%s\'',
                exc,
                os.path.basename(filename)
            )

    return _VALIDATOR_CACHE.get(filename, validator_stub)


def validate_schema(filename):
    # type: (str) -> typing.Any
    schema_validator = get_schema_validator(filename)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # pylint: disable=unused-argument
            try:
                # Ensure content-type: 'application/json'
                content_type = request.content_type.lower().split(';', 1)[0]
                if content_type != 'application/json':
                    raise UnexpectedContentType('Content-type: application/json REQUIRED')
                # Ensure schema validation pass
                schema_validator(json.loads(request.data))
            except (fastjsonschema.JsonSchemaException,
                    json.JSONDecodeError,
                    UnexpectedContentType) as exc:
                if __debug__:
                    # logger.exception('JsonSchemaException: %s;', schema, exc_info=exc)
                    logger.debug('Payload: %s', request.data)
                return make_response(jsonify({
                    'status': 'error',
                    'message': str(exc),
                }), HTTPStatus.BAD_REQUEST)
            return func(*args, **kwargs)

        return wrapper

    return decorator
