# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mafe', 'mafe.process', 'mafe.scan']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.0,<6.0.0',
 'audio-metadata>=0.11.1,<0.12.0',
 'audioread>=2.1.8,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'librosa>=0.8.0,<0.9.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numba>=0.50,<0.51',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.4,<2.0.0',
 'python-magic>=0.4.18,<0.5.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'scipy>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['mafe = mafe.mafe:cli']}

setup_kwargs = {
    'name': 'mafe',
    'version': '0.3.1',
    'description': 'Music Audio Feature Extractor',
    'long_description': '# Music Audio Feature Extractor\n\n## Installation\n```shell script\n$ pip install mafe\n```\n\n## Typical usages\n```shell script\n# scan music tracks to extract raw set of features\n$ mafe -t scanned.csv.bz2 scan -f [MUSIC_DIR]\n# run normalization on extracted features\n$ mafe -t scanned.csv.bz2 -o normalized.csv.bz2 normalize\n# create table of distances between tracks\n$ mafe -t normalized.csv.bz2 -o distances.csv.bz2 distance\n# find clusters of similar tracks\n$ mafe -t normalized.csv.bz2 -o clustered.csv.bz2 cluster -n 4\n# run dimensionality reduction, keeping only the most distinctive features\n$ mafe -t normalized.csv.bz2 -o reduced.csv.bz2 pca\n# run clustering on distinct features, creating a visualization of the clusters\n$ mafe -t reduced.csv.bz2 -o clustered_reduced.csv.bz2 cluster -n 4 -V -I cluster.png\n```\n\n## Command line options\n```shell script\n$ mafe --help\nUsage: mafe [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -t, --tracks-csv TEXT  CSV file containing tracks  [required]\n  -o, --output TEXT      CSV file containing distances between the tracks\n                         [required]\n  --help                 Show this message and exit.\n\nCommands:\n  cluster\n  distance\n  normalize\n  pca\n  scan\n```\n',
    'author': 'Lene Preuss',
    'author_email': 'lene.preuss@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/lilacashes/mafe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
