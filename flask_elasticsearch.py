from typing import Any, Dict, Optional

from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from flask import Flask, _app_ctx_stack, current_app  # type: ignore


class FlaskElasticsearch:
    """Proxy for Elasticsearch connection that works with Flask.

    Documentation for Elasticseach:
      https://elasticsearch-py.readthedocs.io

    Documentation for Elasticseach DSL:
      https://elasticsearch-dsl.readthedocs.io
    """

    def __init__(self, app: Optional[Flask] = None, **kwds: Any):
        self.app = app
        if app is not None:
            self.init_app(app, **kwds)

    def init_app(self, app: Flask, **kwds: Any) -> None:
        app.config.setdefault('ELASTICSEARCH_HOST', None)
        app.config.setdefault('ELASTICSEARCH_TIMEOUT', 30)
        app.config.setdefault('ELASTICSEARCH_USERNAME', None)
        app.config.setdefault('ELASTICSEARCH_PASSWORD', None)

        default_options = {
            'verify_certs': True,
        }

        self.options = {
            **default_options,
            **kwds
        }

        app.teardown_appcontext(self.teardown)

    def connect(self) -> Elasticsearch:
        config = current_app.config

        host = config.get('ELASTICSEARCH_HOST')
        if not host:
            raise RuntimeError(
                'Cannot connect to elastic search without a host')

        options: Dict[str, Any] = {
            **self.options,
            'hosts': [host],
        }

        username = config.get('ELASTICSEARCH_USERNAME')
        password = config.get('ELASTICSEARCH_PASSWORD')

        if username and password:
            options['http_auth'] = (username, password)

        timeout = config.get('ELASTICSEARCH_TIMEOUT')
        if timeout is not None:
            options['timeout'] = timeout

        return connections.create_connection(**options)

    def get_connection(self) -> Optional[Elasticsearch]:
        ctx = _app_ctx_stack.top
        if ctx is None:
            return None

        if not hasattr(ctx, 'elasticsearch'):
            ctx.elasticsearch = self.connect()

        return ctx.elasticsearch

    def __getattr__(self, item: str) -> Any:
        connection = self.get_connection()

        if connection is None:
            return None

        return getattr(connection, item)

    def teardown(self, exception: Optional[Exception]) -> None:
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'elasticsearch'):
            connections.remove_connection('default')
            ctx.elasticsearch = None
