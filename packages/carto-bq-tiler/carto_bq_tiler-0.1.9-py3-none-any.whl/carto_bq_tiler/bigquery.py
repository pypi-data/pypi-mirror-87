import configparser
import json
import re
import os

from pathlib import Path

import click

from google.api_core.exceptions import NotFound
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import bigquery, bigquery_storage_v1 as bigquery_storage
from google.oauth2.credentials import Credentials as UserCredentials
from google.oauth2.service_account import Credentials as ServiceCredentials

from .exceptions import CARTOBigQueryTilerException
from .settings import (BIGQUERYRC_FILE_PATH, CARTO_PARTITION_DEFAULT_MAX, CARTO_PARTITION_DEFAULT_MIN,
                       CARTO_PARTITION_DEFAULT_STEP, MBTILES_TILES_TABLE_FIELDS, MBTILES_TILES_TABLE_Y_INDEX,
                       MBTILES_TILES_TABLE_Z_INDEX, TILESET_LABEL, TILESET_TABLE_SCHEMA, TILESET_LAST_VERSION)
from .utils import datetime_to_timestamp


class BigQueryClient:

    def __init__(self, project_id, credentials_file_path):
        project_file, credentials_file, project_rc, credentials_rc = None, None, None, None

        if credentials_file_path:
            project_file, credentials_file = self._get_credentials_from_file(credentials_file_path)

        if self._exists_bigqueryrc():
            project_rc, credentials_rc = self._get_credentials_from_bigqueryrc()

        project = project_id or project_file or project_rc
        credentials = credentials_file or credentials_rc

        try:
            self._client = bigquery.Client(project=project, credentials=credentials)
            self._storage_client = bigquery_storage.BigQueryReadClient(credentials=credentials)

        except DefaultCredentialsError:
            raise CARTOBigQueryTilerException('Project ID and / or credentials missing from configuration')

    @property
    def project(self):
        return self._client.project

    @property
    def token(self):
        token = self._client._credentials.token
        if token is None:
            self.populate_credentials()
            token = self._client._credentials.token

        return token

    def populate_credentials(self):
        if self._client._credentials.token is None:
            self.query('SELECT 1')

    def query(self, sql_query, job_config=None):
        query_job = self._client.query(sql_query, job_config=job_config)
        return query_job.result()

    def exists_dataset(self, dataset):
        datasets = self._client.list_datasets(include_all=True)
        return any(dataset == dataset_.dataset_id for dataset_ in datasets)

    def create_dataset(self, dataset):
        dataset_id = '{project}.{dataset}'.format(project=self.project, dataset=dataset)
        dataset_ = bigquery.Dataset(dataset_id)
        self._client.create_dataset(dataset_)

    def exists_tileset(self, tileset_name, tileset_last_version=True):
        tileset_name_ = self.validate_tileset_name(tileset_name)
        try:
            table_id = '{project}.{tileset_name}'.format(project=self.project, tileset_name=tileset_name_)
            table = self._client.get_table(table_id)
            table.labels.get(TILESET_LABEL)
            return True

        except NotFound:
            return False

    def upload_tileset_metadata_and_label(self, tileset_name, metadata):
        table_id = '{project}.{tileset_name}'.format(project=self.project, tileset_name=tileset_name)

        query = """
            INSERT INTO `{table_id}`
                    (z, x, y, data, carto_partition)
                VALUES
                    (-1, NULL, NULL, CAST(@metadata AS BYTES), NULL);
            """.format(table_id=table_id)
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('metadata', 'STRING', json.dumps(metadata))
            ]
        )
        self.query(query, job_config)

        table = self._client.get_table(table_id)
        table.labels = {TILESET_LABEL: TILESET_LAST_VERSION}
        table = self._client.update_table(table, ['labels'])

    def get_tileset_metadata(self, tileset_name):
        metadata = None
        table_id = '{project}.{tileset_name}'.format(project=self.project, tileset_name=tileset_name)
        query = """
            SELECT CAST(data AS STRING) AS metadata
                FROM {table_id}
                WHERE carto_partition IS NULL
                    AND z = -1
                LIMIT 1;
            """.format(table_id=table_id)

        result = self.query(query)
        for row in result:
            metadata = row['metadata']

        return json.loads(metadata) if metadata else {}

    def list_tilesets(self, tileset_last_version=True):
        tables = []
        for dataset in self._client.list_datasets(include_all=True):
            for table in self._client.list_tables(dataset.dataset_id):
                if table.labels.get(TILESET_LABEL):
                    tables.append({
                        'tileset_name': '{dataset}.{table}'.format(dataset=table.dataset_id, table=table.table_id),
                        'version': table.labels.get(TILESET_LABEL),
                        'created_at': datetime_to_timestamp(table.created)
                    })

        tables.sort(key=lambda x: x['created_at'], reverse=True)
        return tables

    def exist_tilesets(self, tileset_names, tileset_last_version=True):
        tileset_names_ = [self.validate_tileset_name(tileset_name) for tileset_name in tileset_names]
        bigquery_tileset_names = [
            tileset['tileset_name'] for tileset in self.list_tilesets(tileset_last_version=tileset_last_version)
        ]

        actual_tilesets = [tileset_name for tileset_name in tileset_names_ if tileset_name in bigquery_tileset_names]
        not_tilesets = [tileset_name for tileset_name in tileset_names_ if tileset_name not in bigquery_tileset_names]

        return actual_tilesets, not_tilesets

    def upload_tileset_from_csv(self, csv_file_path, tileset_name, carto_partition):
        dataset = self.validate_tileset_name(tileset_name).split('.')[0]
        if not self.exists_dataset(dataset):
            self.create_dataset(dataset)

        table_id = '{project}.{tileset}'.format(project=self.project, tileset=tileset_name)
        self._create_empty_tileset(table_id, CARTO_PARTITION_DEFAULT_MIN, CARTO_PARTITION_DEFAULT_MAX,
                                   CARTO_PARTITION_DEFAULT_STEP)
        table = self._client.get_table(table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.schema = self._create_table_schema(TILESET_TABLE_SCHEMA)

        with open(csv_file_path, 'rb') as file:
            job = self._client.load_table_from_file(file, table, job_config=job_config)
        job.result()
        Path(csv_file_path).unlink()

        query = """
            UPDATE `{table_id}`
                SET
                    carto_partition = cartobq.tiler.ST_TileToCARTOPartition(z, x, y, '{carto_partition}')
                WHERE TRUE;
            """.format(table_id=table_id, carto_partition=json.dumps(carto_partition))
        self.query(query)

    def drop_tilesets(self, tileset_names):
        try:
            tileset_names_ = [self.validate_tileset_name(tileset_name) for tileset_name in tileset_names]
            queries = [
                'DROP TABLE IF EXISTS`{project}.{tileset}`'.format(
                    project=self.project, tileset=tileset_name_) for tileset_name_ in tileset_names_
            ]
            self.query('; '.join(queries))

        except NotFound:
            return

    def get_tileset_name(self, tileset_name):
        tileset_name_ = self.validate_tileset_name(tileset_name)
        used_tileset_names = [tileset['tileset_name'] for tileset in self.list_tilesets(tileset_last_version=False)]

        if tileset_name_ not in used_tileset_names:  # If it's already a unique name
            return tileset_name_

        suffix = 1
        full_tileset_name = '{tileset}_{suffix}'.format(tileset=tileset_name_, suffix=suffix)
        while full_tileset_name in used_tileset_names:
            suffix += 1
            full_tileset_name = '{tileset}_{suffix}'.format(tileset=tileset_name_, suffix=suffix)

        return full_tileset_name

    def export_tileset_rows(self, tileset_name):
        dataset, table = self.validate_tileset_name(tileset_name).split('.')
        table_ref = 'projects/{project}/datasets/{dataset}/tables/{table}'.format(project=self.project, dataset=dataset,
                                                                                  table=table)
        requested_session = bigquery_storage.types.ReadSession()
        requested_session.table = table_ref
        requested_session.data_format = bigquery_storage.enums.DataFormat.AVRO
        requested_session.read_options.row_restriction = 'carto_partition IS NOT NULL'

        for field in MBTILES_TILES_TABLE_FIELDS:
            requested_session.read_options.selected_fields.append(field)

        parent = 'projects/{project}'.format(project=self.project)
        session = self._storage_client.create_read_session(
            parent,
            requested_session,
            max_stream_count=1  # TODO: Check how to handle more streams
        )
        reader = self._storage_client.read_rows(session.streams[0].name)

        rows = reader.rows(session)
        for row in rows:
            result_row = []
            for i in range(len(MBTILES_TILES_TABLE_FIELDS)):
                result_row.append(row[MBTILES_TILES_TABLE_FIELDS[i]])
            result_row[MBTILES_TILES_TABLE_Y_INDEX] = (
                (2 ** result_row[MBTILES_TILES_TABLE_Z_INDEX]) - result_row[MBTILES_TILES_TABLE_Y_INDEX] - 1
            )
            yield result_row

    def _create_empty_tileset(self, table_id, min_carto_partition, max_carto_partition, step_carto_partition):
        query = """
            CREATE OR REPLACE TABLE `{table_id}`
                (
                    z INT64,
                    x INT64,
                    y INT64,
                    data BYTES,
                    carto_partition INT64
                )
                PARTITION BY RANGE_BUCKET(
                    carto_partition,
                    GENERATE_ARRAY({min_carto_partition}, {max_carto_partition}, {step_carto_partition})
                )
                CLUSTER BY z, x, y;
            """.format(table_id=table_id, min_carto_partition=min_carto_partition,
                       max_carto_partition=max_carto_partition, step_carto_partition=step_carto_partition)
        self.query(query)

    @staticmethod
    def _exists_bigqueryrc():
        return os.path.isfile(str(Path.home().joinpath(BIGQUERYRC_FILE_PATH)))

    @classmethod
    def _get_credentials_from_bigqueryrc(cls):
        config_header = 'default'
        with open(str(Path.home().joinpath(BIGQUERYRC_FILE_PATH)), 'r') as file:
            bigqueryrc_config_string = '[{header}]\n{file}'.format(header=config_header, file=file.read())

        bigqueryrc_config = configparser.ConfigParser()
        bigqueryrc_config.read_string(bigqueryrc_config_string)

        project_id = bigqueryrc_config.get(config_header, 'project_id', fallback=None)
        credentials_file_path = bigqueryrc_config.get(config_header, 'credential_file', fallback=None)

        if not project_id or not credentials_file_path:
            error_message = ('{bq_cli} ({bq_rc}) configuration file looks corrupted, the auhtenticaion process '
                             "can't be completed.").format(bq_cli=click.style('bq command line tool', bold=True),
                                                           bq_rc=click.style('HOME/' + BIGQUERYRC_FILE_PATH, bold=True))
            raise CARTOBigQueryTilerException(error_message)

        credentials_file = cls._get_credentials_json(credentials_file_path)
        is_service_account = credentials_file.get('type') == 'service_account'

        if is_service_account:
            credentials = ServiceCredentials.from_service_account_info(credentials_file)

        else:  # `authorized_user` or `%token%` type
            credentials = UserCredentials.from_authorized_user_info(credentials_file)

        return project_id, credentials

    @classmethod
    def _get_credentials_from_file(cls, credentials_file_path):
        project_id = None
        credentials_file = cls._get_credentials_json(credentials_file_path)

        if credentials_file.get('type') == 'service_account':
            credentials = ServiceCredentials.from_service_account_info(credentials_file)
            project_id = project_id or credentials_file.get('project_id')

        else:  # `authorized_user` type
            credentials = UserCredentials.from_authorized_user_info(credentials_file)

        return project_id, credentials

    @staticmethod
    def _get_credentials_json(credentials_file_path):
        with open(credentials_file_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def _create_table_schema(schema):
        return [
            bigquery.SchemaField(field['name'], field['type'], mode=field['mode']) for field in schema
        ]

    @classmethod
    def validate_tileset_name(cls, identifier):
        identifiers = identifier.split('.')
        if len(identifiers) != 2:
            error_message = ("{tileset} isn't a valid tileset name. It must follow the {pattern} pattern.").format(
                tileset=click.style(identifier, bold=True), pattern=click.style('dataset.table', bold=True))
            raise CARTOBigQueryTilerException(error_message)

        identifiers = [cls._clean_identifier(identifier_) for identifier_ in identifiers]
        return '{dataset}.{table}'.format(dataset=identifiers[0], table=identifiers[1])

    @staticmethod
    def _clean_identifier(identifier):
        identifier_ = re.sub('[^0-9a-zA-Z_\\.]', '', identifier)  # Remove illegal chars
        return re.sub('^[^a-z]+', '', identifier_)  # It starts by lowercase letter
