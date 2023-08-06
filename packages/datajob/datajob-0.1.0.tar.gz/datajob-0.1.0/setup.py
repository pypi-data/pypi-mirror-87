# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datajob', 'datajob.glue']

package_data = \
{'': ['*']}

install_requires = \
['aws-cdk.aws-glue>=1.70.0,<2.0.0',
 'aws-cdk.aws-s3-deployment>=1.70.0,<2.0.0',
 'aws-cdk.core>=1.70.0,<2.0.0',
 'contextvars>=2.4,<3.0',
 'stepfunctions>=1.1.2,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['datajob = datajob.datajob:run']}

setup_kwargs = {
    'name': 'datajob',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'vincent',
    'author_email': 'vclaes1986@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
