# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['broadworks_ocip']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.2.0,<21.0.0', 'classforge>=0.92,<0.93', 'lxml>=4.5.2,<5.0.0']

setup_kwargs = {
    'name': 'broadworks-ocip',
    'version': '1.2.0',
    'description': 'API interface to the OCI-P provisioning interface of a Broadworks softswitch',
    'long_description': '# Broadworks OCI-P Interface\n\n\n[![ci](https://img.shields.io/travis/nigelm/broadworks_ocip.svg)](https://travis-ci.com/nigelm/broadworks_ocip)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://nigelm.github.io/broadworks_ocip/)\n[![pypi version](https://img.shields.io/pypi/v/broadworks_ocip.svg)](https://pypi.python.org/pypi/broadworks_ocip)\n\n`broadworks_ocip` interfaces to the OCI-P provisioning interface of a Broadworks softswitch\n\n\n- Free software: BSD license\n- Documentation: https://nigelm.github.io/broadworks_ocip/\n\n----\n\n## Features\n\n- python objects to match all Broadworks schema objects\n- API framework to talk to a Broadworks server\n- additional magic to handle authentication and sessions\n- Based on Broadworks schema R21\n\n----\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install ssh2_parse_key\n```\n\n----\n\n## Usage\n\nMore details is given within the usage section of the documentation, but the\nminimal summary is:-\n\n```python\nfrom broadworks_ocip import BroadworksAPI\n\n# configure the API, connect and authenticate to the server\napi = BroadworksAPI(\n    host=args.host, port=args.port, username=args.username, password=args.password,\n)\n\n# get the platform software level\nresponse = api.command("SystemSoftwareVersionGetRequest")\nprint(response.version)\n```\n\n## Credits\n\nThe class is built using Michael DeHaan\'s [`ClassForge`](https://classforge.io/) object system.\n\nDevelopment on the python version was done by [`Nigel Metheringham <nigelm@cpan.org>`](https://github.com/nigelm/)\n\n----\n',
    'author': 'Nigel Metheringham',
    'author_email': 'nigelm@cpan.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/broadworks-ocip/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
