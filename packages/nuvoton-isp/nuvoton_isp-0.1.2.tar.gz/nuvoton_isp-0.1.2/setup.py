# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nuvoton_isp']

package_data = \
{'': ['*']}

install_requires = \
['pyusb>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['nuvoisp = nuvoton_isp.cli:main']}

setup_kwargs = {
    'name': 'nuvoton-isp',
    'version': '0.1.2',
    'description': 'Nuvoton ISP library and CLI',
    'long_description': '===========\nNuvoton ISP\n===========\n\n\n.. image:: https://img.shields.io/pypi/v/nuvoton_isp.svg\n        :target: https://pypi.python.org/pypi/nuvoton_isp\n\n.. image:: https://img.shields.io/travis/fishman/nuvoton_isp.svg\n        :target: https://travis-ci.org/fishman/nuvoton_isp\n\n.. image:: https://ci.appveyor.com/api/projects/status/fishman/branch/master?svg=true\n    :target: https://ci.appveyor.com/project/fishman/nuvoton_isp/branch/master\n    :alt: Build status on Appveyor\n\n.. image:: https://readthedocs.org/projects/nuvoton-isp/badge/?version=latest\n        :target: https://nuvoton-isp.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n.. image:: https://pyup.io/repos/github/fishman/nuvoton_isp/shield.svg\n     :target: https://pyup.io/repos/github/fishman/nuvoton_isp/\n     :alt: Updates\n\n\n\nNuvoton ISP library and CLI\n\n\n* Free software: MIT license\n\n* Documentation: https://fishman.github.io/nuvoton_isp\n\n\n\nInstallation:\n-------------\n\n.. code-block:: console\n\n    $ pip install nuvoton-isp\n\nUSAGE:\n------\n\n.. code-block:: console\n\n    $ nuvoisp -f firmware.bin\n\nFeatures\n--------\n\n* Flash APROM\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `wboxx1/cookiecutter-pypackage-poetry`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`wboxx1/cookiecutter-pypackage-poetry`: https://github.com/wboxx1/cookiecutter-pypackage-poetry\n',
    'author': 'Reza Jelveh',
    'author_email': 'pypi@jelveh.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fishman.github.io/nuvoton_isp',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
