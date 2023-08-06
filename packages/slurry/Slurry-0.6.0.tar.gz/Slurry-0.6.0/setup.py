# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slurry']

package_data = \
{'': ['*']}

install_requires = \
['trio>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'slurry',
    'version': '0.6.0',
    'description': 'An async stream processing microframework',
    'long_description': "======\nSlurry\n======\n\n.. image:: https://readthedocs.org/projects/slurry/badge/?version=latest\n   :target: https://slurry.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://img.shields.io/pypi/v/slurry.svg\n   :target: https://pypi.org/project/slurry\n   :alt: Latest PyPi version\n\n.. image:: https://travis-ci.com/andersea/slurry.svg?branch=master\n   :target: https://travis-ci.com/andersea/slurry\n   :alt: Build Status\n\nAn async stream processing microframework for Python\n\nIntroduction\n------------\n\nSlurry_ builds on the concepts of structured concurrency and memory channels, originating in\nTrio_, and uses them to create a microframework for processing streaming data.\n\nThe basic building blocks of Slurry includes:\n\n- **Pipelines** - An asynchronous context manager which encapsulates a stream process.\n- **Sections** - The individual processing steps.\n- **Taps** - Output channels for the processed stream.\n- **Extensions** - A way to add more processing steps to an existing pipeline.\n\nSlurry avoids using asynchronous generator functions, in favor of the pull-push programming style\nof memory channels. It can be thought of as an asynchronous version of itertools_ - on steroids!\n\nIncluded in the basic library are a number of basic stream processing building blocks, like\n``Map``, ``Chain``, ``Merge`` and ``Zip``, and it is easy to build your own!\n\nDemonstration\n-------------\nEnough talk! Time to see what's up!\n\n.. code-block:: python\n\n   async with Pipeline.create(\n        Zip(produce_increasing_integers(1, max=3), produce_alphabet(0.9, max=3))\n    ) as pipeline, pipeline.tap() as aiter:\n            results = []\n            async for item in aiter:\n                results.append(item)\n            assert results == [(0,'a'), (1, 'b'), (2, 'c')]\n\nThe example producers (which are not part of the framework) could look like this:\n\n.. code-block:: python\n\n   async def produce_increasing_integers(interval, *, max=3):\n      for i in range(max):\n         yield i\n         if i == max-1:\n               break\n         await trio.sleep(interval)\n\n   async def produce_alphabet(interval, *, max=3):\n      for i, c in enumerate(string.ascii_lowercase):\n         yield c\n         if i == max - 1:\n               break\n         await trio.sleep(interval)\n\nFurther documentation is available on readthedocs_. Check out the `source code`_ on github__.\n\nInstallation\n------------\nStill here? Wanna try it out yourself? Install from PyPI_::\n\n   pip install slurry\n\nSlurry is tested on Python 3.6 or greater. For now, Slurry is Trio only. AnyIO_ support is not\nruled out in the future.\n\nLicense\n-------\nSlurry is licensed under the `MIT license`_.\n\n.. _Slurry: https://github.com/andersea/slurry\n.. _Trio: https://github.com/python-trio/trio\n.. _itertools: https://docs.python.org/3/library/itertools.html\n.. _PyPI: https://pypi.org/\n.. _readthedocs: https://slurry.readthedocs.io/\n.. _`source code`: https://github.com/andersea/slurry\n__ `source code`_\n.. _AnyIO: https://github.com/agronholm/anyio\n.. _MIT license: https://github.com/andersea/slurry/blob/master/LICENSE\n\n",
    'author': 'Anders Ellenshøj Andersen',
    'author_email': 'andersa@ellenshoej.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andersea/slurry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
