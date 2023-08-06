# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['meltano',
 'meltano.api',
 'meltano.api.controllers',
 'meltano.api.events',
 'meltano.api.executor',
 'meltano.api.models',
 'meltano.api.security',
 'meltano.api.workers',
 'meltano.cli',
 'meltano.core',
 'meltano.core.behavior',
 'meltano.core.bundle',
 'meltano.core.compiler',
 'meltano.core.job',
 'meltano.core.logging',
 'meltano.core.m5o',
 'meltano.core.plugin',
 'meltano.core.plugin.dbt',
 'meltano.core.plugin.model',
 'meltano.core.plugin.singer',
 'meltano.core.runner',
 'meltano.core.sql',
 'meltano.core.tracking',
 'meltano.core.utils',
 'meltano.migrations',
 'meltano.migrations.versions',
 'meltano.oauth']

package_data = \
{'': ['*'],
 'meltano.api': ['static/*',
                 'static/css/*',
                 'static/js/*',
                 'static/logos/*',
                 'templates/*',
                 'templates/email/pipeline_manual_run/*',
                 'templates/security/*',
                 'templates/security/email/*'],
 'meltano.oauth': ['templates/*']}

install_requires = \
['aiohttp>=3.4.4,<4.0.0',
 'alembic>=1.0.11,<2.0.0',
 'async_generator>=1.10,<2.0',
 'atomicwrites>=1.2.1,<2.0.0',
 'authlib>=0.10,<0.11',
 'bcrypt>=3.2.0,<4.0.0',
 'click-default-group>=1.2.1,<2.0.0',
 'click>=7.0,<8.0',
 'email-validator>=1.1.2,<2.0.0',
 'fasteners>=0.15.0,<0.16.0',
 'flask-cors>=3.0.7,<4.0.0',
 'flask-executor>=0.9.2,<0.10.0',
 'flask-restful>=0.3.7,<0.4.0',
 'flask-sqlalchemy>=2.4.4,<3.0.0',
 'flask>=1.0.2',
 'flatten-dict>=0.1.0,<0.2.0',
 'gunicorn>=19.9.0,<20.0.0',
 'ipython>=7.5.0,<8.0.0',
 'jsonschema>=2.6.0,<3.0.0',
 'markdown>=3.0.1,<4.0.0',
 'meltano-flask-security>=0.1.0,<0.2.0',
 'networkx>=2.2,<3.0',
 'psutil>=5.6.3,<6.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'pyhocon>=0.3.51,<0.4.0',
 'pyhumps==1.2.2',
 'pypika>=0.25.1,<0.26.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'python-gitlab>=1.8.0,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 'simplejson>=3.16.0,<4.0.0',
 'smtpapi>=0.4.1,<0.5.0',
 'snowflake-sqlalchemy>=1.2.3,<2.0.0',
 'sqlalchemy>=1.3.19,<2.0.0',
 'sqlparse>=0.3.0,<0.4.0',
 'watchdog>=0.9.0,<0.10.0',
 'werkzeug>=0.16.1,<0.17.0']

entry_points = \
{'console_scripts': ['meltano = meltano.cli:main']}

setup_kwargs = {
    'name': 'meltano',
    'version': '1.60.0',
    'description': 'Meltano',
    'long_description': '[![pipeline status](https://gitlab.com/meltano/meltano/badges/master/pipeline.svg)](https://gitlab.com/meltano/meltano/commits/master)\n\n# Meltano: open source ELT\n\n[Meltano](https://meltano.com) is an open source platform for\nbuilding, running & orchestrating ELT pipelines made up of\n[Singer](https://www.singer.io/) taps and targets and [dbt](https://www.getdbt.com)\nmodels, that you can [run locally](https://meltano.com/docs/installation.html) or\n[easily deploy in production](https://meltano.com/docs/production.html).\n\n## Documentation\n\nYou can find our documentation at [https://www.meltano.com/docs/](https://www.meltano.com/docs/).\n\n## Contributing to Meltano\n\nWe welcome contributions and improvements, please see the [contribution guidelines](https://meltano.com/docs/contributor-guide.html)\n\n## Responsible Disclosure Policy\n\nPlease refer to the [responsible disclosure policy](https://meltano.com/docs/responsible-disclosure.html) on our website.\n\n## License\n\nThis code is distributed under the MIT license, see the [LICENSE](LICENSE) file.\n',
    'author': 'Meltano Team and Contributors',
    'author_email': 'meltano@gitlab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/meltano/meltano',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
