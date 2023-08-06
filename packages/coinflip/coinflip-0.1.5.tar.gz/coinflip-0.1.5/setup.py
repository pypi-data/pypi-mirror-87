# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['coinflip',
 'coinflip._randtests',
 'coinflip._randtests.common',
 'coinflip.cli']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'altair>=4.1.0,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'numpy>=1.19.4,<2.0.0',
 'pandas>=1.1.4,<2.0.0',
 'rich>=9.2.0,<10.0.0',
 'scipy>=1.5.4,<2.0.0',
 'sortedcontainers>=2.3.0,<3.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{'docs': ['sphinx>=3,<4',
          'sphinx-rtd-theme>=0.5.0,<0.6.0',
          'sphinx-click>=2.5.0,<3.0.0'],
 'refimpl': ['more-itertools>=8.6.0,<9.0.0'],
 'test': ['tox>=3.20.1,<4.0.0',
          'pytest>=6.1.2,<7.0.0',
          'hypothesis>=5.41.2,<6.0.0',
          'pytest-timeout>=1.4.2,<2.0.0',
          'defaultlist>=1.0.0,<2.0.0']}

entry_points = \
{'console_scripts': ['coinflip = coinflip.cli.commands:main']}

setup_kwargs = {
    'name': 'coinflip',
    'version': '0.1.5',
    'description': 'Randomness testing for humans',
    'long_description': '========\ncoinflip\n========\n\nRandomness testing for humans\n\n|build| |docs| |license| |version| |supported-versions| |hypothesis| |black|\n\n*coinflip* aims to implement the tests recommended by `NIST SP800-22\n<https://csrc.nist.gov/publications/detail/sp/800-22/rev-1a/final>`_\nto check random number generators for randomness.  A user-friendly command-line\ninterface provided allows you to ``run`` the tests on your data, and\nsubsequently ``report`` on the results by generating informational HTML\ndocuments.\n\n``coinflip.randtests`` acts as the `public API\n<https://coinflip.readthedocs.io/en/latest/reference/randtests.html>`_\nfor `notebook users <https://jupyter.org/index.html>`_ and developers to use\nthe randomness tests directly. The tests are implemented as general solutions,\nmeaning they accept basically any sequence with two distinct elements!\n\n.. image:: https://raw.githubusercontent.com/Honno/coinflip/report/.video_files/thumb/thumb_thumb.png\n   :target: http://www.youtube.com/watch?v=0xrWG3Ki9Z8\n\nSetup\n=====\n\nYou can get the latest release of coinflip from PyPI.\n\n.. code-block:: console\n\n    $ pip install coinflip\n\nAlternatively you can get the (unstable) development version straight from\nGitHub.\n\n.. code-block:: console\n\n    $ pip install git+https://github.com/Honno/coinflip\n\nIf that means nothing to you, no fret! Please continue reading the instructions\nbelow.\n\nInstall Python 3.7+\n-------------------\n\nCross-platform installation instructions for Python  are available at\n`realpython.com/installing-python/ <https://realpython.com/installing-python/>`_.\n\nNote ``coinflip`` only works on **Python 3.7 or above**. Make sure you have\nPython 3.7 (or higher) by checking the version of your installation:\n\n.. code-block:: console\n\n    $ python --version\n    Python 3.7.X\n\nClone repository\n----------------\n\nYou can clone the source code via `Git\n<https://www.freecodecamp.org/news/what-is-git-and-how-to-use-it-c341b049ae61/>`_:\n\n.. code-block:: console\n\n    $ git clone https://github.com/Honno/coinflip\n\n\nInstall coinflip\n----------------\n\nEnter the directory *coinflip* is downloaded to:\n\n.. code-block:: console\n\n   $ cd coinflip\n\nYou can install *coinflip* via the ``pip`` module:\n\n.. code-block:: console\n\n    $ pip install -e .\n\n`pip <https://realpython.com/what-is-pip/>`_ is the standard package manager for\nPython, which should of installed automatically when installing Python 3.7+.\n\nTrial run\n---------\n\nTry running the randomness tests on an automatically generated binary sequence:\n\n.. code-block:: console\n\n    $ coinflip example-run\n\nIf the command ``coinflip`` is "not found", you may need to add your local\nbinaries folder to your shell\'s path. For example, in bash you would do the\nfollowing:\n\n.. code-block:: console\n\n    $ echo "export PATH=~/.local/bin:$PATH" >> ~/.bash_profile\n    $ source ~/.bash_profile\n\nIn the worst case, you can execute commands via ``python -m``:\n\n.. code-block:: console\n\n    $ python -m coinflip example-run\n\n\nQuick start\n===========\n\nRandomness tests can be ran over your RNG output via the ``run`` command.\n\n.. code-block:: console\n\n    $ coinflip run DATA OUT\n    ...\n\n``DATA`` is the path to newline-delimited text file that contains a binary\nsequence. An example file to use is available on `my gist\n<https://gist.github.com/Honno/dd6f3527e588428fa17a999042e3c6e8>`_.\nAlternatively, raw binary files can be read as bitstreams via the ``--binary``\nflag\n\n``OUT`` is the path where you want the results to be saved. The results will be\nsaved as a `pickle <https://docs.python.org/3/library/pickle.html>`_-serialised\nfile, which can be viewed again via the ``read`` command. Additionally you can\ngenerate informational HTML reports from the results via the ``report`` command,\nbut note that the reports are currently very lacking.\n\nOutput should comprise of the sequence parsed from ``DATA``, test-specific result\nsummaries, and a final overall summary table.\n\n.. |build| image:: https://img.shields.io/github/workflow/status/Honno/coinflip/Test\n    :target: https://github.com/Honno/coinflip/actions?query=workflow%3ATest\n    :alt: GitHub Workflow Status\n\n.. |docs| image:: https://readthedocs.org/projects/coinflip/badge/?style=flat\n    :target: https://readthedocs.org/projects/coinflip\n    :alt: Documentation Status\n\n.. |hypothesis| image:: https://img.shields.io/badge/hypothesis-tested-brightgreen.svg\n   :alt: Tested with Hypothesis\n   :target: https://hypothesis.readthedocs.io\n\n.. |version| image:: https://img.shields.io/pypi/v/coinflip.svg\n    :alt: PyPI package latest release\n    :target: https://pypi.org/project/coinflip\n\n.. |supported-versions| image:: https://img.shields.io/badge/python-3.7%2B-informational\n    :alt: Supported versions\n    :target: https://pypi.org/project/coinflip\n\n.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/coinflip.svg\n    :alt: Supported implementations\n    :target: https://pypi.org/project/coinflip\n\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :alt: Code style\n    :target: https://github.com/psf/black\n\n.. |license| image:: https://img.shields.io/badge/license-BSD-blueviolet\n    :alt: License\n    :target: https://github.com/Honno/coinflip/blob/master/LICENSE.md\n',
    'author': 'Matthew Barber',
    'author_email': 'quitesimplymatt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Honno/coinflip',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
