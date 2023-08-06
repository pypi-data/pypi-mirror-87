# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['encapsia_cli']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.16.0,<0.17.0',
 'boto3>=1.14.29,<2.0.0',
 'click-completion>=0.5.0,<0.6.0',
 'click-shell>=2.0,<3.0',
 'click>=7.0,<8.0',
 'encapsia-api>=0.2.6,<0.3.0',
 'httpie>=2.2,<3.0',
 'requests[security,socks]>=2.24.0,<3.0.0',
 'semver>=2.10.2,<3.0.0',
 'tabulate>=0.8.3,<0.9.0',
 'toml>=0.10.0,<0.11.0']

extras_require = \
{'httpie-shell': ['http-prompt>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['encapsia = encapsia_cli.encapsia:encapsia']}

setup_kwargs = {
    'name': 'encapsia-cli',
    'version': '0.4.0',
    'description': 'Client CLI for talking to an Encapsia system.',
    'long_description': '# About\n\n[![Known Vulnerabilities](https://snyk.io/test/github/tcorbettclark/encapsia-cli/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/tcorbettclark/encapsia-cli?targetFile=requirements.txt)\n\nThis package provides command line access to Encapsia over the REST API.\n\nAll of these are designed to work with server 1.5 and beyond.\n\n## Autocomplete\n\nSetup autocomplete using the instructions found on <https://github.com/click-contrib/click-completion>\n\n## Tests\n\nSee the `walkthrough_tests` directory for bash scripts which exercise the CLI.\n\nRun them e.g. with:\n\n    bash walkthrough_tests/all.sh\n\nor test specific subcommands with:\n\n    bash walkthrough_tests/token.sh\n\nNote that these tests are *not* self-verifying; they just provide helpful coverage, assurance, and working documentation.\n\n## Release checklist\n\n* Run: `black .`\n* Run: `isort`\n* Run: `flake8 .`\n* Run: `mypy .`\n* Ensure "tests" run ok (see above).\n* Capture test output and commit with: `bash walkthrough_tests/all.sh 2>&1 | ansi2html -f 80% >WALKTHROUGH.html`\n* Create `requirements.txt` for Snyk scanning with: `poetry export -f requirements.txt >requirements.txt`\n* Ensure git tag, package version, and `enacpsia_cli.__version__` are all equal.',
    'author': 'Timothy Corbett-Clark',
    'author_email': 'timothy.corbettclark@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tcorbettclark/encapsia-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
