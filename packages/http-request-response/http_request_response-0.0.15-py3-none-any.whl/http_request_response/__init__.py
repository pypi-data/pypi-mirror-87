from functools import wraps

from flask import current_app as app
from flask import request, has_request_context
from flask_jwt_extended import get_jwt_identity
from http_status_code.standard import bad_request


class RequestResponse:

    def __init__(self, status_code=None, data=None, message=None):
        self.status_code = status_code
        self.data = data
        self.message = self.__message_to_str(message)

    def update(self, status_code=200, data=None, message=None):
        self.status_code = status_code
        self.data = data
        self.message = self.__message_to_str(message)

    def __message_to_str(self, message):
        return message if message is None else str(message)

    def __call__(self, *args, **kwargs):
        return self.__dict__


class RequestUtilities:
    @staticmethod
    def get_request_context():
        context = dict()
        if has_request_context():
            context['url'] = request.url
            context['remote_addr'] = request.remote_addr
            context['method'] = request.method

            # Query string args
            context['original_qs_args'] = request.args
            context['processed_qs_args'] = request.qs_args

            # Body args
            try:
                for key in request.body_args:
                    if 'password' in key or 'db_uri' in key:
                        request.body_args.pop(key, None)

                for key in request.json:
                    if 'password' in key or 'db_uri' in key:
                        request.json.pop(key, None)
            except:
                pass

            request.body_args.pop('file_bytes', None)  # Pop any file bytes
            context['original_body_args'] = request.json
            context['processed_body_args'] = request.body_args

            try:
                context['claims'] = request.claims
            except:
                # Claims are not available in case of login endpoint and when the token is not provided
                pass

        return context

    @staticmethod
    def try_except(fn):
        """A decorator for all of the actions to do try except"""

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                status, data = fn(*args, **kwargs)

                if app.config.get('ENV_NAME') != 'Development':
                    # Do not log INFO to development server
                    try:
                        app.app_info_logger.info(RequestUtilities.get_request_context())
                    except:
                        pass


            except Exception as e:
                status, data = bad_request, None
                if app.config.get('ENV_NAME') != 'Production':
                    status.update_msg(e)
                else:
                    # Do not return the Exception to the user, on the prouction server
                    status.update_msg(f'Something went wrong. Error code: {status.code}')

                # Always log Exceptions
                try:
                    app.app_exc_logger.exception(RequestUtilities.get_request_context())
                except:
                    pass

            rs = RequestResponse(status_code=status.code, message=status.message, data=data)
            return rs()

        return wrapper
