# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nb_cli', 'nb_cli.project.hooks']

package_data = \
{'': ['*'],
 'nb_cli': ['plugin/*',
            'plugin/{{cookiecutter.plugin_slug}}/*',
            'project/*',
            'project/{{cookiecutter.project_slug}}/*',
            'project/{{cookiecutter.project_slug}}/{{cookiecutter.source_dir}}/plugins/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'cookiecutter>=1.7.2,<2.0.0',
 'docker-compose>=1.27.2,<2.0.0',
 'nonebot2>=2.0.0-alpha.7,<3.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'pyinquirer==1.0.3']

entry_points = \
{'console_scripts': ['nb = nb_cli.__main__:main']}

setup_kwargs = {
    'name': 'nb-cli',
    'version': '0.3.0',
    'description': 'CLI for nonebot2',
    'long_description': '# nb-cli\n\nCLI for nonebot2\n\nFeatures:\n\n- Create A NoneBot Project\n- Run NoneBot\n- Deploy NoneBot to Docker\n- Plugin Management\n  - Search for NoneBot Plugin on Pypi\n  - Install NoneBot Plugin on Pypi\n  - Create new plugins\n\n## How to use\n\n### Command-line usage\n\n```shell\nnb --help\n```\n\n### Interactive mode usage\n\n```shell\nnb\n```\n\n### CookieCutter usage\n\n```shell\npip install cookiecutter\ncookiecutter https://github.com/yanyongyu/nb-cli.git --directory="nb_cli/project"\n```\n',
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nonebot/nb-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
