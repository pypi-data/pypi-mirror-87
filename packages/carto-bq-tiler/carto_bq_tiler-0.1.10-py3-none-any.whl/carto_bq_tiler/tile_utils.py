import zlib

import click

from shapely.geometry import Polygon

from .lib import vector_tile_base
from .exceptions import CARTOBigQueryTilerException
from .settings import ZLIB_MODE


def flip_tile_row(zoom_level, tile_row):
    return (2 ** zoom_level) - tile_row - 1


def get_bounding_box_center(bbox_str):
    bbox = [float(coord) for coord in bbox_str.split(',')]
    bbox = Polygon([[bbox[0], bbox[1]], [bbox[2], bbox[1]], [bbox[2], bbox[3]], [bbox[0], bbox[3]]])  # No SRID :(
    coords = [coord for coord in bbox.centroid.coords][0]
    return '{},{}'.format(*coords)


def get_feature_id_and_geometry_type_from_mvt(compressed_mvt, layer_name):
    try:
        tile_decoded = vector_tile_base.VectorTile(zlib.decompress(compressed_mvt, ZLIB_MODE))

    except zlib.error:
        raise CARTOBigQueryTilerException(
            'MVTs need to be {gzip}-compressed.'.format(gzip=click.style('gzip', bold=True))
        )

    for layer in tile_decoded.layers:
        if layer.name != layer_name:
            continue

        feature = layer.features[0]
        feature_id = feature.id
        geometry_type = feature.type.capitalize().replace('_', '')  # point, line_string, polygon
        break

    return feature_id, geometry_type
