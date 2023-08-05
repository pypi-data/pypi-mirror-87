""" Schemas for Schedule Configuration
"""
import re
from celery.schedules import crontab_parser
from marshmallow.validate import OneOf
from marshmallow.exceptions import ValidationError
from marshmallow import Schema, fields, EXCLUDE, pre_load


class ExcludeUnknownSchema(Schema):
    """ Remove unknown keys from loaded dictionary

    # TODO this seems to be just ignoring and letting through vs excluding...
    """
    class Meta:
        unknown = EXCLUDE


class IntervalScheduleSchema(Schema):
    every = fields.Integer(required=True)
    period = fields.String(requried=True,
                           validate=OneOf([
                               'microseconds', 'seconds', 'minutes', 'hours',
                               'days'
                           ]))


class CrontabScheduleSchema(Schema):
    minute = fields.String(required=True)
    hour = fields.String(required=True)
    day_of_week = fields.String(required=True, data_key='dayOfWeek')
    day_of_month = fields.String(required=True, data_key='dayOfMonth')
    month_of_year = fields.String(required=True, data_key='monthOfYear')

class Schedule(fields.Dict):
    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        if data['scheduleType'] == 'crontab':
            schema = CrontabScheduleSchema()
        else:
            schema = IntervalScheduleSchema()
        return schema.load(value)

class ScheduleEntrySchema(ExcludeUnknownSchema):
    """ Definition of a single schedule entry

    TODO: Add validation based on schedule_type and the relevant optional fields
    TODO: Add validation that each name is unique
    """
    id = fields.String(required=True)

    schedule_type = fields.String(
        required=True,
        validate=OneOf(['interval', 'crontab']),
        description="The Celery schedule type of this entry.",
        example="interval",
        data_key='scheduleType')

    # TODO Figure out where that wonky timestamp format is coming from and
    # update this and in celery_beat.py.
    last_run_at = fields.String(allow_none=True,
                                missing=None,
                                description="Timestamp of last run time.",
                                example="Tue, 18 Aug 2020 01:36:06 GMT",
                                data_key='lastRunAt')
    total_run_count = fields.Integer(allow_none=True,
        missing=0,
        description="Count of number of executions.",
        example=12345,
        data_key='totalRunCount')
    name = fields.String(required=True,
                         description="Name of schedule entry.",
                         example="My Scheduled Task")
    queue = fields.String(required=True,
                          description="Name of queue on which to place task.",
                          example="my-default-queue")
    task = fields.String(required=True,
                         description="Path to task to invoke.",
                         example="my_app.module.method")
    enabled = fields.Boolean(required=True,
                             description="Whether entry is enabled.",
                             example=True)

    exchange = fields.String(
        required=False,
        description="Exchange for the task. Celery default "
        "used if not set, which is recommended.",
        example="tasks")
    routing_key = fields.String(
        required=False,
        description="Routing key for the task. Celery "
        "default used if not set, which is recommended.",
        example="task.default")
    expires = fields.Integer(
        required=False,
        description="Number of seconds after which task "
        "expires if not executed. Default: no expiration.",
        example=60)

    schedule = Schedule(required=True)


    @pre_load
    def validate_string_fields(self, item, **kwargs):
        """ Ensure string fields with no OneOf validation conform to patterns
        """
        if item is None:
            raise ValidationError("NoneType provided, check input.")

        validation_map = {
            'name': r'^[\w\d\-\_\.\s]+$',
            'queue': r'^[\w\d\-\_\.]+$',
            'task': r'^[\w\d\-\_\.]+$',
            'exchange': r'^[\w\d\-\_\.]+$',
            'routing_key': r'^[\w\d\-\_\.]+$'
        }
        for field in validation_map:
            if item.get(field, None) is None:
                continue
            if not bool(re.match(validation_map[field], item[field])):
                raise ValidationError(
                    f"Invalid {field}: `{item[field]}``. Must match pattern: "
                    f"{validation_map[field]}")

        if item['scheduleType'] == 'crontab':
            cron_validation_map = {
                'minute': crontab_parser(60),
                'hour': crontab_parser(24),
                'dayOfWeek': crontab_parser(7),
                'dayOfMonth': crontab_parser(31, 1),
                'monthOfYear': crontab_parser(12, 1)
            }

            for field in cron_validation_map:
                try:
                    cron_validation_map[field].parse(item['schedule'][field])
                except:
                    raise ValidationError(
                        f"Invalid {field}: `{item['schedule'][field]}`. Must "
                        "be valid crontab pattern.")

        return item


class ScheduleConfigSchema(ExcludeUnknownSchema):
    schedules = fields.List(
        fields.Nested(ScheduleEntrySchema, required=True),
        required=True,
        description="A list of individual schedule entries")

    @pre_load
    def validate_fields(self, item, **kwargs):
        """ Ensure fields conform to restrictions
        """
        if item is None:
            raise ValidationError("NoneType provided, check input.")
        known_names = []
        for sched in item.get('schedules', []):
            known_names.append(sched['name'])
        if len(known_names) != len(set(known_names)):
            raise ValidationError("All schedule names must be unique!")
        return item
