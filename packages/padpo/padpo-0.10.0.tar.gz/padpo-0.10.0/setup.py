# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['padpo', 'padpo.checkers']

package_data = \
{'': ['*']}

install_requires = \
['pygrammalecte>=1.3.0,<2.0.0',
 'requests>=2.20.0,<3.0.0',
 'simplelogging>=0.10,<0.12']

entry_points = \
{'console_scripts': ['padpo = padpo.padpo:main']}

setup_kwargs = {
    'name': 'padpo',
    'version': '0.10.0',
    'description': 'Linter for gettext files',
    'long_description': "# padpo\n\n[![PyPI](https://img.shields.io/pypi/v/padpo.svg)](https://pypi.python.org/pypi/padpo)\n[![PyPI](https://img.shields.io/pypi/l/padpo.svg)](https://github.com/vpoulailleau/padpo/blob/master/LICENSE)\n[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Downloads](https://pepy.tech/badge/padpo)](https://pepy.tech/project/padpo)\n<!--\n[![Travis](https://api.travis-ci.com/vpoulailleau/padpo.svg?branch=master)](https://travis-ci.com/vpoulailleau/padpo)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/ab4759d5dc9cc7ea915e/test_coverage)](https://codeclimate.com/github/vpoulailleau/padpo/test_coverage)\n[![Maintainability](https://api.codeclimate.com/v1/badges/ab4759d5dc9cc7ea915e/maintainability)](https://codeclimate.com/github/vpoulailleau/padpo/maintainability)\n-->\n\n\nLinter for gettext files (*.po)\n\nCreated to help the translation of official Python docs in French: https://github.com/python/python-docs-fr\n\nIl faut demander aux traducteurs s'ils n'ont pas de pot quand ils traduisent, maintenant ils ont `padpo`…\n:smile: :laughing: :stuck_out_tongue_winking_eye: :joy: (note\xa0: il était tard le soir quand j'ai trouvé le nom).\n\n## License\n\nBSD 3-clause\n\nPull request are welcome.\n\n## Padpo is part of poutils!\n\n[Poutils](https://pypi.org/project/poutils) (`.po` utils) is a metapackage to easily install useful Python tools to use with po files\nand `padpo` is a part of it! Go check out [Poutils](https://pypi.org/project/poutils) to discover the other tools!\n\n\n## Usage\n\nUsing the *activated virtual environment* created during the installation:\n\nFor a local input file:\n\n```bash\npadpo --input-path a_file.po\n```\n\nor for a local input directory:\n\n```bash\npadpo --input-path a_directory_containing_po_files\n```\n\nor for a pull request in python-docs-fr repository (here pull request #978)\n\n```bash\npadpo --python-docs-fr 978\n```\n\nor for a pull request in a GitHub repository (here python/python-docs-fr/pull/978)\n\n```bash\npadpo --github python/python-docs-fr/pull/978\n```\n\n![Screenshot](screenshot.png)\n\n### Color\n\nBy default, the output is colorless, and formatted like GCC messages. You can use `-c`\nor `--color` option to get a colored output.\n\n## Installation\n\n### Automatic installation\n\n```bash\npip install padpo\n```\n\n### Manual installation\n\n1. Install dependencies\n\n   ```bash\n   poetry install\n   ```\n\n   Note: this uses `poetry` that you can get here: https://poetry.eustace.io/docs/\n\n2. Use virtual environment$\n\n   ```bash\n   poetry shell\n   ```\n\n## Update on PyPI\n\n`./deliver.sh`\n\n## Changelog\n\n### v0.10.0 (2020-12-04)\n\n* use `pygrammalecte` v1.3.0\n* use GitHub Actions\n\n### v0.9.0 (2020-09-07)\n\n* use `pygrammalecte` default message for spelling errors\n\n### v0.8.0 (2020-08-25)\n\n* use [`pygrammalecte`](https://github.com/vpoulailleau/pygrammalecte)\n* add continuous integration\n* fix #12, #13, #14, #15, #17, #18, #20\n* add `--color` CLI option to get a colored output (default is colorless)\n\n### v0.7.0 (2019-12-11)\n\n* add `--version` CLI option to display the current version of `padpo`\n* `--input-path` CLI option now accepts several paths as in\n  `padpo --input-path file1.po file2.po directory1 directory2` or\n  `padpo -i file1.po file2.po directory1 directory2`\n\n### v0.6.0 (2019-12-9)\n\n* check errors against defined glossaries\n\n### v0.5.0 (2019-12-3)\n\n* check spelling errors with grammalecte\n* tag releases!\n\n### v0.4.0 (2019-12-2)\n\n* use poetry: https://poetry.eustace.io/docs/\n* add some tests with tox and pytests\n* fix some false positive issues with grammalecte\n",
    'author': 'Vincent Poulailleau',
    'author_email': 'vpoulailleau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vpoulailleau/padpo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
