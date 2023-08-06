# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wetterdienst',
 'wetterdienst.core',
 'wetterdienst.dwd',
 'wetterdienst.dwd.forecasts',
 'wetterdienst.dwd.forecasts.metadata',
 'wetterdienst.dwd.metadata',
 'wetterdienst.dwd.observations',
 'wetterdienst.dwd.observations.metadata',
 'wetterdienst.dwd.observations.util',
 'wetterdienst.dwd.radar',
 'wetterdienst.dwd.radar.metadata',
 'wetterdienst.util']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'beautifulsoup4>=4.9.1,<5.0.0',
 'cachetools>=4.1.1,<5.0.0',
 'dateparser>=1.0.0,<2.0.0',
 'deprecation>=2.1.0,<3.0.0',
 'docopt>=0.6.2,<0.7.0',
 'dogpile.cache>=1.0.2,<2.0.0',
 'h5py>=2.10.0,<3.0.0',
 'lxml>=4.5.2,<5.0.0',
 'munch>=2.5.0,<3.0.0',
 'numpy>=1.19.2,<2.0.0,!=1.19.4',
 'pandas>=1.1.2,<2.0.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'scipy>=1.5.2,<2.0.0',
 'tables>=3.6.1,<4.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'tqdm>=4.47.0,<5.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 'bufr': ['pybufrkit>=0.2.17,<0.3.0'],
 'cratedb': ['crate[sqlalchemy]>=0.25.0,<0.26.0'],
 'docs': ['ipython>=7.10.1,<8.0.0',
          'matplotlib>=3.3.2,<4.0.0',
          'sphinx>=3.2.1,<4.0.0',
          'sphinx-material>=0.0.30,<0.0.31',
          'sphinx-autodoc-typehints>=1.11.0,<2.0.0',
          'sphinxcontrib-svg2pdfconverter>=1.1.0,<2.0.0',
          'tomlkit>=0.7.0,<0.8.0'],
 'duckdb': ['duckdb>=0.2.3,<0.3.0'],
 'excel': ['openpyxl>=3.0.5,<4.0.0'],
 'http': ['fastapi>=0.61.1,<0.62.0', 'uvicorn>=0.11.8,<0.12.0'],
 'influxdb': ['influxdb>=5.3.0,<6.0.0'],
 'ipython': ['ipython>=7.10.1,<8.0.0',
             'ipython-genutils>=0.2.0,<0.3.0',
             'matplotlib>=3.3.2,<4.0.0'],
 'mysql': ['mysqlclient>=2.0.1,<3.0.0'],
 'postgresql': ['psycopg2-binary>=2.8.6,<3.0.0'],
 'radar': ['wradlib>=1.9.0,<2.0.0', 'pybufrkit>=0.2.17,<0.3.0'],
 'sql': ['duckdb>=0.2.3,<0.3.0']}

entry_points = \
{'console_scripts': ['wddump = wetterdienst.dwd.radar.cli:wddump',
                     'wetterdienst = wetterdienst.cli:run']}

setup_kwargs = {
    'name': 'wetterdienst',
    'version': '0.11.0',
    'description': 'Open weather data for humans',
    'long_description': '###########################################\nWetterdienst - Open weather data for humans\n###########################################\n\n.. image:: https://github.com/earthobservations/wetterdienst/workflows/Tests/badge.svg\n   :target: https://github.com/earthobservations/wetterdienst/actions?workflow=Tests\n.. image:: https://codecov.io/gh/earthobservations/wetterdienst/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/earthobservations/wetterdienst\n.. image:: https://readthedocs.org/projects/wetterdienst/badge/?version=latest\n   :target: https://wetterdienst.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n\n.. image:: https://img.shields.io/pypi/pyversions/wetterdienst.svg\n   :target: https://pypi.python.org/pypi/wetterdienst/\n.. image:: https://img.shields.io/pypi/v/wetterdienst.svg\n   :target: https://pypi.org/project/wetterdienst/\n.. image:: https://img.shields.io/pypi/status/wetterdienst.svg\n   :target: https://pypi.python.org/pypi/wetterdienst/\n.. image:: https://pepy.tech/badge/wetterdienst/month\n   :target: https://pepy.tech/project/wetterdienst/month\n.. image:: https://img.shields.io/github/license/earthobservations/wetterdienst\n   :target: https://github.com/earthobservations/wetterdienst/blob/master/LICENSE.rst\n.. image:: https://zenodo.org/badge/160953150.svg\n   :target: https://zenodo.org/badge/latestdoi/160953150\n\n\nIntroduction\n************\nWelcome to Wetterdienst, your friendly weather service library for Python.\n\nWe are a group of like-minded people trying to make access to weather data in\nPython feel like a warm summer breeze, similar to other projects like\nrdwd_ for the R language, which originally drew our interest in this project.\n\nWhile our long-term goal is to provide access to multiple weather services,\nwe are still stuck with the German Weather Service (DWD). Contributions are\nalways welcome!\n\nThis program and its repository tries to use modern Python technologies\nall over the place. The library is based on Pandas across the board,\nuses Poetry for package administration and GitHub Actions for\nall things CI.\n\n\nFeatures\n********\n\nCoverage\n========\nThe library currently covers\n\n- Weather observation data.\n  Both historical and recent.\n- Radar data.\n  All of composite, radolan, radvor, sites and radolan_cdc.\n- MOSMIX statistical optimized scalar forecasts extracted from weather models.\n  Both MOSMIX-L and MOSMIX-S is supported.\n\nTo get better insight on which data we have currently made available, with this library\ntake a look at `data coverage`_.\n\n\nDetails\n=======\n- Get metadata for a set of Parameter, PeriodType and TimeResolution.\n- Get station(s) nearby a selected location.\n- Store/recover collected data.\n- Command line interface.\n- Run SQL queries on the results.\n- Export results to databases and other data sinks.\n- Public Docker image.\n\n\nSetup\n*****\nRun this to make ``wetterdienst`` available in your current environment:\n\n.. code-block:: bash\n\n    pip install wetterdienst\n\nSynopsis\n********\nGet historical data for specific stations, using Python:\n\n.. code-block:: python\n\n    from wetterdienst.dwd.observations import DWDObservationData, DWDObservationParameterSet,\n        DWDObservationPeriod, DWDObservationResolution\n\n    observations = DWDObservationData(\n        station_ids=[1048,4411],\n        parameters=[DWDObservationParameterSet.CLIMATE_SUMMARY,\n                    DWDObservationParameterSet.SOLAR],\n        resolution=DWDObservationResolution.DAILY,\n        start_date="1990-01-01",\n        end_date="2020-01-01",\n        tidy_data=True,\n        humanize_column_names=True,\n    )\n\n    # Collect and analyse data here.\n    for df in observations.collect_data():\n        print(df)\n\nGet data for specific stations from the command line:\n\n.. code-block:: bash\n\n    # Get list of all stations for daily climate summary data in JSON format\n    wetterdienst stations --parameter=kl --resolution=daily --period=recent\n\n    # Get daily climate summary data for specific stations\n    wetterdienst readings --station=1048,4411 --parameter=kl --resolution=daily --period=recent\n\n\nDocumentation\n*************\nWe strongly recommend reading the full documentation, which will be updated continuously\nas we make progress with this library:\n\n- https://wetterdienst.readthedocs.io/\n\nFor the whole functionality, check out the `Wetterdienst API`_ section of our\ndocumentation, which will be constantly updated. To stay up to date with the\ndevelopment, take a look at the changelog_. Also, don\'t miss out our examples_.\n\n\nData license\n************\nAlthough the data is specified as being open, the DWD asks you to reference them as\ncopyright owner. Please take a look at the `Open Data Strategy at the DWD`_ and the\n`Official Copyright`_ statements before using the data.\n\n\n.. _rdwd: https://github.com/brry/rdwd\n.. _Wetterdienst API: https://wetterdienst.readthedocs.io/en/latest/pages/api.html\n.. _data coverage: https://wetterdienst.readthedocs.io/en/latest/pages/data_coverage.html\n.. _changelog: https://wetterdienst.readthedocs.io/en/latest/pages/changelog.html\n.. _examples: https://github.com/earthobservations/wetterdienst/tree/master/example\n.. _Open Data Strategy at the DWD: https://www.dwd.de/EN/ourservices/opendata/opendata.html\n.. _Official Copyright: https://www.dwd.de/EN/service/copyright/copyright_artikel.html?nn=495490&lsbId=627548\n',
    'author': 'Benjamin Gutzmann',
    'author_email': 'gutzemann@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wetterdienst.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
