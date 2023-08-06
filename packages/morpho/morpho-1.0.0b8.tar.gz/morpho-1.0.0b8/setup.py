# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['morpho', 'morpho.rest']

package_data = \
{'': ['*'], 'morpho.rest': ['swagger/*', 'swagger/.swagger-codegen/*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'flask>=1.1.1,<2.0.0',
 'py-eureka-client>=0.7.4,<0.8.0',
 'pydantic>=1.5.1,<2.0.0',
 'regex>=2020.6.7,<2021.0.0',
 'requests>=2.22.0,<3.0.0',
 'toml>=0.10.0,<0.11.0',
 'waitress>=1.4.2,<2.0.0']

entry_points = \
{'console_scripts': ['morpho = morpho.cli:run']}

setup_kwargs = {
    'name': 'morpho',
    'version': '1.0.0b8',
    'description': 'A framework for microservice based document transformation.',
    'long_description': '<img src="https://raw.githubusercontent.com/B4rtware/morpho/master/docs/images/morpho.png" width="100%" alt="Morpho Logo">\n\n> Python port for the go written [doctrans](https://github.com/theovassiliou/doctrans)\n\n<div align="center">\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n</a>\n<a href="https://github.com/B4rtware/morpho/blob/master/LICENSE"><img alt="license: MIT" src="https://img.shields.io/badge/license%3A-MIT-green">\n</a>\n<a href="https://github.com/B4rtware/morpho"><img src="https://img.shields.io/badge/python%3A-%5E3.8-blue"></a><br>\n<a href="https://app.circleci.com/pipelines/github/B4rtware/morpho"><img src="https://circleci.com/gh/B4rtware/morpho.svg?style=shield"></a>\n<a href="https://codecov.io/gh/B4rtware/morpho">\n  <img src="https://codecov.io/gh/B4rtware/morpho/branch/master/graph/badge.svg" />\n</a>\n<a href="">\n  <img src="https://img.shields.io/pypi/v/morpho?color=dar-green" />\n</a>\n</div>\n\nMorpho is a framework for microservice based web services. It offers the ability to transform a given document with a provided function.\n\nIn the first place this framework was created to be used for research purposes.\n\n## 💡 Installation\n\n`pip install morpho`\n\n### via git\n\n1. make sure to use at least **python 3.8**\n2. clone the repo `git clone https://github.com/B4rtware/morpho.git`\n3. `cd morpho` and install dependencies via\n    - `poetry install` ([Poetry](https://github.com/python-poetry/poetry))\n    or\n    - use the provided `requirements.txt`\n\n## ⚙️ Server Example\n\n### ... without options\n\nservice.py\n```python\nfrom morpho.server import Service\n\ndef work(document: str) -> str:\n    return document\n\nservice = Service(name="Echo", version="0.0.1")\n\nif __name__ == "__main__":\n    service.run()\n```\n\n### ... with options\n\nservice.py\n```python\nfrom morpho.server import Service\nfrom pydantic import BaseModel\n\nclass Options(BaseModel):\n    name: str\n\ndef work(document: str, options: Options) -> str:\n    return document + options.name\n\nservice = Service(name="AppendName", version="0.0.1", options_type=Options)\n\nif __name__ == "__main__":\n    service.run()\n```\n\n## 🖥️ Client Example\n\nclient.py\n```python\nfrom morpho.client import Client\nfrom morpho.client import ClientConfig\n\nmorpho = Client(ClientConfig("http://localhost:8761/eureka/"))\n\nresponse = morpho.transform_document(\n    "This is a Document!",\n    service_name="Echo"\n)\n\nprint(response.document)\n```\n`>>> This is a Document!`\n\n## 👩🏽\u200d💻 Development\n\n### Creating a new release\n\n1. Run the following command `poetry version <version>`\n<br>*Morpho* uses the following schema: `^\\d+\\.\\d+\\.\\d+((b|a)\\d+)?$`\n\n2. Bump the version within the file: `morpho/__version__.py`\n<br>Make sure it\'s the same version used when bumping with poetry\n\n3. Open `Changelog.md` and write the new changelog:\n    - Use the following `#` header: `v<version> - (dd.mm.yyyy)`\n    <br>Used `##` headers:\n    - 💌 Added\n    - 🔨 Fixed\n    - ♻️ Changed\n\n4. Stage the modified files and push them with the following commit message:\n    > chore: bump to version `<version>`\n\n5. Run the following command `poetry build` to create a tarball and a wheel based on the new version\n\n6. Create a new github release and:\n    1. Copy and paste the changelog content **without** the `#` header into the *description of the release* textbox\n    2. Use the `#` header style to fill in the *Release title* (copy it from the `Changelog.md`)\n    3. Copy the version with the `v`-prefix into the *Tag version*\n\n7. Attach the produced tarball and wheel (`dist/`) to the release\n\n8. Check *This is a pre-release* if it\'s either an alpha or beta release *(a|b)* - ***optional*** \n\n9. **Publish release**\n\n## 📝 License\nMIT\n',
    'author': 'B4rtware',
    'author_email': '34386047+B4rtware@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://python-morpho.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
