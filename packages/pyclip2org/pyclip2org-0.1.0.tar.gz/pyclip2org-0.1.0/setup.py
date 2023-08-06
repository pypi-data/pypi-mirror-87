# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyclip2org']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'dateparser>=1.0.0,<2.0.0',
 'nox-poetry>=0.5.0,<0.6.0',
 'orgparse>=0.2.1,<0.3.0',
 'python-slugify>=4.0.1,<5.0.0',
 'textwrap3>=0.9.2,<0.10.0']

entry_points = \
{'console_scripts': ['pyclip2org = pyclip2org.__main__:main']}

setup_kwargs = {
    'name': 'pyclip2org',
    'version': '0.1.0',
    'description': 'My Clipping to org-mode notes',
    'long_description': "My Clipping to org-mode notes\n=============================\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/pyclip2org.svg\n   :target: https://pypi.org/project/pyclip2org/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/pyclip2org\n   :target: https://pypi.org/project/pyclip2org\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/pyclip2org\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/pyclip2org/latest.svg?label=Read%20the%20Docs\n   :target: https://pyclip2org.readthedocs.io/\n   :alt: Read the documentation at https://pyclip2org.readthedocs.io/\n.. |Tests| image:: https://github.com/ppalazon/pyclip2org/workflows/Tests/badge.svg\n   :target: https://github.com/ppalazon/pyclip2org/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/ppalazon/pyclip2org/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/ppalazon/pyclip2org\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* Parse 'My Clippings.txt' generated file\n* Extract highlights, marks and notes\n* Export to org-mode files separated by books\n\nRequirements\n------------\n\n* You will need a 'My Clippings.txt' file in English or Spanish\n\n\nInstallation\n------------\n\nYou can install *My Clipping to org-mode notes* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install pyclip2org\n\n\nUsage\n-----\n\nOnce you've installed, you can execute\n\n.. code:: console\n\n   $ pyclip2org -l en -o ~/org/kindle -c /media/Kindle/documents/My\\ Clippings.txt\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*My Clipping to org-mode notes* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\nThis project is based on\n`Managing kindle highlights with Python and GitHub <https://duarteocarmo.com/blog/managing-kindle-highlights-with-python-and-github.html>`_\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/ppalazon/pyclip2org/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://pyclip2org.readthedocs.io/en/latest/usage.html\n",
    'author': 'Pablo Palazon',
    'author_email': 'pablo.palazon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ppalazon/pyclip2org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
