# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['pypi_client', 'pypi_client.types']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'diskcache>=5.0.3,<6.0.0',
 'lxml>=4.6.1,<5.0.0',
 'pydantic>=1.7.2,<2.0.0',
 'requests-mock>=1.8.0,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['pypi-client = pypi_client.cli:cli']}

setup_kwargs = {
    'name': 'pypi-client',
    'version': '0.1.11',
    'description': 'PyPI command-line tool',
    'long_description': "PyPI client\n===========\n\n![Lint and test](https://github.com/abahdanovich/pypi-client/workflows/Lint%20and%20test/badge.svg)\n\nCLI tool for searching for a python package by name.\n\n* fetches all package names from PyPi\n* filters and finds matching packages (by name)\n* downloads github stars (if package uses GH as a repo) number and package downloads\n* shows results in a table or json\n\nInstall\n-------\n\n```\npip install pypi-client\n```\n\nUsage\n-----\n\n```\nUsage: pypi-client [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  auth-github  Log into GitHub\n  search       Search python package by name\n```\n\nSearch\n------\n\n```\nUsage: pypi-client search [OPTIONS] NAME_SEARCH\n\n  Search python package by name\n\nOptions:\n  --limit INTEGER RANGE  Max number of items to return\n  --no-cache             Clear cache before run\n  --verbose              Print debug messages\n  --json                 Return in json format\n  --threads INTEGER      Number of threads to use\n  --help                 Show this message and exit.\n```\n\nExample output:\n\n```\n$ pypi-client search kafka\nFound 155 packages:\nname                                 downloads  summary                                                version      home_page                                                stars    releases  last_release_date\n---------------------------------  -----------  -----------------------------------------------------  -----------  -----------------------------------------------------  -------  ----------  -------------------\nkafka-python                           6863094  Pure Python client for Apache Kafka                    2.0.2        https://github.com/dpkp/kafka-python                      4084          34  2020-09-30\nconfluent-kafka                        3341286  Confluent's Python client for Apache Kafka             1.5.0        https://github.com/confluentinc/confluent-kafka-py...     2017          20  2020-08-07\nns-kafka-python                           5739  Pure Python client for Apache Kafka                    1.4.7        https://github.com/dpkp/kafka-python                      4084           1  2020-09-28\ntencentcloud-sdk-python-ckafka           11820  Tencent Cloud Ckafka SDK for Python                    3.0.290      https://github.com/TencentCloud/tencentcloud-sdk-p...      297          40  2020-11-12\nkafka                                   939197  Pure Python client for Apache Kafka                    1.3.5        https://github.com/dpkp/kafka-python                      4084          17  2017-10-07\n[...]\n```",
    'author': 'Andrzej Bogdanowicz',
    'author_email': 'bahdanovich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abahdanovich/pypi-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
