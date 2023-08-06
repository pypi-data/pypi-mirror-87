# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamic_conf']

package_data = \
{'': ['*']}

install_requires = \
['arger>=1.0.10,<2.0.0']

entry_points = \
{'console_scripts': ['dynamic-conf = dynamic_conf:main']}

setup_kwargs = {
    'name': 'dynamic-conf',
    'version': '1.0.0',
    'description': 'Easy to manage Config variables separate from App code. Useful while developing and deploying( CI/CD) django web-apps',
    'long_description': '# dynamic-config\nProject configuration variables are declared beforehand and inferred from environment variables or configuration files. Useful while developing and deploying( CI/CD) django web-apps\n\n-------\n\n[![PyPi Version](https://img.shields.io/pypi/v/dynamic-conf.svg?style=flat)](https://pypi.python.org/pypi/dynamic-conf)\n[![Python Version](https://img.shields.io/pypi/pyversions/returns.svg)](https://pypi.org/project/dynamic-conf/)\n\n-------\n\n\n# Install\n```\npip install dynamic-conf\n```\n\n# Features\n- supports `.env` or `.py` files\n- supports casting with type annotations\n- You also don\'t need to include a sample file. Since the `Config` object would be able to generate `.env.py` itself.\n- It also loads Configuration variables from environment variables.\nThe order of preference is `env variables` > `env.py`\n- Attributes are lazily evaluated.\n\n# Getting Started\n\n- You need to subclass the `Config` class.\n- The config file should define all the variables needed for a project.\n\n```python\n\n# project/conf.py\n\nfrom dynamic_conf import Config, REQUIRED\n\nclass CONFIG(Config):\n    """singleton to be used for configuring from os.environ and env.py"""\n\n    # default settings\n\n    ENV = "prod" # optional field with a default value\n\n    DB_NAME = "db"\n    DB_HOST = "127.0.0.1"\n    DB_USER = "postgres"\n    DB_PASS = None # even None could be given as default value\n\n    SECRET_KEY:str # Python 3 only\n    AN_SECRET_KEY = REQUIRED # Python 2 & 3\n```\n\n- to create `project/env.py` just run with the path to CONFIG class\'s module\n```shell script\n# you could pass environment variables or set already with export\nenv DB_PASS=\'123\' dynamic-conf project/conf.py\n\ndynamic-conf project/conf.py DB_USER=\'user-1\' DB_PASS=\'123\' # pass as list of key-value pair\n\n#to filter environment variables with a prefix\nenv VARS_PREFIX="PROD_" dynamic-conf project/conf.py PROD_DB_USER="user-2"\n```\n\n# Usage\n\n- To use the config simply import and use particular attribute\n```python\n# project/settings.py\nfrom conf import CONFIG\nDATABASES = {\n    "default": {\n        "ENGINE": "django.contrib.gis.db.backends.postgis",\n        "HOST": CONFIG.DB_HOST,\n        "NAME": CONFIG.DB_NAME,\n        "USER": CONFIG.DB_USER,\n        "PASSWORD": CONFIG.DB_PASSWORD,\n        "PORT": "5432",\n    }\n}\n```\n',
    'author': 'Noortheen Raja',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/dynamic-conf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
