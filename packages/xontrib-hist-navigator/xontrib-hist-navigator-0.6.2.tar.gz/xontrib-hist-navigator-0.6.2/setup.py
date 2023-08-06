# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

install_requires = \
['prompt-toolkit', 'xonsh>=0.9.20']

setup_kwargs = {
    'name': 'xontrib-hist-navigator',
    'version': '0.6.2',
    'description': "A Xonsh plugin to navigate between directories like fish's prevd/nextd",
    'long_description': '# xontrib-hist-navigator\n\nFish-shell like `prevd` and `nextd` for [xonsh](https://github.com/xonsh/xonsh/) with keyboard shortcuts\n\n# Usage\n\n- install using pip\n```sh\npip install xontrib-hist-navigator\n```\n\n- or xpip (that is installed alongside xonsh)\n\n```sh\nxpip install xontrib-hist-navigator\n```\n\n- add to list of xontribs loaded.\n\n```sh\nxontrib load hist_navigator\n```\n\n# Overview\n\n- it keeps track of `cd` usage per session\n- Shortcuts\n\n| command | description                                                        | shortcut          |\n| ------- | ------------------------------------------------------------------ | ----------------- |\n| nextd   | move to previous working directory                                 | Alt + Left Arrow  |\n| prevd   | move to next working directory in the history (if `prevd` is used) | Alt + Right Arrow |\n| listd   | list cd history                                                    |                   |\n| cd ..   | move to parent directory                                           | Alt + Up Arrow    |\n\n# Release\n\n```sh\npoetry version\npoetry publish\n```\n',
    'author': 'Noortheen Raja',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/xontrib-hist-navigator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
