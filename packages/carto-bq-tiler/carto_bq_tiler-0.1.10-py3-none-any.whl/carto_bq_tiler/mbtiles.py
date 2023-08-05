import base64
import csv
import hashlib
import json
import sqlite3
import tempfile

from pathlib import Path

import click


from .exceptions import CARTOBigQueryTilerException
from .settings import (CARTO_PARTITION_DEFAULT_STEP, CARTO_PARTITION_CURRENT_VERSION, DEFAULT_LAYER, LINE_SEPARATOR,
                       MAX_BIGQUERY_PARTITIONS, MBTILES_CREATE_STATEMENTS, MBTILES_METADATA_SCHEMA,
                       TILESET_LAST_VERSION)
from .tile_utils import flip_tile_row, get_bounding_box_center, get_feature_id_and_geometry_type_from_mvt
from .utils import get_current_timestamp


class MBTilesClient:

    def __init__(self, filepath, create=False):
        mbtiles_path = Path(filepath)
        self.file_name = str(mbtiles_path.name)
        self.file_stem = str(mbtiles_path.stem)

        self._connection = sqlite3.connect(filepath)
        self._metadata = {}

        if create:
            for create_statements in MBTILES_CREATE_STATEMENTS:
                self.query(create_statements)

    def query(self, sql_query):
        return self._connection.execute(sql_query)

    def tileset_to_csv(self):
        csv_file_name = '.{}.csv'.format(hashlib.md5(self.file_stem.encode()).hexdigest())
        csv_file_path = str(Path(tempfile.gettempdir()).joinpath(csv_file_name))

        with open(csv_file_path, 'w') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            for row in self.query('SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles'):
                zoom_level = row[0]
                tile_column = row[1]
                tile_row = flip_tile_row(zoom_level, row[2])
                tile_data = base64.b64encode(row[3]).decode('utf-8')
                carto_partition = -CARTO_PARTITION_CURRENT_VERSION  # Setting a default `carto_partition`

                writer.writerow([zoom_level, tile_column, tile_row, tile_data, carto_partition])

        return csv_file_path

    def get_metadata(self, key=None):
        if key:
            return self._metadata.get(key, None)

        else:
            return self._metadata

    def parse_and_clean_metadata(self):
        created_at = get_current_timestamp()
        metadata_errors = []

        # Getting metadta from MBTiles `metadata` table
        self._metadata = {
            **{row[0]: row[1] for row in self.query('SELECT name, value FROM metadata')},
            **{
                'original_file': self.file_name,
                'created_at': created_at,
                'updated_at': created_at,
                'version': TILESET_LAST_VERSION
            }
        }

        # Validating
        for key, value in MBTILES_METADATA_SCHEMA.items():
            mandatory = value.get('mandatory')
            default = value.get('default')
            values = value.get('values')
            integer = value.get('integer')

            if mandatory and not default and key not in self._metadata:
                metadata_errors.append('Missing {key}.'.format(key=click.style(key, bold=True)))

            elif mandatory and values and self._metadata.get(key) not in values:
                metadata_errors.append('{key} must be one of {values}.'.format(
                    key=click.style(key, bold=True), values=click.style(', '.join(values), bold=True))
                )

            elif default and key not in self._metadata:
                self._metadata[key] = default

            if integer and not isinstance(self._metadata[key], int):
                self._metadata[key] = int(self._metadata[key])

        if metadata_errors:
            self.raise_metadata_errors(metadata_errors)

        # Getting `center`
        if not self._metadata.get('center'):
            center = get_bounding_box_center(self._metadata.get('bounds'))
            self._metadata['center'] = center

        # Getting `carto_partition`
        carto_partition_query = """
            SELECT  q1.min_zoom_level, q1.max_zoom_level,
                    MIN(q0.tile_column), MAX(q0.tile_column),
                    MIN(q0.tile_row), MAX(q0.tile_row)
                FROM (SELECT zoom_level, tile_column, ((1 << zoom_level) - tile_row - 1) AS tile_row FROM tiles) q0,
                    (SELECT MIN(zoom_level) AS min_zoom_level, MAX(zoom_level) AS max_zoom_level FROM tiles) q1
                WHERE q0.zoom_level = q1.max_zoom_level
            """
        result = self.query(carto_partition_query).fetchone()
        self._metadata['carto_partition'] = {
            'version': CARTO_PARTITION_CURRENT_VERSION,
            'partitions': MAX_BIGQUERY_PARTITIONS,
            'zstep': CARTO_PARTITION_DEFAULT_STEP,
            'zmin': result[0],
            'zmax': result[1],
            'xmin': result[2],
            'xmax': result[3],
            'ymin': result[4],
            'ymax': result[5]
        }

        # Getting `vector_layers`, the main layer, its id & `tilestats`
        metadata_json_field = json.loads(self._metadata['json'])
        layers = metadata_json_field.get('vector_layers', [{}])
        layer = layers[0] if layers else {}
        layer_id = layer.get('id', DEFAULT_LAYER)
        tilestats = metadata_json_field.get('tilestats', {})

        # Getting `feature_id` and `geometry_type`
        for row in self.query('SELECT tile_data FROM tiles'):
            feature_id, geometry_type = get_feature_id_and_geometry_type_from_mvt(row[0], layer_id)

            if geometry_type is None:  # Emtpy tile?
                continue

            if feature_id is None:
                metadata_errors.append('Invalid MVTs format, features must contain an {id} field.'.format(
                    id=click.style('id', bold=True)
                ))

            break

        if metadata_errors:
            self.raise_metadata_errors(metadata_errors)

        layer['geometry_type'] = geometry_type
        layers[0] = layer

        # Deleting `json` and saving `layer_id` and `vector_layers`
        del self._metadata['json']
        self._metadata['layer'] = layer_id
        self._metadata['vector_layers'] = layers
        self._metadata['tilestats'] = tilestats

        if metadata_errors:
            self.raise_metadata_errors(metadata_errors)

    def insert_metadata(self, metadata):
        self._connection.executemany('INSERT INTO metadata (name, value) VALUES (?, ?)', metadata.items())
        self._connection.commit()

    def insert_tiles(self, tile_rows):
        self._connection.executemany(
            'INSERT INTO tiles (zoom_level, tile_column, tile_row, tile_data) VALUES (?, ?, ?, ?)', tile_rows
        )
        self._connection.commit()

    def close(self):
        self._connection.close()

    def raise_metadata_errors(self, metadata_errors):
        error_message = 'Error/s found in the {file_name} file metadata:{separator}{errors}'.format(
            file_name=click.style(self.file_name, bold=True), separator=LINE_SEPARATOR,
            errors=LINE_SEPARATOR.join(metadata_errors)
        )
        raise CARTOBigQueryTilerException(error_message)
