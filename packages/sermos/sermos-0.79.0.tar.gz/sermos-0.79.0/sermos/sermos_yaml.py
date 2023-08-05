""" Definition of the `sermos.yaml` file. This is only relevant/used for
managed deployments through Sermos.ai. If self-hosting, safely disregard this
yaml format, no `sermos.yaml` is required for your application.

If using, a basic file may look like::

    imageConfig:
        - name: base-image
            installCommand: sermos-demo-client[core]
        - name: public-api-image
            repositoryUrl: myregistry/public-api-image

    environmentVariables:
        - name: GLOBAL_ENV_VAR
            value: globally-available-env-var

    serviceConfig:
        - name: base-worker
          serviceType: celery-worker
          imageName: base-image
          queue: default-queue
          registeredTasks:
              - handler: sermos_demo_client.workers.demo_worker.demo_task

"""
import re
import os
import logging
import pkg_resources
import yaml
from yaml.loader import SafeLoader
from marshmallow import Schema, fields, pre_load, EXCLUDE, INCLUDE,\
    validates_schema
from marshmallow.validate import OneOf
from marshmallow.exceptions import ValidationError
from sermos.utils.module_utils import SermosModuleLoader, normalized_pkg_name
from sermos.constants import DEFAULT_YAML_NAME

logger = logging.getLogger(__name__)


class InvalidPackagePath(Exception):
    pass


class InvalidSermosConfig(Exception):
    pass


class MissingSermosConfig(Exception):
    pass


class InvalidImageConfig(Exception):
    pass


class ExcludeUnknownSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class EnvironmentVariableSchema(ExcludeUnknownSchema):
    """ A single environment variables (singular)
    """
    name = fields.String(required=True,
                         description="Environment variable name.",
                         example="MY_ENV_VAR")
    value = fields.String(required=True,
                          description="Environment variable value.",
                          example="my special value")

    @pre_load
    def replace_null_values(self, item, **kwargs):
        """ Environment variables are often secrets and therefore should not
            be committed to the sermos.yaml file. Instead, they should be
            templated with ${ENV_VAR_NAME} and injected into the file only
            in memory during deployments, etc.

            The Sermos application will use the sermos.yaml file for other
            configuration pieces that do not require the environment variables,
            therefore we add 'unset' as the value to any null values in order
            for the schema to pass the load step as being non-null.
        """
        item["value"] = item["value"]\
            if item.get("value", None) is not None else "unset"
        return item


class EnvironmentVariablesSchema(Schema):
    """ Multiple environment variables (plural)
    """
    environmentVariables = fields.List(
        fields.Nested(EnvironmentVariableSchema, required=True),
        description="List of name/value environment variable pairs available "
        "to the scope of this service.",
        required=False)


class ServiceRequestsSchema(Schema):
    replicaCount = fields.Integer(
        required=False,
        description="Baseline (min) scale of this service to have available.",
        default=1,
        example=1)
    # servicePreference = fields.String(
    #     required=False,
    #     validate=OneOf(['availability', 'cost'])
    #     description="Tell Sermos to optimize for availability or cost.",
    #     example="cost"
    # )
    # scalingMethod = fields.String(
    #     required=False,
    #     validate=OneOf(['manual', 'queue', 'cpu', 'memory'])
    #     description="Method for this worker to scale up/down.",
    #     default="manual",
    #     example="manual"
    # )
    # scalingQueueName = fields.String(
    #     required=False,
    #     description="Queue to watch to scale. Required for `queue` scaling",
    #     default="default",
    #     example="my-special-queue"
    # )
    # scalingMaxReplicaCount = fields.Integer(
    #     required=False,
    #     description="Maximum scale of this service to have available.",
    #     default=1,
    #     example=10
    # )
    # cpuRequest = fields.Float(
    #     required=False,
    #     description="CPUs expected to be available for each replica.",
    #     default=0.5,
    #     example="0.5")
    # memoryRequest = fields.Float(
    #     required=False,
    #     description="Memory (in GB) expected to be available for each replica.",
    #     default=0.5,
    #     example="0.5 (means half of one GB)")
    cpuLimit = fields.Float(
        required=False,
        description="Maximum CPUs to be available for each replica.",
        default=0.5,
        example="0.5")
    memoryLimit = fields.Float(
        required=False,
        description="Maximum memory (in GB) to be available for each replica.",
        default=0.5,
        example="0.5 (means half of 1 GB)")


class NameSchema(Schema):
    """ Validated name string field.
    """
    name = fields.String(required=True,
                         description="Name for service or image. Must include "
                         "only alphanumeric characters along with `_` and `-`.",
                         example="my-service-name")

    @pre_load
    def validate_characters(self, item, **kwargs):
        """ Ensure name field conforms to allowed characters
        """
        valid_chars = r'^[\w\d\-\_]+$'
        if not bool(re.match(valid_chars, item['name'])):
            raise ValueError(
                f"Invalid name: {item['name']}. Only alphanumeric characters "
                "allowed along with `-` and `_`.")
        return item


class SermosImageConfigSchema(NameSchema):
    installCommand = fields.String(
        required=False,
        description="The pip install command to use when Sermos is "
        "responsible for building your image.",
        example="sermos-client-pkg[core,special_feature]")
    sourceSshUrl = fields.String(
        required=False,
        description="The source code ssh url to use when Sermos is "
        "responsible for building your image.",
        example="git@github.com:myorg/sermos-client.git")
    baseImage = fields.String(
        required=False,
        description="The Docker base image to use as the starting point when "
        "Sermos is responsible for building your image",
        example="rhoai/sermos:latest"
    )
    repositoryUrl = fields.String(
        required=False,
        description="The Docker image repository url when using an image "
        "not built by Sermos. Tag is optional, if excluded, `latest` is used.",
        example="rhoai/custom-image ; rhoai/custom-image:v0.0.0")
    repositoryUser = fields.String(
        required=False,
        description="Optional repository username if provided repositoryUrl "
        "is a private registry.",
        example="rhoai")
    repositoryPassword = fields.String(
        required=False,
        description="Optional repository password if provided repositoryUrl "
        "is a private registry. NOTE: Strongly recommended to use environment "
        "variable interpolation in your sermos.yaml file, do not commit "
        "unencrypted secrets to a git repository. "
        "e.g. repositoryPassword: ${DOCKER_REPOSITORY_PASSWORD}",
        example="abc123")


class SermosSharedConfigSchema(Schema):
    """ Attributes shared across internal and external service types
    """
    command = fields.String(
        required=False,
        _required=True,
        description="Command to be run as container CMD.",
        example="gunicorn -b 0.0.0.0:5000 package.app:create_app()")
    port = fields.Integer(
        required=False,
        _required=True,
        description="Port (and targetPort) to direct traffic.",
        example=5000)


class SermosExternalConfigSchema(SermosSharedConfigSchema):
    """ Attributes required for serviceType: external

        Note: Schema lists these are not required in order for this to be used
        as a mixin to SermosServiceConfigSchema. The validation is done
        programmatically based on serviceType.
    """
    serviceId = fields.String(
        required=False,
        _required=True,
        description="The serviceId provided by Sermos. Find in admin console.",
        example="dry-gorge-8018")


class SermosInternalSchema(SermosSharedConfigSchema):
    """ Attributes required for serviceType: internal

        Note: Schema lists these are not required in order for this to be used
        as a mixin to SermosServiceConfigSchema. The validation is done
        programmatically based on serviceType.
    """
    protocol = fields.String(required=False,
                             _required=True,
                             description="Protocol to use.",
                             example="TCP",
                             validate=OneOf(['TCP', 'UDP']))


class SermosRegisteredTaskDetailConfigSchema(Schema):
    handler = fields.String(
        required=True,
        description="Full path to the Method handles work / pipeline tasks.",
        example="sermos_customer_client.workers.worker_group.useful_worker")

    event = fields.Raw(
        required=False,
        unknown=INCLUDE,
        description="Arbitrary user data, passed through `event` arg in task.")


class SermosCeleryWorkerConfigSchema(Schema):
    """ Attributes required for serviceType: celery-worker

        Note: Schema lists these are not required in order for this to be used
        as a mixin to SermosServiceConfigSchema. The validation is done
        programmatically based on serviceType.
    """
    command = fields.String(
        required=False,
        _required=True,
        description="Command to be run as container CMD.",
        example="celery -A mypkg.celery.celery worker --queue my-queue")

    registeredTasks = fields.List(
        fields.Nested(SermosRegisteredTaskDetailConfigSchema, required=True),
        required=False,
        _required=True,
        description="List of task handlers to register for to your Sermos app.")


# Mapping of serviceType keys to their respective schema
service_types = {
    'external': SermosExternalConfigSchema,
    'internal': SermosInternalSchema,
    'celery-worker': SermosCeleryWorkerConfigSchema
}


class SermosServiceConfigSchema(ExcludeUnknownSchema, ServiceRequestsSchema,
                                EnvironmentVariablesSchema,
                                SermosExternalConfigSchema,
                                SermosInternalSchema,
                                SermosCeleryWorkerConfigSchema, NameSchema):
    """ Base service config object definition for workers and internal/external
        services.
    """
    imageName = fields.String(
        required=True,
        description="Specify the name of the base image to use for this "
        "service.",
        example="custom-worker-name")

    serviceType = fields.String(required=True,
                                description="Name of the worker.",
                                example="useful_worker",
                                validate=OneOf(service_types.keys()))


class SermosYamlSchema(ExcludeUnknownSchema, EnvironmentVariablesSchema):
    """ The primary `sermos.yaml` file schema. This defines all available
        properties in a valid Sermos configuration file.
    """

    imageConfig = fields.List(fields.Nested(SermosImageConfigSchema,
                                            required=True),
                              required=True,
                              description="List of available base images. At "
                              "least one image must be defined. The 'name' "
                              "of the image is used in each service defined "
                              "in `serviceConfig`")

    serviceConfig = fields.List(
        fields.Nested(SermosServiceConfigSchema,
                      required=True,
                      description="Core service configuration."),
        description="List of workers for Sermos to manage.",
        required=True)

    def validate_errors(self, schema: Schema, value: dict):
        """ Run Marshmallow validate() and raise if any errors
        """
        schema = schema()
        errors = schema.validate(value)
        if len(errors.keys()) > 0:
            raise ValidationError(errors)

    @validates_schema
    def validate_types(self, data, **kwargs):
        """ Additional validation.

            Nested fields that are not required are not validated by Marshmallow
            by default. Do a single level down of validation for now.

            Each serviceType has attributes that are required but are listed
            as not required in the marshmallow schema. Validate here.

            imageConfig can provide *either* an install command for Sermos
            to use to build the image for customer *or* a Docker repository
            for Sermos to pull.
        """
        # Vaidate nested
        key_schema_pairs = (
            ('imageConfig', SermosImageConfigSchema),
            ('environmentVariables', EnvironmentVariableSchema),
            ('serviceConfig', SermosServiceConfigSchema),
        )
        for k_s in key_schema_pairs:
            val = data.get(k_s[0], None)
            if val is not None:
                if type(val) == list:
                    for v in val:
                        self.validate_errors(k_s[1], v)
                else:
                    self.validate_errors(k_s[1], val)

        # Validate the services. We list every service schema field as not
        # required in order to use them as mixins for a generic service object,
        # however, they ARE required, so validate here using the custom
        # metadata property `_required`. Default to value of `required`.
        service_image_names = []
        for service in data.get('serviceConfig'):
            service_type = service['serviceType']
            schema = service_types[service_type]
            for field in schema().fields:
                try:
                    if schema().fields[field].metadata.get(
                            '_required',
                            getattr(schema().fields[field], 'required')):
                        assert field in service
                except AssertionError:
                    raise ValidationError(
                        f"`{field}` missing in {service_type} definition.")

            service_image_names.append(service['imageName'])

        # Validate imageConfig
        image_names = []
        for image in data.get('imageConfig'):
            image_names.append(image['name'])
            try:
                if image.get('installCommand', None) is not None:
                    assert image.get('repositoryUrl', None) is None
                if image.get('repositoryUrl', None) is not None:
                    assert image.get('installCommand', None) is None
            except AssertionError:
                raise InvalidImageConfig(
                    "Each imageConfig may have *either* an installCommand "
                    "*or* a repositoryUrl but not both. Review "
                    f"image `{image['name']}`")
            
            if image.get('installCommand', None) is not None:
                if image.get('sourceSshUrl') is None:
                    raise InvalidImageConfig(
                        "Each imageConfig must have a sourceSshUrl if "
                        "installCommand is specified")
                if image.get('baseImage') is None:
                    raise InvalidImageConfig(
                        "Each imageConfig must have a baseImage if "
                        "installCommand is specified")


        # Verify each imageName referenced in each service exists in imageConfig
        try:
            assert set(service_image_names).issubset(image_names)
        except AssertionError:
            raise InvalidImageConfig(
                "Mismatched imageName in at least one "
                f"service ({service_image_names}) compared to images available "
                f"in imageConfig ({image_names})")


class YamlPatternConstructor():
    """ Adds a pattern resolver + constructor to PyYaml.

        Typical/deault usage is for parsing environment variables
        in a yaml file but this can be used for any pattern you provide.

        See: https://pyyaml.org/wiki/PyYAMLDocumentation
    """
    def __init__(self,
                 env_var_pattern: str = None,
                 add_constructor: bool = True):
        self.env_var_pattern = env_var_pattern
        if self.env_var_pattern is None:
            # Default pattern is: ${VAR:default}
            self.env_var_pattern = r'^\$\{(.*)\}$'
        self.path_matcher = re.compile(self.env_var_pattern)

        if add_constructor:
            self.add_constructor()

    def _path_constructor(self, loader, node):
        """ Extract the matched value, expand env variable,
            and replace the match

            TODO: Would need to update this (specifically the parsing) if any
            pattern other than our default (or a highly compatible variation)
            is provided.
        """
        # Try to match the correct env variable pattern in this node's value
        # If the value does not match the pattern, return None (which means
        # this node will not be parsed for ENV variables and instead just
        # returned as-is).
        env_var_name = re.match(self.env_var_pattern, node.value)
        try:
            env_var_name = env_var_name.group(1)
        except AttributeError:
            return None

        # If we get down here, then the 'node.value' matches our specified
        # pattern, so try to parse. env_var_name is the value inside ${...}.
        # Split on `:`, which is our delimiter for default values.
        env_var_name_split = env_var_name.split(':')

        # Attempt to retrieve the environment variable...from the environment
        env_var = os.environ.get(env_var_name_split[0], None)

        if env_var is None:  # Nothing found in environment
            # If a default was provided (e.g. VAR:default), return that.
            # We join anything after first element because the default
            # value might be a URL or something with a colon in it
            # which would have 'split' above
            if len(env_var_name_split) > 1:
                return ":".join(env_var_name_split[1:])
            return None  # Return None if not in environ nor default
        return env_var

    def add_constructor(self):
        """ Initialize PyYaml with ability to resolve/load environment
            variables defined in a yaml template when they exist in
            the environment.

            Add to SafeLoader in addition to standard Loader.
        """
        # Add the `!env_var` tag to any scalar (value) that matches the
        # pattern self.path_matcher. This allows the template to be much more
        # intuitive vs needing to add !env_var to the beginning of each value
        yaml.add_implicit_resolver('!env_var', self.path_matcher)
        yaml.add_implicit_resolver('!env_var',
                                   self.path_matcher,
                                   Loader=SafeLoader)

        # Add constructor for the tag `!env_var`, which is a function that
        # converts a node of a YAML representation graph to a native Python
        # object.
        yaml.add_constructor('!env_var', self._path_constructor)
        yaml.add_constructor('!env_var',
                             self._path_constructor,
                             Loader=SafeLoader)


def parse_config_file(sermos_yaml: str):
    """ Parse the `sermos.yaml` file when it's been loaded.

        Arguments:
            sermos_yaml (required): String of loaded sermos.yaml file.
    """
    YamlPatternConstructor()  # Add our env variable parser
    try:
        sermos_yaml_schema = SermosYamlSchema()
        # First suss out yaml issues
        sermos_config = yaml.safe_load(sermos_yaml)
        # Then schema issues
        sermos_config = sermos_yaml_schema.load(sermos_config)
    except ValidationError as e:
        msg = "Invalid Sermos configuration due to {}"\
            .format(e.messages)
        logger.error(msg)
        raise InvalidSermosConfig(msg)
    except InvalidImageConfig as e:
        msg = "Invalid imageConfig configuration due to {}"\
            .format(e)
        logger.error(msg)
        raise InvalidImageConfig(msg)
    except Exception as e:
        msg = "Invalid Sermos configuration, likely due to invalid "\
            "YAML formatting ..."
        logger.exception("{} {}".format(msg, e))
        raise InvalidSermosConfig(msg)
    return sermos_config


def load_sermos_config(pkg_name: str = None,
                       sermos_yaml_filename: str = None,
                       as_dict: bool = True):
    """ Load and parse the `sermos.yaml` file. Issue usable exceptions for
        known error modes so bootstrapping can handle appropriately.

        Arguments:
            pkg_name (required): Directory name for your Python
                package. e.g. my_package_name . If none provided, will check
                environment for `SERMOS_CLIENT_PKG_NAME`. If not found,
                will exit.
            sermos_yaml_filename (optional): Relative path to find your
                `sermos.yaml` configuration file. Defaults to `sermos.yaml`
                which should be found inside your `pkg_name`
            as_dict (optional): If true (default), return the loaded sermos
                configuration as a dictionary. If false, return the loaded
                string value of the yaml file.
    """
    sermos_config = None
    sermos_yaml = None
    if sermos_yaml_filename is None:
        sermos_yaml_filename = DEFAULT_YAML_NAME

    try:
        sermos_config_path = pkg_resources.resource_filename(
            normalized_pkg_name(pkg_name), sermos_yaml_filename)
    except Exception as e:
        msg = "Either pkg_name ({}) or sermos_yaml_filename ({}) is "\
            "invalid ...".format(pkg_name, sermos_yaml_filename)
        logger.error("{} ... {}".format(msg, e))
        raise InvalidPackagePath(e)

    try:
        with open(sermos_config_path, 'r') as f:
            sermos_yaml = f.read()
            sermos_config = parse_config_file(sermos_yaml)
    except InvalidSermosConfig as e:
        raise
    except InvalidImageConfig as e:
        raise
    except FileNotFoundError as e:
        msg = "Sermos config file could not be found at path {} ...".format(
            sermos_config_path)
        raise MissingSermosConfig(msg)
    except Exception as e:
        raise e
    if as_dict:
        return sermos_config
    return yaml.safe_dump(sermos_config)


def load_client_config_and_version(client_pkg_name: str = None,
                                   config_relative_path: str = None):
    """ For this to work, the CLIENT_PKG_NAME needs to be provided (or
        available in the environment) and that package (with exact name) must
        be installed in the same environment as this Sermos package.
    """
    sermos_config = None
    client_version = None

    if client_pkg_name is None:
        client_pkg_name = os.environ.get('CLIENT_PKG_NAME', None)
        if client_pkg_name is None:
            return None, None
        client_pkg_name = normalized_pkg_name(client_pkg_name)

    if config_relative_path is None:
        config_relative_path = os.environ.get('SERMOS_CONFIG_RELATIVE_PATH',
                                              'sermos.yaml')

    logger.info(f"Loading `sermos.yaml` from package `{client_pkg_name}` "
                f"and file location `{config_relative_path}` ...")

    try:
        loader = SermosModuleLoader()
        pkg = loader.get_module(client_pkg_name + '.__init__')
        client_version = getattr(pkg, '__version__', '0.0.0')
        sermos_config = load_sermos_config(client_pkg_name,
                                           config_relative_path)
    except MissingSermosConfig as e:
        logger.error(e)
    except InvalidSermosConfig as e:
        logger.error(e)
    except InvalidPackagePath as e:
        logger.error(e)
    except Exception as e:
        logger.error("Unable to load client's pkg __version__ or "
                     "{} config file for package: {} ... {}".format(
                         config_relative_path, client_pkg_name, e))

    return sermos_config, client_version
