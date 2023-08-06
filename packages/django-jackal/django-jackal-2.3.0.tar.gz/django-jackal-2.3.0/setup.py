# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jackal',
 'jackal.helpers',
 'jackal.management',
 'jackal.management.commands',
 'jackal.mixins',
 'jackal.views']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.2,<4.0.0', 'djangorestframework>=3.11.0,<4.0.0']

setup_kwargs = {
    'name': 'django-jackal',
    'version': '2.3.0',
    'description': 'Boilerplate for Django and Django REST Framework',
    'long_description': 'Jackal, the Boilerplate library for Django REST Framework\n-------------------------------------------------------------\n\n.. image:: https://badge.fury.io/py/django-jackal.svg\n    :target: https://badge.fury.io/py/django-jackal\n\n.. image:: https://imgur.com/XnlU8T9.jpg\n    :width: 720px\n    :align: center\n\n\n**Jackal** is Boilerplate Library based on Django and Django REST Framework(DRF)\nthat help you easily implement the necessary features on your web backend server.\n\nInstallation\n===============\n\n.. code::\n\n    pip install django-jackal\n\n\nDocument\n============\n\nSee wiki_ for details.\n\n.. _wiki: https://github.com/joyongjin/jackal/wiki\n\nTest\n============\n\n.. code::\n\n    python runtests.py tests\n',
    'author': 'joyongjin',
    'author_email': 'wnrhd114@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joyongjin/jackal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
