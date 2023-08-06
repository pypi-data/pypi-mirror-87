# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['checkdigit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'checkdigit',
    'version': '0.1.1',
    'description': 'A check digit library for data validation',
    'long_description': '# checkdigit\n\nA check digit library for data validation.\n  \n| Test Status | [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/harens/checkdigit/Tests?logo=github&style=flat-square)](https://github.com/harens/checkdigit/actions) [![Codecov](https://img.shields.io/codecov/c/github/harens/checkdigit?style=flat-square)](https://codecov.io/gh/harens/checkdigit)  |\n|:--|:--|\n| __Version Info__ | [![PyPI](https://img.shields.io/pypi/v/checkdigit?logo=pypi&logoColor=white&style=flat-square)](https://pypi.org/project/checkdigit/) [![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/harens/checkdigit?logo=github&style=flat-square)](https://github.com/harens/checkdigit/releases) [![PyPI - Downloads](https://img.shields.io/pypi/dm/checkdigit?logo=python&logoColor=white&style=flat-square)](https://pypi.org/project/checkdigit/) |\n| __Code Analysis__ |[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/harens/checkdigit?logo=code%20climate&style=flat-square)](https://codeclimate.com/github/harens/checkdigit) [![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/harens/checkdigit?logo=codefactor&style=flat-square)](https://www.codefactor.io/repository/github/harens/checkdigit) [![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/harens/checkdigit?logo=lgtm&style=flat-square)](https://lgtm.com/projects/g/harens/checkdigit/)|\n\n## 🔨 Installation\n\n```shell\npip install checkdigit\n```\n\nOr download the project [here](https://github.com/harens/checkdigit/archive/master.zip).\n\n## ✨ Features\n\n* Contains various functions relating to __Luhn, ISBN, UPC and many other codes__.\n* Extensive __in-code comments and docstrings__ to explain how the functions work.\n* Written in __pure Python__ with __no dependencies__ required to run the program.\n\nCheck out the [documentation](https://github.com/harens/checkdigit/wiki) for more details on how to use the library.\n\n## 🏗️ Contributing\n\nAny change, big or small, that you think can help improve this project is more than welcome 🎉.\n\nAs well as this, feel free to open an issue with any new suggestions or bug reports. Every contribution is valued.\n\nFor smaller tasks (that are still really appreciated 😃), be sure to check the [good first issue](https://github.com/harens/checkdigit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) tag.\n\n## 💻 Setup\n\nClone the project and install the dev dependencies:\n\n```shell\ngit clone https://github.com/harens/checkdigit\ncd checkdigit\npoetry install\n```\n\nIf you want to send a PR, please run the following:\n\n```bash\nbash ./scripts/format.sh # Format files\nbash ./scripts/tests.sh  # Run tests\n\n# NB shellcheck is not installed by poetry\nshellcheck scripts/*.sh\n```\n\n## 📒 License\n\nThis project is licensed under [GPL-3.0-or-later](https://github.com/harens/checkdigit/blob/master/LICENSE).\n',
    'author': 'harens',
    'author_email': 'harensdeveloper@gmail.com',
    'maintainer': 'harens',
    'maintainer_email': 'harensdeveloper@gmail.com',
    'url': 'https://github.com/harens/checkdigit',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
