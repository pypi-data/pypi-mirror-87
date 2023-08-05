# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carto_bq_tiler', 'carto_bq_tiler.lib', 'carto_bq_tiler.lib.vector_tile_base']

package_data = \
{'': ['*'], 'carto_bq_tiler': ['assets/*']}

install_requires = \
['Shapely==1.7.0',
 'click-spinner==0.1.10',
 'click==7.1.2',
 'google-api-core==1.17.0',
 'google-auth==1.14.2',
 'google-cloud-bigquery-storage[fastavro]==0.8.0',
 'google-cloud-bigquery==1.24.0',
 'google-cloud-core==1.3.0',
 'grpcio==1.28.1',
 'mercantile==1.1.4',
 'pyproj==2.5.0']

entry_points = \
{'console_scripts': ['carto-bq-tiler = carto_bq_tiler.carto_bq_tiler:main']}

setup_kwargs = {
    'name': 'carto-bq-tiler',
    'version': '0.1.10',
    'description': 'CARTO BigQuery Tiler cli',
    'long_description': None,
    'author': 'CARTO',
    'author_email': 'support@carto.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5.3,<4.0.0',
}


setup(**setup_kwargs)
