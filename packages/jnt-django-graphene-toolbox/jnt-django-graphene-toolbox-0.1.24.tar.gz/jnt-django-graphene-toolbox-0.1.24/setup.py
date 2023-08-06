# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jnt_django_graphene_toolbox',
 'jnt_django_graphene_toolbox.connection_fields',
 'jnt_django_graphene_toolbox.connection_fields.mixins',
 'jnt_django_graphene_toolbox.converters',
 'jnt_django_graphene_toolbox.errors',
 'jnt_django_graphene_toolbox.filters',
 'jnt_django_graphene_toolbox.filters.mixins',
 'jnt_django_graphene_toolbox.helpers',
 'jnt_django_graphene_toolbox.mutations',
 'jnt_django_graphene_toolbox.mutations.mixins',
 'jnt_django_graphene_toolbox.security.mixins',
 'jnt_django_graphene_toolbox.security.permissions',
 'jnt_django_graphene_toolbox.serializers',
 'jnt_django_graphene_toolbox.serializers.fields',
 'jnt_django_graphene_toolbox.serializers.validators',
 'jnt_django_graphene_toolbox.types',
 'jnt_django_graphene_toolbox.views']

package_data = \
{'': ['*'],
 'jnt_django_graphene_toolbox': ['locale/en/LC_MESSAGES/*',
                                 'locale/ru/LC_MESSAGES/*']}

install_requires = \
['django-filter>=2.3.0,<3.0.0',
 'djangorestframework>=3.11.0,<3.12.0',
 'graphene-file-upload>=1.2.2,<2.0.0',
 'graphene_django>=2.10.1,<3.0.0',
 'jnt_django_toolbox>=0.1.6,<0.2.0',
 'psycopg2-binary>=2.8.5,<3.0.0']

setup_kwargs = {
    'name': 'jnt-django-graphene-toolbox',
    'version': '0.1.24',
    'description': '',
    'long_description': None,
    'author': 'Junte',
    'author_email': 'tech@junte.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
