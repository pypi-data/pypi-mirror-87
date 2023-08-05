""" Flask specific decorators (primarily for auth activities and app context)
"""
import os
import logging
from http import HTTPStatus
from functools import wraps
import requests
from rhodb.redis_conf import RedisConnector
from flask import current_app, request
from rho_web.response import abort
from sermos.flask import oidc
from sermos.constants import DEFAULT_BASE_URL, AUTH_LOCK_KEY, \
    AUTH_LOCK_DURATION

logger = logging.getLogger(__name__)
redis_conn = RedisConnector().get_connection()


def require_login(fn):
    """ Utilize Flask RhoAuth to secure a route with @require_login decorator
    """
    secure_fn = oidc.require_login(fn)

    @wraps(fn)
    def decorated(*args, **kwargs):
        if str(current_app.config['RHOAUTH_ENABLED']).lower() == 'true':
            return secure_fn(*args, **kwargs)
        return fn(*args, **kwargs)

    return decorated


def require_permission(roles=[]):
    def wrapper(fn):
        secure_fn = oidc.require_permission(roles=roles)(fn)

        @wraps(fn)
        def decorated(*args, **kwargs):
            if str(current_app.config['RHOAUTH_ENABLED']).lower() == 'true':
                return secure_fn(*args, **kwargs)
            return fn(*args, **kwargs)

        return decorated

    return wrapper


# TODO this needs to be updated to distinguish between a sermos access key
# and a customer application's API keys
def validate_api_key(api_key: str):
    """ Verify whether an API key is valid according to Sermos
    """
    if api_key is None:
        api_key = os.environ.get('SERMOS_ACCESS_KEY', None)

    if api_key is None:
        return False

    # Ask cache first
    validated = redis_conn.get(AUTH_LOCK_KEY)
    if validated is not None:
        return True

    # Ask Sermos
    headers = {'apikey': api_key}
    admin_api_endpoint = DEFAULT_BASE_URL + 'auth'
    r = requests.post(admin_api_endpoint, headers=headers, verify=True)

    if r.status_code == 200:
        redis_conn.setex(AUTH_LOCK_KEY, AUTH_LOCK_DURATION, '')
        return True
    return False


def require_apikey(fn):
    """ Convenience decorator to add to a web route (typically an API)
        when using Flask.

        Usage::
            from sermos import Blueprint, ApiServices
            bp = Blueprint('api_routes', __name__, url_prefix='/api')

            @bp.route('/my-api-route')
            class ApiClass(MethodView):
                @require_apikey
                def post(self, payload: dict):
                    return {}
    """
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        api_key = request.headers.get('apikey')
        if not api_key:
            api_key = request.args.get('apikey')

        if not api_key:
            abort(HTTPStatus.UNAUTHORIZED)

        if validate_api_key(api_key):
            return fn(*args, **kwargs)

        abort(HTTPStatus.UNAUTHORIZED)

    return decorated_view
