# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['docker_composer',
 'docker_composer._utils',
 'docker_composer.runner',
 'docker_composer.runner.cmd']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0', 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'docker-composer',
    'version': '0.8.5',
    'description': 'Use docker-compose from within Python',
    'long_description': '# Docker Composer\nA library to interact with `docker-compose` from a python Program.\nAll commands and parameters are exposed as python classes and attributes\nto allow for full auto-completion of its parameters with IDEs\nthat support it.\n\n\n## Install\n```shell script\npip install docker-composer\n```\n\n## Usage\nThe main class is `docker_composer.DockerCompose`. Its parameters are\nall options from `docker-compose`.\n \nEach `docker-compose` command has a corresponding function, e.g. \n`DockerCompose.run` or `DockerCompose.scale`. Their arguments again mirror \nthe options of the corresponding command.\n\nThe resulting object has a `call` function. \nIt takes arbitrary strings as input, as well as all keyword arguments from \n`subprocess.run`, and returns a `subprocess.CompletedProcess`\n\n```python\nfrom docker_composer import DockerCompose\n\n\nbase = DockerCompose(file="docker-compose.yml", verbose=True)\nbase.run(detach=True, workdir="/tmp").call("app")\nbase.run(workdir="/tmp").call("app", "/bin/bash", "-l")\n\n# /tmp $ ls /.dockerenv\n# /.dockerenv\n# /tmp $ exit\n\nprocess = base.ps(all=True).call(capture_output=True)\nprint(process.stdout.encode("UTF-8"))\n#          Name                      Command           State    Ports\n# -------------------------------------------------------------------\n# myapp_app_70fd8b786b76   myapp --start-server        Exit 0        \n# myapp_app_6ac3db4e1b55   myapp --client              Exit 0   \n```\n\n## Develop\n\n### Coding Standards\n\n| **Type**       | Package  | Comment                         |\n| -------------- | -------- | ------------------------------- |\n| **Linter**     | `black`  | Also for auto-formatted modules |\n| **Logging**    | `loguru` |                                 |\n| **Packaging**  | `poetry` |                                 |\n| **Tests**      | `pytest` |                                 |\n| **Typing**     | `mypy`   | Type all methods                |\n| **Imports**    | `isort`  |                                 |\n',
    'author': 'Micha',
    'author_email': 'schollm-git@gmx.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/schollm/docker-composer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
