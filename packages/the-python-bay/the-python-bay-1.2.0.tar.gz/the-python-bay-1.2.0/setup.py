# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['the_python_bay', 'the_python_bay.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests']

setup_kwargs = {
    'name': 'the-python-bay',
    'version': '1.2.0',
    'description': 'A python library for searching thepiratebay.org',
    'long_description': '[![title](https://img.shields.io/pypi/v/the-python-bay.svg)](https://pypi.org/project/the-python-bay)\n[![title](https://img.shields.io/pypi/pyversions/the-python-bay.svg)](https://pypi.org/project/the-python-bay)\n\n- [Install](#install)\n- [Basic Usage](#basic-usage)\n- [Full docs](#full-docs)\n    - [search](#search)\n    - [top_movies](#top_movies)\n    - [top_tv](#top_tv)\n    - [Torrent](#torrent)\n\n\n# the-python-bay\n\nPython library for searching thepiratebay.org\n\n## Install\n\n```bash\npip install the-python-bay\n```\n## Basic Usage\n\n```python\nfrom the_python_bay import tpb\n\nresults = tpb.search("ubuntu")\n```\n\nThis will return the a list of instances of the `Torrent` class.\n\nSo you can then access the data like so:\n```python\nfor torrent in results:\n    print(f"{torrent.name} - {torrent.magnet}")\n```\n\n## Full Docs\n### search\nThis can be used to search thepiratebay.org, it will return a list of instances of the `Torrent` class.\n```python\nfrom the_python_bay import tpb\nresults = tpb.search("ubuntu")\n```\n\n### top_movies\nCan be used to return the current top 100 movies on thepiratebay.org\n```python\nfrom the_python_bay import tpb\nresults = tpb.top_movies()\n```\n\n### top_tv\nCan be used to return the current top 100 tv on thepiratebay.org\n```python\nfrom the_python_bay import tpb\nresults = tpb.top_tv()\n```\n\n### Torrent\nThe `Torrent` class is the format the torrents are returned in, it has the following attributes:\n- `name`     the torrents name\n- `magent`   the torrents magnet link\n- `seeders`  number of seeders the torrent has\n- `username` the username of the torrents uploader\n- `status`   the users prominence status\n\nTorrent also has the property `json` that can he used to return the json/dict of the the object. It can be used more generally:\n```python\nfrom the_python_bay import tpb\nresults = tpb.search_json("ubuntu")\n\n```\nOr it can be used on a specific `Torrent` object like so:\n```python\nfrom the_python_bay import tpb\nresults = tpb.search("ubuntu")\nfor torrent in results:\n    print(torrent.json)\n```\nOr even more directly:\n```python\ntorrent = Torrent(data)\ntorrent.json\n```',
    'author': 'Philip Bell',
    'author_email': 'philhabell@gmail.com',
    'maintainer': 'Philip Bell',
    'maintainer_email': 'philhabell@gmail.com',
    'url': 'https://github.com/philhabell/the-python-bay',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
