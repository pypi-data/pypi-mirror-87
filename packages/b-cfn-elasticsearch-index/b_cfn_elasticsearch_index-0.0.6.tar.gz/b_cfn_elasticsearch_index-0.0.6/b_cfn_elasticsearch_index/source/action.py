import base64
import json
import logging
import os
from typing import Dict, Any, Optional, Tuple
from secrets import token_urlsafe

import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import reindex as elasticsearch_reindex
from requests_aws4auth import AWS4Auth


logger = logging.getLogger(__name__)


class Action:
    def __init__(self, invocation_event: Dict[str, Any]):
        self.__invocation_event: Dict[str, Any] = invocation_event
        self.__parameters: Dict[str, Any] = invocation_event['ResourceProperties']
        self.__old_parameters: Optional[Dict[str, Any]] = invocation_event.get('OldResourceProperties')
        self.__resource_id: Optional[str] = invocation_event.get('PhysicalResourceId')

        try:
            self.REGION = os.environ['AWS_REGION']

            self.INDEX_PREFIX = self.__parameters['IndexPrefix']
            self.ELASTICSEARCH_ENDPOINT = self.__parameters['ElasticsearchEndpoint']
            self.INDEX_SETTINGS = self.__parameters['IndexSettings']
            self.MAPPING_SETTINGS = self.__parameters['MappingSettings']
            self.MIGRATE_DATA = self.__parameters['MigrateData']
        except KeyError as ex:
            logger.error(f'Missing environment: {repr(ex)}.')
            raise
        
        if not isinstance(self.INDEX_SETTINGS, dict):
            logger.error(f'IndexSettings must be a dictionary, got {type(self.INDEX_SETTINGS)}.')
            raise ValueError(f'IndexSettings must be a dictionary, got {type(self.INDEX_SETTINGS)}.')
        
        if not isinstance(self.MAPPING_SETTINGS, dict):
            logger.error(f'MappingSettings must be a dictionary, got {type(self.INDEX_SETTINGS)}.')
            raise ValueError(f'MappingSettings must be a dictionary, got {type(self.INDEX_SETTINGS)}.')

    def create(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Creates a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource creation with these parameters: {json.dumps(self.__parameters)}.')

        index_name, physical_id = self.__create_index(
            self.INDEX_PREFIX,
            self.REGION,
            self.ELASTICSEARCH_ENDPOINT,
            self.INDEX_SETTINGS,
            self.MAPPING_SETTINGS,
        )

        return {"IndexName": index_name}, physical_id


    def update(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Updates a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource update with these parameters: {json.dumps(self.__parameters)}.')

        try:
            # Resource id's are in the format {domain_endpoint}||{index_name}, we split on || to extract the index name.
            index_name = self.__resource_id.split("||")[1]
        except IndexError:
            raise ValueError(f"Invalid PhysicalResourceId given, PhysicalResourceId: {self.__resource_id}.")
        
        old_es_endpoint = self.__old_parameters["ElasticsearchEndpoint"]
        old_index_prefix = self.__old_parameters["IndexPrefix"]

        if self.ELASTICSEARCH_ENDPOINT != old_es_endpoint or self.INDEX_PREFIX != old_index_prefix:
            # We need to create a new index here, we can just reuse the code for normal creation.
            new_index_name, physical_id = self.__create_index(
                self.INDEX_PREFIX,
                self.REGION,
                self.ELASTICSEARCH_ENDPOINT,
                self.INDEX_SETTINGS,
                self.MAPPING_SETTINGS,
            )

            if self.MIGRATE_DATA:
                self.__migrate_index(
                    region=self.REGION,
                    target_elasticsearch_endpoint=self.ELASTICSEARCH_ENDPOINT,
                    source_elasticsearch_endpoint=old_es_endpoint,
                    target_index_name=new_index_name,
                    source_index_name=index_name,
                )
            
            return {"IndexName": new_index_name}, physical_id
        
        else:
            try:
                self.__update_index()
                return {"IndexName": index_name}, self.__resource_id
            except Exception:
                # Some settings cannot be updated on a live index so this requires creating a new index.
                # Detecting if settings that cannot be updated beforehand requires maintaining a list, and
                # Elasticsearch documentation contains no such list, so it's simpler to check if the call failed and fall back.
                new_index_name, physical_id = self.__create_index(
                    self.INDEX_PREFIX,
                    self.REGION,
                    self.ELASTICSEARCH_ENDPOINT,
                    self.INDEX_SETTINGS,
                    self.MAPPING_SETTINGS,
                )

                if self.MIGRATE_DATA:
                    self.__migrate_index(
                        region=self.REGION,
                        target_elasticsearch_endpoint=self.ELASTICSEARCH_ENDPOINT,
                        source_elasticsearch_endpoint=old_es_endpoint,
                        target_index_name=new_index_name,
                        source_index_name=index_name,
                    )
                
                return {"IndexName": new_index_name}, physical_id

    def delete(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Deletes a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource deletion with these parameters: {json.dumps(self.__parameters)}.')

        try:
            # Resource id's are in the format {domain_endpoint}||{index_name}, we split on || to extract the index name.
            index_name = self.__resource_id.split("||")[1]
        except IndexError:
            raise ValueError(f"Invalid PhysicalResourceId given, PhysicalResourceId: {self.__resource_id}")

        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            self.REGION,
            "es",
            session_token=credentials.token,
        )

        es = Elasticsearch(
            hosts=[{"host": self.ELASTICSEARCH_ENDPOINT, "port": 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )

        es.indices.delete(index_name)

        return {"IndexName": index_name}, self.__resource_id

    @staticmethod
    def __create_index(
        index_prefix: str,
        region: str,
        elasticsearch_endpoint: str,
        index_settings: Dict[str, Any],
        mapping_settings: Dict[str, Any],
    ):
        index_name = f"{index_prefix}-{token_urlsafe(8).lower()}"

        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            region,
            "es",
            session_token=credentials.token,
        )

        es = Elasticsearch(
            hosts=[{"host": elasticsearch_endpoint, "port": 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            retry_on_timeout=True,
        )

        try:
            es.indices.create(
                index=index_name,
                body={
                    "settings": index_settings,
                    "mappings": {"properties": mapping_settings},
                },
                # 5 minutes is likely too much for index creation, but large clusters might need it.
                timeout="5m",
            )
        except Exception as e:
            raise Exception(f"Index creation failed:{repr(e)}")

        physical_id = f"{elasticsearch_endpoint}||{index_name}"

        return index_name, physical_id

    @staticmethod
    def __update_index(
        region: str,
        elasticsearch_endpoint: str,
        index_name: str,
        index_settings: Dict[str, Any],
        mapping_settings: Dict[str, Any],
    ):
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            region,
            "es",
            session_token=credentials.token,
        )

        es = Elasticsearch(
            hosts=[{"host": elasticsearch_endpoint, "port": 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )
        try:
            es.indices.put_settings(
                index=index_name,
                body=index_settings,
                # Timeouts subject to tweaking, 5m is a bit on the safe side, but large indices might need more.
                timeout="5m", 
            )

            es.indices.put_mapping(
                index=index_name,
                body={"properties": mapping_settings},
                # Timeouts subject to tweaking, 5m is a bit on the safe side, but large indices might need more.
                timeout="5m",
            )
        except Exception as e:
            logger.warning("Failed to update live index", exc_info=True)
            raise e

    @staticmethod
    def __migrate_index(
        region: str,
        target_elasticsearch_endpoint: str,
        source_elasticsearch_endpoint: str,
        target_index_name: str,
        source_index_name: str,
    ):
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            region,
            "es",
            session_token=credentials.token,
        )

        source_es = Elasticsearch(
            hosts=[{"host": source_elasticsearch_endpoint, "port": 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )

        if source_elasticsearch_endpoint == target_elasticsearch_endpoint:
            try:
                source_es.reindex(
                    {
                        "source": {"index": old_index_name},
                        "dest": {"index": new_index_name},
                    },
                    refresh=True,
                    # 10 minutes should be plenty for medium-sized indexes.
                    timeout="10m",
                )
            except Exception:
                logger.warning("Failed to reindex", exc_info=True)
            
        else:
            target_es = Elasticsearch(
                hosts=[{"host": target_elasticsearch_endpoint, "port": 443}],
                http_auth=awsauth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
            )

            try:
                elasticsearch_reindex(
                    client = source_es,
                    source_index=source_index_name,
                    target_index=target_index_name,
                    target_client=target_es,
                )
            except Exception:
                logger.warning("Failed to reindex across clusters", exc_info=True)

