from aws_cdk.core import Stack, CustomResource, RemovalPolicy
from aws_cdk.aws_elasticsearch import Domain

from b_cfn_elasticsearch_index.function import ElasticsearchIndexProviderFunction


class ElasticsearchIndexResource(CustomResource):
    """
    Custom resource used for managing an Elasticsearch index.

    Creates an index on stack creation.
    Updates the index on settings change.
    Deletes the index on stack deletion.
    """

    def __init__(
        self,
        scope: Stack,
        name: str,
        elasticsearch_domain: Domain,
        index_prefix: str,
        index_settings: dict = {},
        mapping_settings: dict = {},
        migrate_data: bool = False,
    ) -> None:

        self.elasticsearch_domain = elasticsearch_domain

        function = ElasticsearchIndexProviderFunction(
            scope=scope,
            name = f"{name}ProviderFunction",
        )

        super().__init__(
            scope=scope,
            id=f"{name}ElasticsearchIndex",
            service_token=function.function_arn,
            removal_policy=RemovalPolicy.DESTROY,
            resource_type="Custom::ElasticsearchIndex",
            properties={
                "ElasticsearchEndpoint": elasticsearch_domain.domain_endpoint,
                "IndexPrefix": index_prefix,
                "IndexSettings": index_settings,
                "MappingSettings": mapping_settings,
                "MigrateData": migrate_data,
            },
        )

    @property
    def index_name(self):
        return self.get_att_string("IndexName")