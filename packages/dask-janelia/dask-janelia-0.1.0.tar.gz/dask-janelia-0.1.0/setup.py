# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dask_janelia']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.1.1,<3.0.0',
 'dask-jobqueue==0.7.1',
 'dask[bag]>=2.19.0,<3.0.0',
 'distributed>=2.14.0,<3.0.0']

setup_kwargs = {
    'name': 'dask-janelia',
    'version': '0.1.0',
    'description': 'Simple dask distributed deployment for the Janelia Research Campus compute cluster.',
    'long_description': None,
    'author': 'Davis Vann Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
