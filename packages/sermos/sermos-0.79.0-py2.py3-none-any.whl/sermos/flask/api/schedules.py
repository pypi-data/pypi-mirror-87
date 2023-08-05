""" API Endpoints for Scheduled Tasks
"""
import os
import logging
from flask import jsonify, request
from flask.views import MethodView
from marshmallow import Schema, fields
from rho_web.smorest import Blueprint
from rho_web.response import abort
from marshmallow.exceptions import ValidationError
from sermos.constants import API_DOC_RESPONSES, API_DOC_PARAMS,\
    API_PATH_V1
from sermos.utils.config_utils import retrieve_latest_schedule_config, \
    update_schedule_config
from sermos.schedule_config_schema import ScheduleConfigSchema
from sermos.flask.decorators import require_apikey

logger = logging.getLogger(__name__)

bp = Blueprint('schedules', __name__, url_prefix=API_PATH_V1 + '/schedules')
SERMOS_DEPLOYMENT_ID = os.environ.get("SERMOS_DEPLOYMENT_ID", "local")


@bp.route('/')
class Schedules(MethodView):
    """ Operations related to schedules
    """
    @require_apikey
    @bp.doc(responses=API_DOC_RESPONSES,
            parameters=[API_DOC_PARAMS['apikey']],
            tags=['Schedules'])
    def get(self):
        """ Retrieve list of available schedule entries.
        """
        api_key = request.headers.get('apikey')
        try:
            schedule_config = retrieve_latest_schedule_config(
                deployment_id=SERMOS_DEPLOYMENT_ID, access_key=api_key)
        except ValidationError:
            abort(400, message="Invalid schedule found ...")

        if schedule_config is None:
            abort(404)

        return jsonify(schedule_config)

    @require_apikey
    @bp.doc(responses=API_DOC_RESPONSES,
            parameters=[API_DOC_PARAMS['apikey']],
            tags=['Schedules'])
    @bp.arguments(ScheduleConfigSchema)
    def post(self, payload: dict):
        """ Update a deployment's schedules. Primarily used to update dynamic
        keys such as last run at and total run count. This does not allow
        overloading schedules, only updating select keys on known schedule
        entries (as in, this is not destructive).
        """
        api_key = request.headers.get('apikey')
        try:
            success = update_schedule_config(
                new_schedule_config=payload,
                deployment_id=SERMOS_DEPLOYMENT_ID,
                access_key=api_key)
        except ValidationError as e:
            abort(400, message=e)

        if not success:
            abort(500)

        return jsonify({'message': 'Schedule update successful ...'})
