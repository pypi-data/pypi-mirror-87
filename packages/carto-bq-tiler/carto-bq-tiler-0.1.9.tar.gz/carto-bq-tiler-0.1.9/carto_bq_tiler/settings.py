import configparser

from pathlib import Path


toml_file_path = Path(__file__).parent.parent.joinpath('pyproject.toml')
toml_config = configparser.ConfigParser()
toml_config.read(str(toml_file_path))

NAME = toml_config.get('tool.poetry', 'name', fallback='carto-bq-tiler').replace('"', '')
VERSION = toml_config.get('tool.poetry', 'version', fallback='0.1.0').replace('"', '')
AUTHORS = toml_config.get('tool.poetry', 'authors', fallback='["CARTO <support@carto.com>"]').strip('[]').replace('"',
                                                                                                                  '')
VIEWER_PORT = 8000

HELP_CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help']
}

TILESET_LABEL = 'carto_tileset'
CARTO_PARTITION_CURRENT_VERSION = 1
TILESET_LAST_VERSION = 6

MAX_BIGQUERY_PARTITIONS = 4000

CARTO_PARTITION_DEFAULT_STEP = 1
CARTO_PARTITION_DEFAULT_MIN = CARTO_PARTITION_DEFAULT_STEP
CARTO_PARTITION_DEFAULT_MAX = MAX_BIGQUERY_PARTITIONS

LAYER_TYPE = 'overlay'
LINE_SEPARATOR = '\n\t- '
BIGQUERYRC_FILE_PATH = '.bigqueryrc'
ZLIB_MODE = 15 + 32

TILE_SIZE = 512
TILE_EXTENT = 4096
TILE_FORMAT = 'pbf'
TILE_COMPRESSION_FORMAT = 'gzip'

DEFAULT_LAYER = 'default'

DEFAULT_GEOMETRY_TYPE = 'Polygon'
GEOJSON_TYPE_CONVERSION = {
    'point': 'point',
    'linestring': 'linestring',
    'polygon': 'polygon',
    'multipoint': 'point',
    'multilinestring': 'linestring',
    'multipolygon': 'polygon'
}

TILESET_TABLE_SCHEMA = [
    {
        'name': 'z',
        'type': 'INT64',
        'mode': 'REQUIRED'
    },
    {
        'name': 'x',
        'type': 'INT64',
        'mode': 'REQUIRED'
    },
    {
        'name': 'y',
        'type': 'INT64',
        'mode': 'REQUIRED'
    },
    {
        'name': 'data',
        'type': 'BYTES',
        'mode': 'NULLABLE'
    },
    {
        'name': 'carto_partition',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }
]

MBTILES_METADATA_SCHEMA = {
    # Basic
    'name': {
        'mandatory': True
    },
    'format': {
        'mandatory': True,
        'values': [TILE_FORMAT]
    },
    'json': {
        'mandatory': True
    },

    # Spatial
    'center': {},
    'bounds': {
        'mandatory': True
    },
    'minzoom': {
        'mandatory': True,
        'integer': True
    },
    'maxzoom': {
        'mandatory': True,
        'integer': True
    },

    # Tiles
    'tile_size': {
        'default': TILE_SIZE,
        'integer': True
    },
    'tile_extent': {
        'default': TILE_EXTENT,
        'integer': True
    },
    'compression': {
        'default': TILE_COMPRESSION_FORMAT
    },

    # Extra
    'type': {
        'default': LAYER_TYPE
    },

    # Geneartor
    'generator': {
        'default': NAME
    },
    'generator_options': {}
}

MBTILES_CREATE_STATEMENTS = [
    'CREATE TABLE metadata (name text, value text)',
    'CREATE TABLE tiles (zoom_level integer, tile_column integer, tile_row integer, tile_data blob)',
    'CREATE UNIQUE INDEX name on metadata (name)',
    'CREATE UNIQUE INDEX tile_index on tiles (zoom_level, tile_column, tile_row)',
]
MBTILES_TILES_TABLE_FIELDS = ['z', 'x', 'y', 'data']
MBTILES_TILES_TABLE_Z_INDEX = MBTILES_TILES_TABLE_FIELDS.index('z')
MBTILES_TILES_TABLE_Y_INDEX = MBTILES_TILES_TABLE_FIELDS.index('y')
