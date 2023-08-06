import logging
import uuid
from copy import deepcopy

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

import great_expectations.exceptions as ge_exceptions
from great_expectations.marshmallow__shade import (
    INCLUDE,
    Schema,
    ValidationError,
    fields,
    post_dump,
    post_load,
    validates_schema,
)
from great_expectations.types import DictDot
from great_expectations.types.configurations import ClassConfigSchema

logger = logging.getLogger(__name__)

yaml = YAML()

CURRENT_CONFIG_VERSION = 2
MINIMUM_SUPPORTED_CONFIG_VERSION = 2
DEFAULT_USAGE_STATISTICS_URL = (
    "https://stats.greatexpectations.io/great_expectations/v1/usage_statistics"
)


class AssetConfig(DictDot):
    def __init__(
        self,
        # partitioner_name=None,
        **kwargs,
    ):
        # if partitioner_name is not None:
        #     self._partitioner_name = partitioner_name
        for k, v in kwargs.items():
            setattr(self, k, v)

    # @property
    # def partitioner_name(self):
    #     return self._partitioner_name


class AssetConfigSchema(Schema):
    class Meta:
        unknown = INCLUDE

    # partitioner_name = fields.String(required=False, allow_none=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        pass

    # noinspection PyUnusedLocal
    @post_load
    def make_asset_config(self, data, **kwargs):
        return AssetConfig(**data)


class SorterConfig(DictDot):
    def __init__(
        self, name, class_name=None, module_name=None, orderby="asc", **kwargs,
    ):
        self._name = name
        self._class_name = class_name
        self._module_name = module_name
        self._orderby = orderby
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def name(self):
        return self._name

    @property
    def class_name(self):
        return self._class_name

    @property
    def module_name(self):
        return self._module_name

    @property
    def orderby(self):
        return self._orderby


class SorterConfigSchema(Schema):
    class Meta:
        unknown = INCLUDE

    name = fields.String(required=True)
    class_name = fields.String(required=True)
    module_name = fields.String(
        missing="great_expectations.datasource.data_connector.partitioner.sorter"
    )
    orderby = fields.String(required=False, missing="asc", allow_none=False)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        pass

    # noinspection PyUnusedLocal
    @post_load
    def make_sorter_config(self, data, **kwargs):
        return SorterConfig(**data)


class PartitionerConfig(DictDot):
    def __init__(
        self,
        class_name,
        module_name=None,
        sorters=None,
        allow_multipart_partitions=False,
        runtime_keys=None,
        **kwargs,
    ):
        self._class_name = class_name
        self._module_name = module_name
        if sorters is not None:
            self._sorters = sorters
        self._allow_multipart_partitions = allow_multipart_partitions
        if runtime_keys is not None:
            self._runtime_keys = runtime_keys
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def class_name(self):
        return self._class_name

    @property
    def module_name(self):
        return self._module_name

    @property
    def sorters(self):
        return self._sorters

    @property
    def allow_multipart_partitions(self):
        return self._allow_multipart_partitions

    @property
    def runtime_keys(self):
        return self._runtime_keys


class PartitionerConfigSchema(Schema):
    class Meta:
        unknown = INCLUDE

    class_name = fields.String(required=True)
    module_name = fields.String(
        missing="great_expectations.datasource.data_connector.partitioner"
    )

    sorters = fields.List(
        cls_or_instance=fields.Nested(SorterConfigSchema),
        required=False,
        allow_none=True,
    )

    allow_multipart_partitions = fields.Boolean(
        required=False, missing=False, allow_none=False
    )

    runtime_keys = fields.List(
        cls_or_instance=fields.String(), required=False, allow_none=True
    )

    @validates_schema
    def validate_schema(self, data, **kwargs):
        pass

    # noinspection PyUnusedLocal
    @post_load
    def make_partitioner_config(self, data, **kwargs):
        return PartitionerConfig(**data)


# TODO: <Alex></Alex>
class DataConnectorConfig(DictDot):
    def __init__(
        self,
        class_name,
        module_name=None,
        # partitioners=None,
        # default_partitioner_name=None,
        assets=None,
        **kwargs,
    ):
        self._class_name = class_name
        self._module_name = module_name
        # if partitioners is not None:
        #     self._partitioners = partitioners
        # if default_partitioner_name is not None:
        #     self._default_partitioner_name = default_partitioner_name
        if assets is not None:
            self._assets = assets
        for k, v in kwargs.items():
            setattr(self, k, v)

    # @property
    # def partitioners(self):
    #     return self._partitioners

    # @property
    # def default_partitioner_name(self):
    #     return self._default_partitioner_name

    @property
    def assets(self):
        return self._assets

    @property
    def class_name(self):
        return self._class_name

    @property
    def module_name(self):
        return self._module_name


class DataConnectorConfigSchema(Schema):
    class Meta:
        unknown = INCLUDE

    class_name = fields.String(required=True)
    module_name = fields.String(missing="great_expectations.datasource.data_connector")

    assets = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(AssetConfigSchema),
        required=False,
        allow_none=True,
    )

    # TODO: <Alex></Alex>
    # partitioners = fields.Dict(
    #     keys=fields.Str(),
    #     values=fields.Nested(PartitionerConfigSchema),
    #     required=False,
    #     allow_none=True,
    # )

    # default_partitioner_name = fields.String(
    #     required=False,
    #     allow_none=True,
    # )

    @validates_schema
    def validate_schema(self, data, **kwargs):
        pass

    # noinspection PyUnusedLocal
    @post_load
    def make_data_connector_config(self, data, **kwargs):
        return DataConnectorConfig(**data)


class ExecutionEngineConfig(DictDot):
    def __init__(
        self,
        class_name,
        module_name=None,
        caching=None,
        batch_spec_defaults=None,
        **kwargs,
    ):
        self._class_name = class_name
        self._module_name = module_name
        if caching is not None:
            self.caching = caching
        if batch_spec_defaults is not None:
            self._batch_spec_defaults = batch_spec_defaults
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def module_name(self):
        return self._module_name

    @property
    def class_name(self):
        return self._class_name

    @property
    def batch_spec_defaults(self):
        return self._batch_spec_defaults


class ExecutionEngineConfigSchema(Schema):
    class Meta:
        unknown = INCLUDE

    class_name = fields.String(required=True)
    module_name = fields.String(missing="great_expectations.execution_engine")
    caching = fields.Boolean()
    batch_spec_defaults = fields.Dict(allow_none=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        pass

    # noinspection PyUnusedLocal
    @post_load
    def make_execution_engine_config(self, data, **kwargs):
        return ExecutionEngineConfig(**data)


class DatasourceConfig(DictDot):
    def __init__(
        self,
        class_name=None,
        module_name=None,
        execution_engine=None,
        data_connectors=None,
        credentials=None,
        reader_method=None,
        limit=None,
        **kwargs,
    ):
        # NOTE - JPC - 20200316: Currently, we are mostly inconsistent with respect to this type...
        self._class_name = class_name
        self._module_name = module_name
        self.execution_engine = execution_engine
        if data_connectors is None:
            data_connectors = {}
        self.data_connectors = data_connectors
        if credentials is not None:
            self.credentials = credentials
        if reader_method is not None:
            self.reader_method = reader_method
        if limit is not None:
            self.limit = limit
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def class_name(self):
        return self._class_name

    @property
    def module_name(self):
        return self._module_name


class DatasourceConfigSchema(Schema):
    class Meta:
        unknown = INCLUDE

    class_name = fields.String(missing="Datasource")
    module_name = fields.String(missing="great_expectations.datasource")
    execution_engine = fields.Nested(ExecutionEngineConfigSchema)

    data_connectors = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(DataConnectorConfigSchema),
        required=True,
        allow_none=False,
    )

    credentials = fields.Raw(allow_none=True)
    spark_context = fields.Raw(allow_none=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        pass

    # noinspection PyUnusedLocal
    @post_load
    def make_datasource_config(self, data, **kwargs):
        return DatasourceConfig(**data)


class LegacyDatasourceConfig(DictDot):
    def __init__(
        self,
        class_name,
        module_name=None,
        data_asset_type=None,
        batch_kwargs_generators=None,
        credentials=None,
        boto3_options=None,
        reader_method=None,
        limit=None,
        **kwargs,
    ):
        # NOTE - JPC - 20200316: Currently, we are mostly inconsistent with respect to this type...
        self._class_name = class_name
        self._module_name = module_name
        self.data_asset_type = data_asset_type
        if batch_kwargs_generators is not None:
            self.batch_kwargs_generators = batch_kwargs_generators
        if credentials is not None:
            self.credentials = credentials
        if reader_method is not None:
            self.reader_method = reader_method
        if limit is not None:
            self.limit = limit
        for k, v in kwargs.items():
            setattr(self, k, v)
        if boto3_options is not None:
            self.boto3_options = boto3_options

    @property
    def class_name(self):
        return self._class_name

    @property
    def module_name(self):
        return self._module_name


class AnonymizedUsageStatisticsConfig(DictDot):
    def __init__(self, enabled=True, data_context_id=None, usage_statistics_url=None):
        self._enabled = enabled
        if data_context_id is None:
            data_context_id = str(uuid.uuid4())
            self._explicit_id = False
        else:
            self._explicit_id = True

        self._data_context_id = data_context_id
        if usage_statistics_url is None:
            usage_statistics_url = DEFAULT_USAGE_STATISTICS_URL
            self._explicit_url = False
        else:
            self._explicit_url = True
        self._usage_statistics_url = usage_statistics_url

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        if not isinstance(enabled, bool):
            raise ValueError("usage statistics enabled property must be boolean")
        self._enabled = enabled

    @property
    def data_context_id(self):
        return self._data_context_id

    @data_context_id.setter
    def data_context_id(self, data_context_id):
        try:
            uuid.UUID(data_context_id)
        except ValueError:
            raise ge_exceptions.InvalidConfigError(
                "data_context_id must be a valid uuid"
            )
        self._data_context_id = data_context_id
        self._explicit_id = True

    @property
    def explicit_id(self):
        return self._explicit_id

    @property
    def usage_statistics_url(self):
        return self._usage_statistics_url

    @usage_statistics_url.setter
    def usage_statistics_url(self, usage_statistics_url):
        self._usage_statistics_url = usage_statistics_url
        self._explicit_url = True


class AnonymizedUsageStatisticsConfigSchema(Schema):
    data_context_id = fields.UUID()
    enabled = fields.Boolean(default=True)
    usage_statistics_url = fields.URL(allow_none=True)
    _explicit_url = fields.Boolean(required=False)

    # noinspection PyUnusedLocal
    @post_load()
    def make_usage_statistics_config(self, data, **kwargs):
        if "data_context_id" in data:
            data["data_context_id"] = str(data["data_context_id"])
        return AnonymizedUsageStatisticsConfig(**data)

    # noinspection PyUnusedLocal
    @post_dump()
    def filter_implicit(self, data, **kwargs):
        if not data.get("_explicit_url") and "usage_statistics_url" in data:
            del data["usage_statistics_url"]
        if "_explicit_url" in data:
            del data["_explicit_url"]
        return data


class LegacyDatasourceConfigSchema(Schema):
    class Meta:
        unknown = INCLUDE

    class_name = fields.String(required=True)
    module_name = fields.String(missing="great_expectations.datasource")
    data_asset_type = fields.Nested(ClassConfigSchema)
    boto3_options = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True)
    # TODO: Update to generator-specific
    # batch_kwargs_generators = fields.Mapping(keys=fields.Str(), values=fields.Nested(fields.GeneratorSchema))
    batch_kwargs_generators = fields.Dict(
        keys=fields.Str(), values=fields.Dict(), allow_none=True
    )
    credentials = fields.Raw(allow_none=True)
    spark_context = fields.Raw(allow_none=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if "generators" in data:
            raise ge_exceptions.InvalidConfigError(
                "Your current configuration uses the 'generators' key in a datasource, but in version 0.10 of "
                "GE, that key is renamed to 'batch_kwargs_generators'. Please update your config to continue."
            )

    # noinspection PyUnusedLocal
    @post_load
    def make_datasource_config(self, data, **kwargs):
        return LegacyDatasourceConfig(**data)


class NotebookTemplateConfig(DictDot):
    def __init__(self, file_name, template_kwargs=None):
        self.file_name = file_name
        if template_kwargs:
            self.template_kwargs = template_kwargs
        else:
            self.template_kwargs = {}


class NotebookTemplateConfigSchema(Schema):
    file_name = fields.String()
    template_kwargs = fields.Dict(
        keys=fields.Str(), values=fields.Str(), allow_none=True
    )

    # noinspection PyUnusedLocal
    @post_load
    def make_notebook_template_config(self, data, **kwargs):
        return NotebookTemplateConfig(**data)


class NotebookConfig(DictDot):
    def __init__(
        self,
        class_name,
        module_name,
        custom_templates_module,
        header_markdown=None,
        footer_markdown=None,
        table_expectations_header_markdown=None,
        column_expectations_header_markdown=None,
        table_expectations_not_found_markdown=None,
        column_expectations_not_found_markdown=None,
        authoring_intro_markdown=None,
        column_expectations_markdown=None,
        header_code=None,
        footer_code=None,
        column_expectation_code=None,
        table_expectation_code=None,
    ):
        self.class_name = class_name
        self.module_name = module_name
        self.custom_templates_module = custom_templates_module

        self.header_markdown = header_markdown
        self.footer_markdown = footer_markdown
        self.table_expectations_header_markdown = table_expectations_header_markdown
        self.column_expectations_header_markdown = column_expectations_header_markdown
        self.table_expectations_not_found_markdown = (
            table_expectations_not_found_markdown
        )
        self.column_expectations_not_found_markdown = (
            column_expectations_not_found_markdown
        )
        self.authoring_intro_markdown = authoring_intro_markdown
        self.column_expectations_markdown = column_expectations_markdown

        self.header_code = header_code
        self.footer_code = footer_code
        self.column_expectation_code = column_expectation_code
        self.table_expectation_code = table_expectation_code


class NotebookConfigSchema(Schema):
    class_name = fields.String(missing="SuiteEditNotebookRenderer")
    module_name = fields.String(
        missing="great_expectations.render.renderer.suite_edit_notebook_renderer"
    )
    custom_templates_module = fields.String()

    header_markdown = fields.Nested(NotebookTemplateConfigSchema, allow_none=True)
    footer_markdown = fields.Nested(NotebookTemplateConfigSchema, allow_none=True)
    table_expectations_header_markdown = fields.Nested(
        NotebookTemplateConfigSchema, allow_none=True
    )
    column_expectations_header_markdown = fields.Nested(
        NotebookTemplateConfigSchema, allow_none=True
    )
    table_expectations_not_found_markdown = fields.Nested(
        NotebookTemplateConfigSchema, allow_none=True
    )
    column_expectations_not_found_markdown = fields.Nested(
        NotebookTemplateConfigSchema, allow_none=True
    )
    authoring_intro_markdown = fields.Nested(
        NotebookTemplateConfigSchema, allow_none=True
    )
    column_expectations_markdown = fields.Nested(
        NotebookTemplateConfigSchema, allow_none=True
    )

    header_code = fields.Nested(NotebookTemplateConfigSchema, allow_none=True)
    footer_code = fields.Nested(NotebookTemplateConfigSchema, allow_none=True)
    column_expectation_code = fields.Nested(
        NotebookTemplateConfigSchema, allow_none=True
    )
    table_expectation_code = fields.Nested(
        NotebookTemplateConfigSchema, allow_none=True
    )

    # noinspection PyUnusedLocal
    @post_load
    def make_notebook_config(self, data, **kwargs):
        return NotebookConfig(**data)


class NotebooksConfig(DictDot):
    def __init__(self, suite_edit):
        self.suite_edit = suite_edit


class NotebooksConfigSchema(Schema):
    # for now only suite_edit, could have other customization options for
    # notebooks in the future
    suite_edit = fields.Nested(NotebookConfigSchema)

    # noinspection PyUnusedLocal
    @post_load
    def make_notebooks_config(self, data, **kwargs):
        return NotebooksConfig(**data)


class DataContextConfig(DictDot):
    def __init__(
        self,
        config_version,
        expectations_store_name,
        validations_store_name,
        evaluation_parameter_store_name,
        plugins_directory,
        validation_operators,
        stores,
        data_docs_sites,
        notebooks=None,
        config_variables_file_path=None,
        anonymous_usage_statistics=None,
        commented_map=None,
        datasources=None,
    ):
        if commented_map is None:
            commented_map = CommentedMap()
        self._commented_map = commented_map
        self._config_version = config_version
        if datasources is None:
            datasources = {}
        self.datasources = datasources
        self.expectations_store_name = expectations_store_name
        self.validations_store_name = validations_store_name
        self.evaluation_parameter_store_name = evaluation_parameter_store_name
        self.plugins_directory = plugins_directory
        if not isinstance(validation_operators, dict):
            raise ValueError(
                "validation_operators must be configured with a dictionary"
            )
        self.validation_operators = validation_operators
        self.stores = stores
        self.notebooks = notebooks
        self.data_docs_sites = data_docs_sites
        self.config_variables_file_path = config_variables_file_path
        if anonymous_usage_statistics is None:
            anonymous_usage_statistics = AnonymizedUsageStatisticsConfig()
        elif isinstance(anonymous_usage_statistics, dict):
            anonymous_usage_statistics = AnonymizedUsageStatisticsConfig(
                **anonymous_usage_statistics
            )
        self.anonymous_usage_statistics = anonymous_usage_statistics

    @property
    def commented_map(self):
        return self._commented_map

    @property
    def config_version(self):
        return self._config_version

    @classmethod
    def from_commented_map(cls, commented_map):
        try:
            config = dataContextConfigSchema.load(commented_map)
            return cls(commented_map=commented_map, **config)
        except ValidationError:
            logger.error(
                "Encountered errors during loading data context config. See ValidationError for more details."
            )
            raise

    def to_yaml(self, outfile):
        commented_map = deepcopy(self.commented_map)
        commented_map.update(dataContextConfigSchema.dump(self))
        yaml.dump(commented_map, outfile)


class DataContextConfigSchema(Schema):
    config_version = fields.Number(
        validate=lambda x: 0 < x < 100,
        error_messages={"invalid": "config version must " "be a number."},
    )
    # TODO: <Alex>Proper Schema enforcement for the new Datasource must be implemented.</Alex>
    datasources = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(LegacyDatasourceConfigSchema),
        allow_none=True,
    )
    expectations_store_name = fields.Str()
    validations_store_name = fields.Str()
    evaluation_parameter_store_name = fields.Str()
    plugins_directory = fields.Str(allow_none=True)
    validation_operators = fields.Dict(keys=fields.Str(), values=fields.Dict())
    stores = fields.Dict(keys=fields.Str(), values=fields.Dict())
    notebooks = fields.Nested(NotebooksConfigSchema, allow_none=True)
    data_docs_sites = fields.Dict(
        keys=fields.Str(), values=fields.Dict(), allow_none=True
    )
    config_variables_file_path = fields.Str(allow_none=True)
    anonymous_usage_statistics = fields.Nested(AnonymizedUsageStatisticsConfigSchema)

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def handle_error(self, exc, data, **kwargs):
        """Log and raise our custom exception when (de)serialization fails."""
        logger.error(exc.messages)
        raise ge_exceptions.InvalidDataContextConfigError(
            "Error while processing DataContextConfig.", exc
        )

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if "config_version" not in data:
            raise ge_exceptions.InvalidDataContextConfigError(
                "The key `config_version` is missing; please check your config file.",
                validation_error=ValidationError("no config_version key"),
            )

        if not isinstance(data["config_version"], (int, float)):
            raise ge_exceptions.InvalidDataContextConfigError(
                "The key `config_version` must be a number. Please check your config file.",
                validation_error=ValidationError("config version not a number"),
            )

        # When migrating from 0.7.x to 0.8.0
        if data["config_version"] == 0 and (
            "validations_store" in list(data.keys())
            or "validations_stores" in list(data.keys())
        ):
            raise ge_exceptions.UnsupportedConfigVersionError(
                "You appear to be using a config version from the 0.7.x series. This version is no longer supported."
            )
        elif data["config_version"] < MINIMUM_SUPPORTED_CONFIG_VERSION:
            raise ge_exceptions.UnsupportedConfigVersionError(
                "You appear to have an invalid config version ({}).\n    The version number must be at least {}. "
                "Please see the migration guide at https://docs.greatexpectations.io/en/latest/guides/how_to_guides/migrating_versions.html".format(
                    data["config_version"], MINIMUM_SUPPORTED_CONFIG_VERSION
                ),
            )
        elif data["config_version"] > CURRENT_CONFIG_VERSION:
            raise ge_exceptions.InvalidDataContextConfigError(
                "You appear to have an invalid config version ({}).\n    The maximum valid version is {}.".format(
                    data["config_version"], CURRENT_CONFIG_VERSION
                ),
                validation_error=ValidationError("config version too high"),
            )


dataContextConfigSchema = DataContextConfigSchema()
legacyDatasourceConfigSchema = LegacyDatasourceConfigSchema()
datasourceConfigSchema = DatasourceConfigSchema()
dataConnectorConfigSchema = DataConnectorConfigSchema()
assetConfigSchema = AssetConfigSchema()
partitionerConfigSchema = PartitionerConfigSchema()
sorterConfigSchema = SorterConfigSchema()
anonymizedUsageStatisticsSchema = AnonymizedUsageStatisticsConfigSchema()
notebookConfigSchema = NotebookConfigSchema()
