# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databricksbundle']

package_data = \
{'': ['*'],
 'databricksbundle': ['_config/*',
                      'container/*',
                      'dbutils/*',
                      'jdbc/*',
                      'notebook/*',
                      'pipeline/decorator/*',
                      'pipeline/decorator/executor/*',
                      'pipeline/function/*',
                      'pipeline/function/service/*',
                      'spark/*',
                      'spark/config/*']}

install_requires = \
['injecta>=0.8.9,<0.9.0',
 'logger-bundle>=0.5.0,<0.6.0',
 'pyfony-bundles>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'databricks-bundle',
    'version': '0.5.10b2',
    'description': 'Databricks bundle for the Pyfony framework',
    'long_description': '# Databricks bundle\n\nThis bundle allows you to create simple functional Databricks pipelines, which can be easily auto-documented and unit-tested. It is part of the [Bricksflow framework](https://github.com/bricksflow/bricksflow).\n\n![alt text](docs/functional_pipeline.png "Databricks functional pipeline example")\n\n## Installation\n\nInstall the bundle via Poetry:\n\n```\n$ poetry add databricks-bundle && poetry add databricks-connect --dev && poetry add py4j --dev\n```\n\nAdd the `DatabricksBundle.autodetect()` to your application\'s **Kernel.py** to activate it:\n\n```python\nfrom pyfony.kernel.BaseKernel import BaseKernel\nfrom databricksbundle.DatabricksBundle import DatabricksBundle\n\nclass Kernel(BaseKernel):\n    \n    def _registerBundles(self):\n        return [\n            # ...\n            DatabricksBundle.autodetect(),\n            # ...\n        ]\n```\n\n## Usage\n\n1. [Writing functional pipelines](docs/pipelines.md)\n1. [Recommended pipelines structure](docs/structure.md)\n1. [Configuring pipelines](docs/configuration.md)\n1. [Using dependencies](docs/dependencies.md)\n1. [Databricks Connect setup](docs/databricks-connect.md)\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bricksflow/databricks-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
