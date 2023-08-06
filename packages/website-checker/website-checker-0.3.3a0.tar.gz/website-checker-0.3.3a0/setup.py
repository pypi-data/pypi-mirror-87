# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['website_checker']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.25.0,<3.0.0', 'structlog>=20.1.0,<21.0.0']

entry_points = \
{'console_scripts': ['check = website_checker.cli:cli']}

setup_kwargs = {
    'name': 'website-checker',
    'version': '0.3.3a0',
    'description': 'A simple python application for running checks against websites.',
    'long_description': '[![Tests](https://github.com/aidanmelen/website-checker/workflows/Tests/badge.svg)](https://github.com/aidanmelen/website-checker/actions?workflow=Tests)\n[![Release](https://github.com/aidanmelen/website-checker/workflows/Release/badge.svg)](https://github.com/aidanmelen/website-checker/actions?workflow=Release)\n[![PyPI](https://img.shields.io/pypi/v/website_checker.svg)](https://pypi.org/project/website-checker/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n# website_checker\n\nA simple python application for running checks against websites.\n\n## Usage\n\n### Install\n\n```bash\n$ pipx install website-checker\n  installed package site-check 0.1.0, Python 3.9.0\n  These apps are now globally available\n    - check\ndone! ✨ 🌟 ✨\n\n# or install into system python with pip\n# pip install website-checker\n```\n\n### Example\n\nDisplay help message\n\n```text\n$ check --help\nUsage: check [OPTIONS] COMMAND [ARGS]...\n\n  A simple python application for running checks against websites.\n\nOptions:\n  --debug / --no-debug  Toggle debug mode.\n  --version             Show the version and exit.\n  --help                Show this message and exit.\n\nCommands:\n  health   Check website health.\n  latency  Check website latency.\n  network  Check website network connectivity.\n```\n\nSome examples\n\n```bash\n$ check network -u https://google.com -u https://blarg.com\n{"event": {"check": "network", "input": {"timeout": 5, "url": "https://google.com"}, "output": "pass"}, "logger": "website-checker", "timestamp": "2020-11-30T05:27:23.413281"}\n{"event": {"check": "network", "input": {"timeout": 5, "url": "https://blarg.com"}, "output": "fail"}, "logger": "website-checker", "timestamp": "2020-11-30T05:27:23.443994"}\n\n$ check health -u https://google.com\n{"event": {"check": "health", "input": {"timeout": 5, "url": "https://google.com"}, "output": "pass"}, "logger": "website-checker", "timestamp": "2020-11-30T05:27:49.413241"}\n\n$ check latency -u https://google.com\n{"event": {"check": "latency", "input": {"threshold": 500, "timeout": 5, "url": "https://google.com"}, "output": "pass"}, "logger": "website-checker", "timestamp": "2020-11-30T05:28:14.460530"}\n```\n\n### Docker\n\n```bash\n$ docker run --rm -it aidanmelen/website-checker health --url https://google.com\n{"event": {"check": "health", "input": {"timeout": 5, "url": "https://google.com"}, "output": "pass"}, "logger": "website-checker", "timestamp": "2020-11-30T05:00:23.444290"}\n```\n\n# License\n\nCheck out the [LICENSE](./LICENSE) for more information.\n\n# Credits\n\nCheck out the [CREDITS](./docs/CREDITS.md) for more information.\n',
    'author': 'Aidan Melen',
    'author_email': 'aidanmelen@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aidanmelen/website-checker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
