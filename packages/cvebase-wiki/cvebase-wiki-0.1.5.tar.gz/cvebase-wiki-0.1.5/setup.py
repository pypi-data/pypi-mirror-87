# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvebase_wiki']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'cvebased>=0.1.7,<0.2.0',
 'python-editor>=1.0.4,<2.0.0',
 'rich>=9.2.0,<10.0.0']

entry_points = \
{'console_scripts': ['cvebase-wiki = cvebase_wiki.cvebase_wiki:cli']}

setup_kwargs = {
    'name': 'cvebase-wiki',
    'version': '0.1.5',
    'description': "cvebase's command line tool for interacting with cvebase.com wiki data",
    'long_description': "# cvebase-wiki\n\ncvebase's command line tool for interacting with cvebase.com wiki data.\n\n* [Visit cvebase.com web app](https://www.cvebase.com/)\n* [View wiki repo on GitHub (cvebase/cvebase.com)](https://github.com/cvebase/cvebase.com)\n\n## Installation\n\n```\npython3 -m pip install cvebase-wiki --upgrade\n```\n\n## Usage\n\nLint all CVE & Researcher markdown files.\n\n```\ncvebase-wiki lint -r <path to cvebase.com repo>\n```\n\nEdit CVE file. Looks for ${EDITOR} env variable, then system editor in order: vim, emacs, nano.\n\n```\ncvebase-wiki edit -t <path to cvebase.com repo> -t cve CVE-2020-14882\n```\n",
    'author': 'cvebase',
    'author_email': 'hello@cvebase.com',
    'maintainer': 'cvebase',
    'maintainer_email': 'hello@cvebase.com',
    'url': 'https://www.cvebase.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
