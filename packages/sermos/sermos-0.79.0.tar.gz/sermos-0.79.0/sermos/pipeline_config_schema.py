""" Schemas for Pipelines

TODO: Add validation that all specified nodes in DAG have corresponding
node in taskDefinitions
"""
import yaml
from marshmallow import Schema, fields, EXCLUDE
from marshmallow.exceptions import ValidationError


class ExcludeUnknownSchema(Schema):
    """ Remove unknown keys from loaded dictionary
    """
    class Meta:
        """ Exclude unknown properties.
        """
        unknown = EXCLUDE


class MetadataSchema(Schema):
    """ Schema for a pipeline's metadata object.
    """
    queue = fields.String(required=True,
                          description="Default queue for all pipeline tasks.",
                          example="default-queue-name")

    maxRetry = fields.Integer(
        required=False,
        description="Max number of retries for a pipeline.",
        default=3,
        example=3)

    maxTtl = fields.Integer(required=False,
                            description="Max TTL for a pipeline in seconds.",
                            default=60,
                            example=60)


class TaskDefinitionsSchema(ExcludeUnknownSchema):
    """ Schema for a single task's configuration
    """
    handler = fields.String(required=True,
                            description="Path to the worker task definition",
                            example="client.workers.my_task")

    maxTtl = fields.Integer(required=False,
                            description="Max TTL for a task in seconds.",
                            default=60,
                            example=60)

    queue = fields.String(required=False,
                          description="Non-default queue for this task.",
                          example="custom-queue-name")
    # payload_args = fields.List(
    #     fields.Dict(keys=fields.String(),
    #                    values=fields.Nested(PayloadArgKwargSchema)))
    # payload_kwargs = fields.List(
    #     fields.Dict(keys=fields.String(),
    #                    values=fields.Nested(PayloadArgKwargSchema)))
    # model_version = fields.String()
    # arbitrary other stuff passed to task?


class PipelineConfigSchema(Schema):
    """ Overall pipeline configuration schema
    """
    metadata = fields.Nested(
        MetadataSchema,
        required=True,
        description="Metadata and configuration information for this pipeline."
    )
    dagAdjacency = fields.Dict(
        keys=fields.String(
            required=True,
            description=
            "Task's node name. *MUST* match key in taskDefinitions dict.",
            example="node_a"),
        values=fields.List(
            fields.String(
                required=True,
                description=
                "Task's node name. *Must* match key in taskDefinitions dict.")
        ),
        required=True,
        description="The DAG Adjacency definition.")
    taskDefinitions = fields.Dict(
        keys=fields.String(
            required=True,
            description=
            "Task's node name. *Must* match related key in dagAdjacency.",
            example="node_a"),
        values=fields.Nested(
            TaskDefinitionsSchema,
            required=True,
            description="Definition of each task in the pipeline.",
            example={
                'handler': 'abc.task',
                'maxRetry': 1
            }),
        required=True,
        description="Configuration for each node defined in DAG.")

class PipelineSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.String(required=True, description="ID for the pipeline.")
    name = fields.String(required=True, description="Pipeline name")
    
    description = fields.String(required=False, missing=None,
                                description="Description of the pipeline.",
                                example="A valuable pipeline.")
    config = fields.Nested(
        PipelineConfigSchema,
        required=True,
        description="Metadata and configuration information for this pipeline."
    )


class PipelineConfigValidator(object):
    """ Validate a pipeline configuration.

        This is stored as a string in the database under `PipelineConfig.config`
        in order to keep it easy for custom features to be added over time.
        This model represents the required / valid features so we can
        programmatically validate when saving, updating, viewing.
    """
    def __init__(self, config_dict: dict = None, config_yaml: str = None):
        super().__init__()

        # We validate this as a dictionary. Turn into dictionary if provided
        # as yaml.
        if config_dict is not None:
            self.config = config_dict
        elif config_yaml is not None:
            self.config = yaml.safe_load(config_yaml)

        self.is_valid = False
        self.validated_config = {}
        self.validation_errors = {}
        try:
            # https://github.com/marshmallow-code/marshmallow/issues/377
            # See issue above when migrating to marshmallow 3
            pcs = PipelineConfigSchema()
            self.validated_config = pcs.load(self.config)
            self.is_valid = True
        except ValidationError as e:
            self.validation_errors = e.messages
            raise e
        except Exception as e:
            raise e
