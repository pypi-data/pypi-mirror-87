# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prethink',
 'prethink.vendor',
 'prethink.vendor.rethinkdb',
 'prethink.vendor.rethinkdb.asyncio_net',
 'prethink.vendor.rethinkdb.backports',
 'prethink.vendor.rethinkdb.backports.ssl_match_hostname',
 'prethink.vendor.rethinkdb.gevent_net',
 'prethink.vendor.rethinkdb.tornado_net',
 'prethink.vendor.rethinkdb.trio_net',
 'prethink.vendor.rethinkdb.twisted_net']

package_data = \
{'': ['*'],
 'prethink.vendor': ['bin/*',
                     'rethinkdb-2.4.7.dist-info/*',
                     'six-1.15.0.dist-info/*']}

install_requires = \
['inflection>=0.5.1,<0.6.0', 'setuptools>=50.3.2,<51.0.0']

setup_kwargs = {
    'name': 'prethink',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Logi Leifsson',
    'author_email': 'logileifs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
