# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marko_backlinks',
 'marko_backlinks.adapters',
 'marko_backlinks.adapters.references_db',
 'marko_backlinks.dto',
 'marko_backlinks.entrypoints',
 'marko_backlinks.infrastructure',
 'marko_backlinks.interfaces',
 'marko_backlinks.usecases',
 'marko_backlinks.usecases.marko_ext']

package_data = \
{'': ['*']}

install_requires = \
['marko>=0.10.0,<0.11.0',
 'rich>=8,<10',
 'sqlalchemy>=1.3.20,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6,<4.0']}

entry_points = \
{'console_scripts': ['marko-backlinks = marko_backlinks.__main__:app']}

setup_kwargs = {
    'name': 'marko-backlinks',
    'version': '0.2.1',
    'description': 'Awesome `marko-backlinks` is a Python cli/package created with https://github.com/TezRomacH/python-package-template',
    'long_description': '# marko-backlinks\n\n<div align="center">\n\n[![Build status](https://github.com/jb-delafosse/marko-backlinks/workflows/build/badge.svg?branch=master&event=push)](https://github.com/jb-delafosse/marko-backlinks/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/marko-backlinks.svg)](https://pypi.org/project/marko-backlinks/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/jb-delafosse/marko-backlinks/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/jb-delafosse/marko-backlinks/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/jb-delafosse/marko-backlinks/releases)\n[![License](https://img.shields.io/github/license/jb-delafosse/marko-backlinks)](https://github.com/jb-delafosse/marko-backlinks/blob/master/LICENSE)\n\n</div>\n\n## Description\n\nThis project provide a markdown to markdown converter that adds a [Bi-Directional Link](https://maggieappleton.com/bidirectionals)\nSection at the end of each markdown files that is converted.\n\n\nThe project also provide a [pre-commit hook](https://pre-commit.com/) so you can easily integrate it within your own projects easily\n\nIt relies heavily on the [Marko](https://github.com/frostming/marko/tree/master/marko) python package that is the only \nMarkdown Parser with a Markdown Renderer that I know of.\n\n## Why\n\nI believe a great amount of information can be extracted from collaborative notes if we take time to structure them correctly.\n\nI wanted:\n- To make collaborative notes\n- To organize the notes in a [Roam](https://roamresearch.com/) like manner\n- Everyone to be able to navigate through the notes without installing anything\n- This system to be easily adopted by a software engineering team.\n\nUsing git and this converter as a pre-commit, I can easily do all of this ! 🚀\n\n## Installation as a python package\n\n```bash\npip install marko-backlinks\n```\n\nor install with `Poetry`\n\n```bash\npoetry add marko-backlinks\n```\n\nThen you can run\n\n```bash\nmarko-backlinks --help\n```\n\nor if installed with `Poetry`:\n\n```bash\npoetry run marko-backlinks --help\n```\n\n```bash\npoetry run marko-backlinks --name Roman\n```\n\n### Makefile usage\n\n[`Makefile`](https://github.com/jb-delafosse/marko-backlinks/blob/master/Makefile) contains many functions for fast assembling and convenient work.\n\n<details>\n<summary>1. Download Poetry</summary>\n<p>\n\n```bash\nmake download-poetry\n```\n\n</p>\n</details>\n\n<details>\n<summary>2. Install all dependencies and pre-commit hooks</summary>\n<p>\n\n```bash\nmake install\n```\n\nIf you do not want to install pre-commit hooks, run the command with the NO_PRE_COMMIT flag:\n\n```bash\nmake install NO_PRE_COMMIT=1\n```\n\n</p>\n</details>\n\n<details>\n<summary>3. Check the security of your code</summary>\n<p>\n\n```bash\nmake check-safety\n```\n\nThis command launches a `Poetry` and `Pip` integrity check as well as identifies security issues with `Safety` and `Bandit`. By default, the build will not crash if any of the items fail. But you can set `STRICT=1` for the entire build, or you can configure strictness for each item separately.\n\n```bash\nmake check-safety STRICT=1\n```\n\nor only for `safety`:\n\n```bash\nmake check-safety SAFETY_STRICT=1\n```\n\nmultiple\n\n```bash\nmake check-safety PIP_STRICT=1 SAFETY_STRICT=1\n```\n\n> List of flags for `check-safety` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`.\n\n</p>\n</details>\n\n<details>\n<summary>4. Check the codestyle</summary>\n<p>\n\nThe command is similar to `check-safety` but to check the code style, obviously. It uses `Black`, `Darglint`, `Isort`, and `Mypy` inside.\n\n```bash\nmake check-style\n```\n\nIt may also contain the `STRICT` flag.\n\n```bash\nmake check-style STRICT=1\n```\n\n> List of flags for `check-style` (can be set to `1` or `0`): `STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.\n\n</p>\n</details>\n\n<details>\n<summary>5. Run all the codestyle formaters</summary>\n<p>\n\nCodestyle uses `pre-commit` hooks, so ensure you\'ve run `make install` before.\n\n```bash\nmake codestyle\n```\n\n</p>\n</details>\n\n<details>\n<summary>6. Run tests</summary>\n<p>\n\n```bash\nmake test\n```\n\n</p>\n</details>\n\n<details>\n<summary>7. Run all the linters</summary>\n<p>\n\n```bash\nmake lint\n```\n\nthe same as:\n\n```bash\nmake test && make check-safety && make check-style\n```\n\n> List of flags for `lint` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.\n\n</p>\n</details>\n\n<details>\n<summary>8. Build docker</summary>\n<p>\n\n```bash\nmake docker\n```\n\nwhich is equivalent to:\n\n```bash\nmake docker VERSION=latest\n```\n\nMore information [here](https://github.com/jb-delafosse/marko-backlinks/tree/master/docker).\n\n</p>\n</details>\n\n<details>\n<summary>9. Cleanup docker</summary>\n<p>\n\n```bash\nmake clean_docker\n```\n\nor to remove all build\n\n```bash\nmake clean\n```\n\nMore information [here](https://github.com/jb-delafosse/marko-backlinks/tree/master/docker).\n\n</p>\n</details>\n\n## 📈 Releases\n\nYou can see the list of available releases on the [GitHub Releases](https://github.com/jb-delafosse/marko-backlinks/releases) page.\n\nWe follow [Semantic Versions](https://semver.org/) specification.\n\nWe use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.\n\nFor Pull Request this labels are configured, by default:\n\n|               **Label**               |  **Title in Releases**  |\n|:-------------------------------------:|:----------------------:|\n| `enhancement`, `feature`              | 🚀 Features             |\n| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |\n| `build`, `ci`, `testing`              | 📦 Build System & CI/CD |\n| `breaking`                            | 💥 Breaking Changes     |\n| `documentation`                       | 📝 Documentation        |\n| `dependencies`                        | ⬆️ Dependencies updates |\n\nYou can update it in [`release-drafter.yml`](https://github.com/jb-delafosse/marko-backlinks/blob/master/.github/release-drafter.yml).\n\nGitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/jb-delafosse/marko-backlinks)](https://github.com/jb-delafosse/marko-backlinks/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/jb-delafosse/marko-backlinks/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```\n@misc{marko-backlinks,\n  author = {jb-delafosse},\n  title = {Awesome `marko-backlinks` is a Python cli/package created with https://github.com/TezRomacH/python-package-template},\n  year = {2020},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/jb-delafosse/marko-backlinks}}\n}\n```\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'jb-delafosse',
    'author_email': 'jean-baptiste@lumapps.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jb-delafosse/marko-backlinks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
