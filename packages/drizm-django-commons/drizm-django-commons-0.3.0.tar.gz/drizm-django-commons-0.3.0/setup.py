# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drizm_django_commons',
 'drizm_django_commons.management.commands',
 'drizm_django_commons.serializers']

package_data = \
{'': ['*']}

install_requires = \
['django==3.1.1', 'djangorestframework==3.12.1', 'drf-yasg>=1.20.0,<2.0.0']

setup_kwargs = {
    'name': 'drizm-django-commons',
    'version': '0.3.0',
    'description': 'Django commons for the Drizm organization',
    'long_description': '# Django Commons\n[![PyPI version](https://badge.fury.io/py/drizm-django-commons.svg)](https://badge.fury.io/py/drizm-django-commons)\n\nThis package includes shared code used by\nthe Drizm organizations development team.  \n\nIt is not intended for public usage but you\nmay still download, redistribute or \nmodify it to your liking.\n\n## Installation\n\nInstall:  \n>pip install drizm-django-commons\n\nOnce installed through pip, include\nthe app in your settings.py like so:  \nINSTALLED_APPS += ["drizm_django_commons"]  \n\nIn order to use the applications\nmanage.py commands you must include the\napp at the top of the INSTALLED_APPS list.\n\nImport like so:  \nimport drizm_django_commons\n\n## Documentation\n\n### Custom Management Commands\n\n#### startapp\n\nThis version of startapp has been adjust to\nplay well together with the\nDrizm-Django-Template file structure.\n\nApart from that it is not majorly\ndivergent from the default commands\nfunctionality.\n\n#### maketest\n\nAutomagically creates boilerplate for a\nIntegration Test for a given application.\n\n## Changelog\n\n### 0.2.1\n\n- Added HrefModelSerializer which will\nserialize primary keys to hyperlinks\n- Moved testing.py dependencies to\ndrizm-commons package utilities\n\n### 0.2.2\n\n- Fixed bug with view selection for\nSelfHrefField\n\n### 0.3.0\n\n- Rework startapp command for better\ndefault file / folder structure\n- Add maketest <app-name> command\nto quickly generate boilerplate\nfor tests\n- Integrate DRF-yasg documentation\ninto Serializer Fields\n- Reduced boilerplate and added\nadditional code comments for\nserializer fields\n- Add HexColor field\n- Fix issue with implicit\nview_name retrieval on SelfHrefField\n',
    'author': 'ThaRising',
    'author_email': 'kochbe.ber@gmail.com',
    'maintainer': 'Dominik Lewandowski',
    'maintainer_email': 'dominik.lewandow@gmail.com',
    'url': 'https://github.com/drizm-team/django-commons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
