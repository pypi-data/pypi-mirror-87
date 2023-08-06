# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kimsufichecker']

package_data = \
{'': ['*']}

install_requires = \
['colorama', 'requests']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata']}

entry_points = \
{'console_scripts': ['kimsufi-checker = kimsufichecker.cli:run']}

setup_kwargs = {
    'name': 'kimsufichecker',
    'version': '1.1.0',
    'description': 'Command line tool to monitor Kimsufi plans availability',
    'long_description': '# Kimsufi Checker\n\nTool to check [Kimsufi (OVH)](https://www.kimsufi.com) availability and execute actions when a plan is available or not available.\n\n# Install\n\nTo install *Kimsufi Checker* from [PyPI](https://pypi.org/project/kimsufichecker/) simply run\n```sh\n$ pip3 install -U --user kimsufichecker\n$ kimsufi-checker --help\n```\n\nTo install it from the git repository, ensure you installed *Poetry* first:\n```sh\n$ pip3 install -U --user poetry\n$ pip3 install --user git+https://github.com/essembeh/kimsufi-checker\n$ kimsufi-checker --help\n```\n\nTo install it in a *virtualenv*\n```\n$ pip3 install -U --user poetry\n$ git clone https://github.com/essembeh/kimsufi-checker\n$ cd kimsufi-checker\n$ poetry install\n\n$ poetry run kimsufi-checker --help\n--or--\n$ poetry shell\n(.venv) $ kimsufi-checker --help\n```\n\n# Usage\n\n```sh\n$ kimsufi-checker --help\nusage: kimsufi-checker [-h] [-s SECONDS] [-z ZONE] [-x COMMAND] [-X COMMAND]\n                       [-1]\n                       [plans [plans ...]]\n\ntool to perform actions when Kimsufi availabilty changes\n\npositional arguments:\n  plans                 plans to check, example 1801sk13 or 1801sk14\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -s SECONDS, --sleep SECONDS\n                        duration (in seconds) between checks, default: 60\n  -z ZONE, --zone ZONE  check availability in specific zones (example: rbx or\n                        gra)\n  -x COMMAND, --available COMMAND\n                        command to execute when plan becomes available\n  -X COMMAND, --not-available COMMAND\n                        command to execute when plan is not available anymore\n  -1, --execute-on-init\n                        execute -x/-X action on first check, by default\n                        actions are run when plan status change\n\n```\n\n# Example\n\nTo list all plan identifiers and all zone identifiers, use `kimsufi-checker` without argument\n```sh \n$ kimsufi-checker \nList of plans:\n  150cagame1\n  150cagame2\n  150game1\n  150game2\n  1623hardzone1\n[...]\nList of zones:\n  bhs\n  fra\n  gra\n[...]\n```\n\nIf you want to be notified by SMS using the Free Mobile SMS API when plans *1801sk13* or *1801sk14* are available in France or Canada by checking every 10 minutes, use this command:\n\n```sh\n$ kimsufi-checker \\\n    --sleep 600 \\\n    --zone rbx \\\n    --zone gra \\\n    -x \'curl "https://smsapi.free-mobile.fr/sendmsg?user=123456789&pass=MYPASSWORD&msg=Kimsufi%20{plan}%20available"\' \\\n    -X \'curl "https://smsapi.free-mobile.fr/sendmsg?user=123456789&pass=MYPASSWORD&msg=Kimsufi%20{plan}%20not%20available"\' \\\n    1801sk13 1801sk14\n```\n\n> Note: replace `123456789` and `MYPASSWORD` with your own [Free Mobile credentials](https://mobile.free.fr/moncompte/index.php?page=options).\n',
    'author': 'Sébastien MB',
    'author_email': 'seb@essembeh.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/essembeh/kimsufi-checker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
