from __future__ import annotations

from functools import lru_cache

from aws_cdk.aws_lambda import Code, SingletonFunction, Runtime
from aws_cdk.core import Stack, Duration
from aws_cdk.aws_iam import PolicyStatement, PolicyDocument, Role, ServicePrincipal

from b_elasticsearch_layer.layer import Layer as ElasticsearchLayer


class ElasticsearchIndexProviderFunction(SingletonFunction):
    """
    Elasticsearch index resource provider Lambda function.

    Creates index on stack creation.
    Updates index on setting changes.
    Deletes index on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            name: str,
    ) -> None:
        self.__scope = scope
        self.__name = name

        super().__init__(
            scope=scope,
            id=name,
            uuid=f'{name}-uuid',
            function_name=name,
            code=self.__code(),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_8,
            layers=[ElasticsearchLayer(scope, f'{name}ElasticsearchLayer')],
            environment={},
            timeout=Duration.minutes(10),
            role=self.role(),
        )

    def role(self) -> Role:
        inline_policies = {
            "ElasticsearchIndexPrividerFunctionElasticsearchAccessPolicy": PolicyDocument(
                statements=[
                    PolicyStatement(
                        # TODO restrict this to appropriate API calls.
                        actions=["es:*"],
                        resources=["*"],
                    )
                ]
            ),
        }

        return Role(
            scope=self.__scope,
            id=f"{self.__name}ElasticsearchIndexResourceProviderRole",
            assumed_by=ServicePrincipal("lambda.amazonaws.com"),
            description=f"A role for ElasticsearchIndexResourceProvider lambda function.",
            inline_policies=inline_policies,
        )

    @lru_cache
    def __code(self) -> Code:
        from .source import root
        return Code.from_asset(root)

    @property
    def function_name(self):
        return self.__name
