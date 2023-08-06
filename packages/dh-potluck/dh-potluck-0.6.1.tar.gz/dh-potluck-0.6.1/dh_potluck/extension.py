import importlib
import json
import logging
import os
import re
import threading
import traceback
from http import HTTPStatus
from urllib.parse import urlencode

import json_log_formatter
import pkg_resources
from boltons.iterutils import remap
from ddtrace import tracer
from flask import Blueprint, g, jsonify, render_template, request
from flask_limiter import Limiter
from flask_sqlalchemy import get_debug_queries
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException, InternalServerError
from werkzeug.middleware.proxy_fix import ProxyFix

from .auth import get_user, role_required
from .platform_connection import PlatformConnectionError
from .utils.term import Bell, TextColors

SENSITIVE_KEYS = re.compile(r'password|token|secret|key', flags=re.I)
MAX_BODY_SIZE = 50000
LOG_LEVEL_MAPPING = {
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
}


def scrub_keys(path, key, value):
    if isinstance(key, str) and SENSITIVE_KEYS.search(key):
        return key, '-' * 5
    return key, value


def structure_logger(logger):
    def patch_level_func(level_func, level):
        def _patch_level_func(*args, **kwargs):
            extra = {
                **kwargs.get('extra', {}),
                **{'level': level}
            }
            return level_func(*args, **{**kwargs, **{'extra': extra}})

        return _patch_level_func

    def patch_log_func(log_func):
        reversed_mapping = dict([reversed(i) for i in LOG_LEVEL_MAPPING.items()])

        def _patch_log_func(level, *args, **kwargs):
            extra = {
                **kwargs.get('extra', {}),
                **{'level': reversed_mapping.get(level)},
            }
            return log_func(level, *args, **{**kwargs, **{'extra': extra}})

        return _patch_log_func

    # Insert level into json log for each level function invocation
    # ex. logger.info, logger.warning
    for level in LOG_LEVEL_MAPPING.keys():
        func = getattr(logger, level.lower())
        setattr(logger, level.lower(), patch_level_func(func, level))

    # Insert level into json log for direct log function call
    # ex logger.log
    func = getattr(logger, 'log')
    setattr(logger, 'log', patch_log_func(func))

    # Assign JSON formatter to handler
    json_handler = logging.StreamHandler()
    json_handler.setFormatter(json_log_formatter.JSONFormatter())
    logger.handlers = [json_handler]
    logger.propagate = False


def patch_celery_get_logger():
    # This has the opportunity of being a patch closer to the source (kombu)
    # Imports safely hidden behind structured_logging flag for now
    try:
        from celery.utils import log

        def _patch_func(name):
            l = log._get_logger(name)  # noqa: E741
            if logging.root not in (l, l.parent) and l is not log.base_logger:
                l = log._using_logger_parent(log.base_logger, l)  # noqa: E741
            structure_logger(l)
            return l

        log.get_logger = _patch_func
    except ModuleNotFoundError:
        return


def add_request_params_to_trace():
    span = tracer.current_root_span()
    if not span:
        return

    # Log query string (if present) for all request methods
    query_params = request.args
    if query_params:
        clean = remap(query_params.copy(), visit=scrub_keys)
        span.set_tag('http.query_string', urlencode(clean))

    # Skip body logging if not POST, PATCH or PUT
    if request.method not in ['POST', 'PATCH', 'PUT']:
        return

    # Skip body logging if it's empty
    if not request.content_length:
        return

    span.set_tags({'http.content_length': request.content_length})

    if request.content_length > MAX_BODY_SIZE:
        span.set_tag('http.body', 'Body too large, content could not be logged.')
        return

    # Try to parse body as JSON, and scrub sensitive values
    body = request.get_json(silent=True)
    if body:
        clean = remap(body, visit=scrub_keys)
        span.set_tag('http.body', json.dumps(clean))
    else:
        # If we can't parse as JSON, log the raw body
        body = request.get_data(as_text=True)
        span.set_tag('http.body', body)


def get_database_queries_summary(app):
    queries = get_debug_queries()
    message = f'\n{TextColors.LIGHTYELLOW}Database Queries Summary'
    slow_query_time = app.config.get('DH_SLOW_DB_QUERY_TIME', 0.5)
    too_many_queries = app.config.get('DH_TOO_MANY_SQL_QUERIES', 10)
    total_query_time = 0
    select_queries_count = 0
    slow_queries = []
    for query in queries:
        total_query_time += query.duration
        if query.statement.startswith('SELECT'):
            select_queries_count += 1
        if query.duration > slow_query_time:
            slow_queries.append(query)
    message += f'\n\t{TextColors.BLUE}Select queries: {TextColors.RESET}{select_queries_count}'

    if len(queries) - select_queries_count > 0:
        message += (
            f'\n\t{TextColors.BLUE}Other queries: '
            f'{TextColors.RESET}{len(queries) - select_queries_count}'
        )
    message += f'\n\t{TextColors.BLUE}Total queries: {TextColors.RESET}{len(queries)}'
    message += f'\n\t{TextColors.BLUE}Total query time: {TextColors.RESET}{total_query_time:.2f}s'

    if slow_queries:
        message += (
            f'\n\t{TextColors.LIGHTRED}{Bell.BELL}[⚠️  WARNING] Slow queries '
            f'(>{slow_query_time}s): {len(slow_queries)}'
        )

    if len(queries) > too_many_queries:
        message += (
            f'\n\t{TextColors.LIGHTRED}{Bell.BELL}[⚠️  WARNING] Too many queries '
            f'(max {too_many_queries} queries)'
        )

    return message


class DHPotluck:
    def __init__(self, app=None, **kwargs):
        """Initialize dh-potluck."""
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        app_token = app.config['DH_POTLUCK_APP_TOKEN']
        validate_func_name = app.config.get(
            'DH_POTLUCK_VALIDATE_TOKEN_FUNC', 'dh_potluck.auth.validate_token_using_api'
        )
        module_name, class_name = validate_func_name.rsplit('.', 1)
        validate_token_func = getattr(importlib.import_module(module_name), class_name)

        # Adjust the WSGI environ based on X-Forwarded- headers that proxies in front of the
        # application may set.
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

        # Disable tracing when testing
        tracer.configure(enabled=not app.config.get('TESTING', False))
        tracer.set_tags(
            {'dh_potluck.version': pkg_resources.get_distribution('dh-potluck').version}
        )

        enable_rate_limiting = bool(app.config.get('RATELIMIT_ENABLED', 0))
        rate_limit = app.config.get('RATELIMIT_DEFAULT_PER_MINUTE', 1000)

        api_docs = Blueprint(
            'API Docs',
            __name__,
            url_prefix='/docs',
            template_folder='./templates'
            )
        api_docs.add_url_rule('',  view_func=self.render_docs)

        app.register_blueprint(api_docs)

        def key_func():
            if 'Authorization' in request.headers:
                return request.headers['Authorization'].split(' ')[1]
            else:
                ip = request.remote_addr
                if request.headers.getlist('X-Forwarded-For'):
                    ip = request.headers.getlist('X-Forwarded-For')[0]
                return ip

        self.limiter = Limiter(
            key_func=key_func,
            default_limits=[f'{rate_limit} per minute'],
            default_limits_per_method=False,
            headers_enabled=True,
            swallow_errors=True,
            enabled=enable_rate_limiting,
        )

        @self.limiter.request_filter
        def app_token_whitelist():
            return (
                request.headers.get('Authorization', '') == f'Application {app_token}'
            )

        self.limiter.init_app(app)

        @app.before_request
        def before_request():
            # Allow all OPTIONS requests so CORS works properly
            if request.method == 'OPTIONS':
                return
            if 'domo-session' in request.headers:
                span = tracer.current_span()
                if span:
                    span.set_tags(
                        {
                            'dh_potluck.domo.session': request.headers.get('domo-session'),
                        }
                    )
            return get_user(app_token, validate_token_func)

        # Catch webargs validation errors and return them in JSON format
        @app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
        def handle_unprocessable_entity(error):
            add_request_params_to_trace()
            response = {
                'description': 'Input failed validation.',
                'errors': error.exc.messages,
            }
            return jsonify(response), HTTPStatus.BAD_REQUEST

        # Catch marshmallow validation errors and return them in JSON format
        @app.errorhandler(ValidationError)
        def handle_validation_error(error):
            add_request_params_to_trace()
            response = {
                'description': 'Input failed validation.',
                'errors': error.messages,
            }
            return jsonify(response), HTTPStatus.BAD_REQUEST

        # Catch SQLAlchemy IntegrityErrors (usually unique constraint violations) and return them
        # in JSON format. TODO: Right now we return the database error as-is to the client. This
        # should be expanded to parse the integrity error and try to build a more structured,
        # user-friendly message about the error.
        @app.errorhandler(IntegrityError)
        def handle_integrity_errors(error):
            add_request_params_to_trace()
            return (
                jsonify(
                    {'description': f'Database integrity error: {error.orig.args[1]}'}
                ),
                HTTPStatus.BAD_REQUEST,
            )

        # Ensure all other Flask HTTP exceptions are returned in JSON format
        @app.errorhandler(HTTPException)
        def handle_flask_exceptions(error):
            add_request_params_to_trace()
            return jsonify({'description': error.description}), error.code

        # Add extra context to Datadog traces for server errors
        @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
        def handle_server_error(error):
            add_request_params_to_trace()
            error_response = (
                jsonify({'description': InternalServerError.description}),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

            return error_response

        @app.errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
        def handle_too_many_requests(error):
            error_response = (
                jsonify({'description': 'Too Many Requests!'}),
                HTTPStatus.TOO_MANY_REQUESTS,
            )

            if 'Authorization' in request.headers:
                key = key_func()
                cleaned_key = f'{key[0:4]}...{key[-4:-1]}'
            else:
                cleaned_key = request.remote_addr

            tracer.set_tags({'rate_limit_key': cleaned_key})

            return error_response

        @app.errorhandler(PlatformConnectionError)
        def handle_platform_connection_error(err):
            return jsonify({'description': str(err)}), HTTPStatus.BAD_REQUEST

        @app.after_request
        def after_request(response):
            if os.environ.get('FLASK_DEBUG', 'false') == 'true':
                message = get_database_queries_summary(app)
                app.logger.info(message)

            return response

        # Structured logging configuration
        if app.config.get('STRUCTURED_LOGGING'):

            # Configure root logger
            structure_logger(logging.getLogger())

            # Set all others
            for logger in [
                logging.getLogger(name) for name in logging.root.manager.loggerDict
            ]:
                structure_logger(logger)

            # Allow for celery logs to report log level to Datadog
            # TODO - remove this once Celery log configuration hooks are sorted
            patch_celery_get_logger()

            # Catch and log unhandled exceptions in JSON format
            @app.errorhandler(Exception)
            def handle_error(e):
                extra = {
                    'error.stack': traceback.format_exc(),
                    'error.kind': str(type(e)),
                    'logger.thread_name': threading.Thread.getName(
                        threading.current_thread()
                    ),
                }
                app.logger.error(str(e), extra=extra)
                return (
                    jsonify({'description': 'Internal Server Error.'}),
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                )

        # Datadog Profiling - ddtrace 0.39.0 required
        if app.config.get('DD_PROFILING'):
            import ddtrace.profiling.auto  # noqa: F401

    @staticmethod
    def role_required(*args, **kwargs):
        return role_required(*args, **kwargs)

    @property
    def current_user(self):
        return g.user

    def render_docs(self):
        """Render ReDoc for DH API Docs"""
        return render_template('dhdocs.html')
