# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cci_cli', 'cci_cli.circle', 'cci_cli.commands', 'cci_cli.common']

package_data = \
{'': ['*']}

install_requires = \
['confuse>=1.3,<2.0',
 'python-dateutil>=2.8,<3.0',
 'requests>=2.24,<3.0',
 'tabulate>=0.8,<0.9',
 'timeago>=1.0,<2.0',
 'typer>=0.3,<0.4']

entry_points = \
{'console_scripts': ['cci = cci_cli.main:app']}

setup_kwargs = {
    'name': 'cci-cli',
    'version': '0.1.0',
    'description': 'This is a small CircleCI CLI that allows you to interact with the CircleCI API v2',
    'long_description': '# CircleCI CLI\n\n[![CircleCI](https://circleci.com/gh/lightspeed-hospitality/circleci-cli.svg?style=svg&circle-token=639e11bbab82eb96b4cc285724c17de30fecf8ce)](https://app.circleci.com/pipelines/github/lightspeed-hospitality/circleci-cli)\n\n<p align="center">\n  <a href="#development">Development</a> •\n  <a href="#architecture--documentation">Documentation</a> •\n  <a href="#how-to-contribute">Contribute</a> •\n  <a href="#support--feedback">Support</a>\n</p>\n\n🛠 WIP\nThis is a small CircleCI CLI that allows you to interact with the [CircleCI API v2](https://circleci.com/docs/api/v2/).\n\n---\n\n## Use it!\n\n```console\ndocker pull lightspeedhq-ls-container-dev.jfrog.io/circleci-cli\ndocker run -it --rm --volume=$HOME/.config/circleci-cli:/root/.config/circleci-cli lightspeedhq-ls-container-dev.jfrog.io/circleci-cli\nbash-5.0# cci --help\nUsage: cci [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n\nCommands:\n  config\n  pipelines\n```\n\n### Create an alias\n\nYou can also create an alias for `cci` in your zsh or bash config:\n```\nalias cci=\'docker pull lightspeedhq-ls-container-dev.jfrog.io/circleci-cli && docker run -it --rm --volume=$HOME/.config/circleci-cli:/root/.config/circleci-cli lightspeedhq-ls-container-dev.jfrog.io/circleci-cli\'\n```\n\n### Commands\n\n* Display your config:\n```\ncci config show\n```\n\n* Create your config file:\n```\n# with prompts:\ncci config setup\n\n# using flags:\ncci config setup --vcs {gh,bb} --org <your-org> --token <circle-ci-api-token>\n````\n_Note_: To create your config you will need to have a Personal CircleCI API Token, that can be created [here](https://app.circleci.com/settings/user/tokens).\n\n\n* List the last 20 pipelines for <project-name>\n```\ncci pipelines list <project-name>\n```\n\n* Trigger a build for `<project-name>` using `<branch>`\n```\ncci pipelines trigger <project-name> --branch <branch> [--wait-for-result] [--timeout <min>] [--params key=value,...]\n```\n\n## Development\n\n### Setup\n\nFor development, best create a virtual environment and install all dependencies:\n```console\npython3 -m venv venv\n. venv/bin/activate\npip install -r requirements.txt\n```\n\n### Build\n\nYou can create a docker image on your local machine by:\n```console\ndocker build . -t circleci-cli\n```\n\n### Run\n\nIn order to run the build you created on your local machine, run:\n```console\ndocker run -it --rm --volume=$HOME/.config/circleci-cli:/root/.config/circleci-cli circleci-cli\n```\n\n## How to Contribute\n\nIn order to contribute you just have to have Python installed on your machine. In case you do not have it installed get it from [python.org](https://www.python.org/downloads/).\n\n#### Linting Tool\n\nThis project is using [pre-commit](https://pre-commit.com/) to enable linting and auto-formatting as a pre-commit hook.\nThe hooks are configured in [.pre-commit-config.yaml](./.pre-commit-config.yaml).\n\nTo install the hooks you have to run the following command (only once):\n```bash\n. venv/bin/activate\npre-commit install\n```\n\nThen you can trigger all the hooks manually by running:\n```bash\n. venv/bin/activate\npre-commit run --all-files\n```\n\nAdditionally on every `git commit` the hooks will be triggered and have to pass.\n\n#### How to run tests\n\nYou can run all the tests, by simply running:\n```bash\n. venv/bin/activate\npython -m pytest\n```\n\n\n\n## Support & Feedback\n\nYour contribution is very much appreciated. Feel free to create a PR or an Issue with your suggestions for improvements.\n',
    'author': 'Lightspeed Hospitality',
    'author_email': 'pt.hospitality.dev@lightspeedhq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
