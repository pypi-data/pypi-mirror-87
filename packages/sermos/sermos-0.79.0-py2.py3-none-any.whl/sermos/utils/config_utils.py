""" General utilities used frequently in configuration-related tasks.
"""
import os
import re
import logging
import json
from typing import Union, Any
from urllib.parse import urljoin
import requests
from rhodb.redis_conf import RedisConnector
from sermos.constants import DEFAULT_BASE_URL, PIPELINE_CONFIG_CACHE_KEY, \
    SCHEDULE_CONFIG_CACHE_KEY, CONFIG_REFRESH_RATE
from sermos.schedule_config_schema import ScheduleConfigSchema

logger = logging.getLogger(__name__)
redis_conn = RedisConnector().get_connection()


def get_admin_api_url(admin_api_url: Union[str, None] = None):
    """ Simple helper to get admin server url in a standard fashion.
    """
    if admin_api_url is None:
        return DEFAULT_BASE_URL
    return admin_api_url  # TOOD In future can add some validation here.


def get_admin_access_key(access_key: Union[str, None] = None,
                         env_var_name: str = 'SERMOS_ACCESS_KEY'):
    """ Simple helper to get admin server access key in a standard fashion. If
    one is provided, return it back. If not, look in environment for
    `env_var_name`. If that doesn't exist, raise useful error.
    """
    if access_key is not None:
        return access_key

    try:
        return os.environ[env_var_name]
    except KeyError:
        raise KeyError(
            f"{env_var_name} not found in this environment. Find a valid "
            "access key in your Sermos administration console.")

    if access_key is None:
        return os.environ[env_var_name]  # Raises if not in environment
    return access_key


def get_admin_deployment_id(deployment_id: Union[str, None] = None,
                            env_var_name: str = 'SERMOS_DEPLOYMENT_ID'):
    """ Simple helper to get the deployment id in a standard fashion. If
    one is provided, return it back. If not, look in environment for
    `env_var_name`. If that doesn't exist, raise useful error.
    """
    if deployment_id is not None:
        return deployment_id

    try:
        return os.environ[env_var_name]
    except KeyError:
        raise KeyError(
            f"{env_var_name} not found in this environment. Note: this is "
            "required when running a Celery worker as `beat`. Find this ID "
            "in your administration console. For local development, this can "
            "be any arbitrary string.")


def load_json_config_from_redis(key: str) -> Any:
    """ Load a json key from redis. Special carve out for keys explicitly set
    to "none".
    """
    val = redis_conn.get(key)
    if val is None or val.decode('utf-8').lower() == 'none':
        return None
    return json.loads(val)


def set_json_config_to_redis(key: str,
                             data: Union[dict, None],
                             refresh_rate: int = CONFIG_REFRESH_RATE):
    """ For Admin API actions (e.g. schedules/pipelines), deployments cache
    results. The standard method for doing this is through a refresh key, which
    is set in redis to expire after the CONFIG_REFRESH_RATE. This will set
    the cached key.

    Rationale for manually setting a "None" key instead of simply skipping
    is to protect against case of a spammed config request for an unknown
    pipeline, for example. This will still limit our requests to Sermos Admin
    based on the refresh rate even in that scenario.
    """
    if data is None:
        data = 'None'
    else:
        data = json.dumps(data)
    redis_conn.setex(key, refresh_rate, data)


def _generate_api_url(deployment_id: str,
                      admin_api_url: Union[str, None] = None,
                      endpoint: str = ''):
    """ Provide a normalized url based on the base url and endpoint and add in
        the deployment_id to the url, which is required for all
        pipeline/schedule endpoints.
    """
    return urljoin(get_admin_api_url(admin_api_url),
                   f'deployments/{deployment_id}/{endpoint}')


def retrieve_and_cache_config(key: str,
                              admin_api_endpoint: str,
                              access_key: str,
                              refresh_rate: int = CONFIG_REFRESH_RATE) -> Any:
    """ Attempt to retrieve API response from Sermos Config Server and cache
    the response for CONFIG_REFRESH_RATE seconds in local Redis. Return the
    cached version if it already exists.
    """
    conf = load_json_config_from_redis(key)
    if conf is not None:
        return conf

    headers = {'apikey': access_key}
    r = requests.get(admin_api_endpoint, headers=headers, verify=True)

    data = None
    if r.status_code == 200:
        data = r.json()
    else:
        logger.warning(f"Non-200 response retrieving {admin_api_endpoint}: "
                       f"{r.status_code}, {r.reason}")

    # Cache result
    if data is not None:
        set_json_config_to_redis(key, data, refresh_rate)

    return data


def retrieve_latest_pipeline_config(
        deployment_id: Union[str, None] = None,
        pipeline_id: Union[str, None] = None,
        admin_api_url: Union[str, None] = None,
        access_key: Union[str, None] = None,
        pipeline_config_endpoint: Union[str, None] = None,
        refresh_rate: int = CONFIG_REFRESH_RATE) -> Union[dict, list]:
    """ Ask Sermos Admin for the latest configuration for specified pipeline.

    This utilizes redis (required for Sermos-based pipelines/scheduled tasks) to
    cache the result for a predetermined amount of time before requesting an
    update. This is because pipelines/tasks can be invoked rapidly but do not
    change frequently.
    """
    cache_key = PIPELINE_CONFIG_CACHE_KEY.format(pipeline_id)
    deployment_id = get_admin_deployment_id(deployment_id)  # From env if None
    access_key = get_admin_access_key(access_key)  # From env if None

    # Generate pipeline specific endpoint
    admin_api_url = get_admin_api_url(admin_api_url)

    pipeline_config_endpoint = pipeline_config_endpoint\
        if pipeline_config_endpoint is not None else 'pipelines'
    api_url = _generate_api_url(deployment_id, admin_api_url,
                                pipeline_config_endpoint)
    if pipeline_id is not None:
        api_url = urljoin(api_url + '/', pipeline_id)  # Add pipeline ID

    # Retrieve (and cache) result - this will be the exact result from the
    # API response.
    data = retrieve_and_cache_config(cache_key, api_url, access_key,
                                     refresh_rate)
    if data:
        if pipeline_id:
            return data['data']
        return data['data']['results']
    return None
    # TODO do we validate here?


def retrieve_latest_schedule_config(
        deployment_id: Union[str, None] = None,
        admin_api_url: Union[str, None] = None,
        access_key: Union[str, None] = None,
        schedule_config_endpoint: Union[str, None] = None,
        refresh_rate: int = CONFIG_REFRESH_RATE):
    """ Ask Sermos Admin for the latest configuration for scheduled tasks.

    This utilizes redis (required for Sermos-based pipelines/scheduled tasks) to
    cache the result for a predetermined amount of time before requesting an
    update. This is because pipelines/tasks can be invoked rapidly but do not
    change frequently.
    """
    cache_key = SCHEDULE_CONFIG_CACHE_KEY
    deployment_id = get_admin_deployment_id(deployment_id)  # From env if None
    access_key = get_admin_access_key(access_key)  # From env if None

    admin_api_url = get_admin_api_url(admin_api_url)
    schedule_config_endpoint = schedule_config_endpoint\
        if schedule_config_endpoint is not None else 'scheduled_tasks'
    api_url = _generate_api_url(deployment_id, admin_api_url,
                                schedule_config_endpoint)

    data = retrieve_and_cache_config(cache_key, api_url, access_key,
                                     refresh_rate)
    data = {'schedules': data['data']['results']}
    scs = ScheduleConfigSchema()
    return scs.load(data)  # Validate response


def update_schedule_config(new_schedule_config: dict,
                           deployment_id: Union[str, None] = None,
                           admin_api_url: Union[str, None] = None,
                           access_key: Union[str, None] = None,
                           schedule_config_endpoint: Union[str, None] = None):
    """ Tell Sermos to update a deployment's schedule with new version.
    """

    deployment_id = get_admin_deployment_id(deployment_id)  # From env if None
    access_key = get_admin_access_key(access_key)  # From env if None
    admin_api_url = get_admin_api_url(admin_api_url)
    schedule_config_endpoint = schedule_config_endpoint\
        if schedule_config_endpoint is not None else 'scheduled_tasks'
    api_url = _generate_api_url(deployment_id, admin_api_url,
                                schedule_config_endpoint)
    headers = {'apikey': access_key}

    scs = ScheduleConfigSchema()
    for scheduled_task in new_schedule_config['schedules']:
        copy_task = dict(scheduled_task)
        task_id = copy_task.pop('id')
        url = f"{api_url}/{task_id}"
        r = requests.put(url,
                          json=copy_task,
                          headers=headers,
                          verify=True)
        if r.status_code != 200:
            logger.error("Unable to update schedule task in sermos cloud")
            logger.error(r.json())
            return False

    return True
