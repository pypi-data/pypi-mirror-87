import json

from pathlib import Path

from .mbtiles import MBTilesClient
from .settings import DEFAULT_GEOMETRY_TYPE, GEOJSON_TYPE_CONVERSION, MBTILES_METADATA_SCHEMA


def export_to_mbtiles(bq_client, tileset_name, mbtiles_file_path):
    mb_client = MBTilesClient(mbtiles_file_path, create=True)

    tileset_metadata = bq_client.get_tileset_metadata(tileset_name)
    tileset_metadata['json'] = json.dumps({  # The `vector_layers`, `tilestat` & `json` exceptions
        'vector_layers': tileset_metadata.get('vector_layers'),
        'tilestats': tileset_metadata.get('tilestats')
    })
    tileset_metadata = {key: str(value) for key, value in tileset_metadata.items() if key in MBTILES_METADATA_SCHEMA}
    tileset_metadata.update(
        {
            key: value['values'][0] for key, value in MBTILES_METADATA_SCHEMA.items()
            if 'values' in value and key not in tileset_metadata
        }
    )
    mb_client.insert_metadata(tileset_metadata)

    tile_rows = bq_client.export_tileset_rows(tileset_name)
    mb_client.insert_tiles(tile_rows)

    mb_client.close()


def export_to_files(bq_client, tileset_name, viewer_directory_path):
    # Metadata
    tileset_metadata = bq_client.get_tileset_metadata(tileset_name)
    layer_name = tileset_metadata.get('layer')
    center = tileset_metadata.get('center')
    layers = tileset_metadata.get('vector_layers', [{}])
    layer = layers[0] if layers else {}
    minzoom = int(layer.get('minzoom'))
    maxzoom = int(layer.get('maxzoom'))
    zoom = int((minzoom + maxzoom) / 2)
    geometry_type = layer.get('geometry_type', DEFAULT_GEOMETRY_TYPE)
    geometry_type = GEOJSON_TYPE_CONVERSION.get(geometry_type.lower()) if geometry_type else DEFAULT_GEOMETRY_TYPE

    # Tiles
    rows = bq_client.export_tileset_rows(tileset_name)
    for row in rows:
        zoom_level, tile_column, tile_row, tile_data = row[0], row[1], row[2], row[3]

        tile_directory_path = Path(viewer_directory_path).joinpath(str(zoom_level), str(tile_column))
        tile_directory_path.mkdir(parents=True, exist_ok=True)
        tile_file_path = str(tile_directory_path.joinpath('{tile_row}.pbf'.format(tile_row=tile_row)))
        with open(tile_file_path, 'wb') as file:
            file.write(tile_data)

    # Metadata
    metadata = {
        'tileset_name': tileset_name,
        'center': center,
        'minzoom': minzoom,
        'maxzoom': maxzoom,
        'zoom': zoom,
        'layer_name': layer_name,
        'geometry_type': geometry_type
    }

    metadata_file_path = str(Path(viewer_directory_path).joinpath('metadata.json'))
    with open(metadata_file_path, 'w') as file:
        json.dump(metadata, file)
