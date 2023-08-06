# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyconfigurathon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyconfigurathon',
    'version': '0.1.2',
    'description': 'Simple python package to use a json file as a configuration file',
    'long_description': '#   PyConfigurathon\n\nA python package for making it easy to use and manage configuration files in your python applications.\n\n## Installation\n\n#### Using poetry\n    `poetry add pyconfigurathon`\n\n#### Using pip\n    `pip install pyconfigurathon`\n\n\n## How to use\n\nThe recommended way to use this module is to have a module dedicated to your configuration. Eg. config.py\n\n### Use with an absolute path to the configuration file:\n```\nfrom pyconfigurathon.configurator import configurator\n\n\ndef get_config(config_name, file_path="/path/to/file/settings.json"):\n    cf = configurator(file_path)\n\n    return cf.get(config_key=config_name)\n```\n\n### Use with a path to the configuration file relative to the config.py file\n```\nimport os\nfrom pyconfigurathon.configurator import configurator\n\n\ndef get_config(config_name, file="settings.json"):\n    conf = configurator(os.path.join(os.path.dirname(__file__), file))\n\n    return conf.get(config_key=config_name)\n```\n\nPlease note that these are only examples to help you get started faster. There are other ways to use this package.',
    'author': 'JermaineDavy',
    'author_email': None,
    'maintainer': 'Jermaine Davy',
    'maintainer_email': None,
    'url': 'https://github.com/JermaineDavy/pyconfigurathon',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
