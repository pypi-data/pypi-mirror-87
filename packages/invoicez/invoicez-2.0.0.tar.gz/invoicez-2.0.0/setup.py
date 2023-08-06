# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invoicez', 'invoicez.cli']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.0,<4.0.0',
 'Jinja2>=2.11.1,<3.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.1,<8.0.0',
 'coloredlogs>=14.0,<15.0']

entry_points = \
{'console_scripts': ['invoicez = invoicez.cli:cli']}

setup_kwargs = {
    'name': 'invoicez',
    'version': '2.0.0',
    'description': 'Tool to handle invoices.',
    'long_description': "# `invoicez`\n\n[![CI Status](https://img.shields.io/github/workflow/status/m09/invoicez/CI?label=CI&style=for-the-badge)](https://github.com/m09/invoicez/actions?query=workflow%3ACI)\n[![CD Status](https://img.shields.io/github/workflow/status/m09/invoicez/CD?label=CD&style=for-the-badge)](https://github.com/m09/invoicez/actions?query=workflow%3ACD)\n[![Test Coverage](https://img.shields.io/codecov/c/github/m09/invoicez?style=for-the-badge)](https://codecov.io/gh/m09/invoicez)\n[![PyPI Project](https://img.shields.io/pypi/v/invoicez?style=for-the-badge)](https://pypi.org/project/invoicez/)\n\nTool to handle invoices. It is currently not meant to be usable directly by people finding about the package on GitHub. Please open an issue if you want more details or want to discuss this solution.\n\n## Installation\n\nWith `pip`:\n\n    pip install invoicez\n\n## Directory Structure\n\n`invoicez` works with big assumptions on the directory structure of your presentation repository. Among those assumptions:\n\n- your directory should be a git repository\n- it should contain a jinja2 LaTeX invoice template in the `jinja2` directory, with a specific name (`main.tex.jinja2`)\n- your invoice folders should be contained in an organization/company folder. This is meant to avoid repeating the company details all over the place\n\n```\nroot (git repository)\n├── global-config.yml\n├── jinja2\n│\xa0\xa0 ├── main.tex.jinja2\n├── assets\n│\xa0\xa0 ├── img\n│\xa0\xa0 │\xa0\xa0 ├── logo.png\n│\xa0\xa0 │\xa0\xa0 └── signature.jpg\n├── company1\n│\xa0\xa0 └── company-config.yml\n│\xa0\xa0  \xa0\xa0 ├── invoice1.yml\n│\xa0\xa0  \xa0\xa0 └── invoice2.yml\n└── company2\n \xa0\xa0 └── company-config.yml\n \xa0\xa0  \xa0\xa0 ├── invoice1.yml\n \xa0\xa0  \xa0\xa0 └── invoice2.yml\n```\n\n## Configuration\n\n`invoicez` uses two configuration files to avoid repetition, one for your details and global values, one for the details of the company you're writing the invoice for.\n\n### Configuration merging\n\nThe company config is merged into the global config, you can use that fact to override global values for a specific company.\n\n### Using the configuration values\n\nThe values obtained from the merged configurations can be used directly in Jinja2 templates, or in LaTeX after a conversion from snake case to camel case: if the configuration contains the key `user_email`, it will be defined as the `\\UserEmail` command in LaTeX.\n\n## Usage\n\nSee the `--help` flag of the `invoicez` command line tool.\n",
    'author': 'm09',
    'author_email': '142691+m09@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m09/invoicez',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
