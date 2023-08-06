# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['modelldcatnotordf']

package_data = \
{'': ['*']}

install_requires = \
['concepttordf>=1.0.0,<2.0.0',
 'datacatalogtordf>=1.2.0,<2.0.0',
 'rdflib-jsonld>=0.5.0,<0.6.0',
 'rdflib>=5.0.0,<6.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.5.0,<2.0.0']}

setup_kwargs = {
    'name': 'modelldcatnotordf',
    'version': '0.0.6',
    'description': 'A library for mapping a modelldcatno model to rdf',
    'long_description': '# modelldcatnotordf\n\n![Tests](https://github.com/Informasjonsforvaltning/modelldcatnotordf/workflows/Tests/badge.svg)\n[![codecov](https://codecov.io/gh/Informasjonsforvaltning/modelldcatnotordf/branch/master/graph/badge.svg)](https://codecov.io/gh/Informasjonsforvaltning/modelldcatnotordf)\n[![PyPI](https://img.shields.io/pypi/v/modelldcatnotordf.svg)](https://pypi.org/project/modelldcatnotordf/)\n[![Read the Docs](https://readthedocs.org/projects/modelldcatnotordf/badge/)](https://modelldcatnotordf.readthedocs.io/)\n\n\nA small Python library for mapping a modell catalog to rdf\n\nThe library contains helper classes for the following modelldcat-ap-no classes:\n - [InformationModel](https://informasjonsforvaltning.github.io/modelldcat-ap-no/#klasse-informasjonsmodell)\n\n The library will map to [the Norwegian Application Profile](https://informasjonsforvaltning.github.io/modelldcat-ap-no/).\n\n## Usage\n### Install\n```\n% pip install modelldcatnotordf\n```\n### Getting started\n```\nfrom datacatalogtordf import Catalog\nfrom modelldcatnotordf import InformationModel\n\n# Create catalog object\ncatalog = Catalog()\ncatalog.identifier = "http://example.com/catalogs/1"\ncatalog.title = {"en": "A model catalog"}\ncatalog.publisher = "https://example.com/publishers/1"\n\n# Create a model:\nmodel = InformationModel()\nmodel.identifier = "http://example.com/models/1"\nmodel.description = {"nb": "En adressemodell"}\n# ... and further attributes ...\n#\n# Add model to catalog:\ncatalog.model.append(model)\n\n# get rdf representation in turtle (default)\nrdf = catalog.to_rdf()\nprint(rdf.decode())\n```\n## Development\n### Requirements\n- python3\n- [pyenv](https://github.com/pyenv/pyenv)\n- [pipx] (https://github.com/pipxproject/pipx)\n- [poetry](https://python-poetry.org/)\n- [nox](https://nox.thea.codes/en/stable/)\n\n```\n% pipx install poetry==1.0.5\n% pipx install nox==2019.11.9\n```\n### Install\n```\n% git clone https://github.com/Informasjonsforvaltning/modelldcatnotordf.git\n% cd modelldcatnotordf\n% pyenv install 3.8.6\n% pyenv install 3.7.9\n% pyenv local 3.8.6 3.7.9\n% poetry install\n```\n### Run all sessions\n```\n% nox\n```\n### Run all tests with coverage reporting\n```\n% nox -rs tests\n```\n### Debugging\nYou can enter into [Pdb](https://docs.python.org/3/library/pdb.html) by passing `--pdb` to pytest:\n```\nnox -rs tests -- --pdb\n```\nYou can set breakpoints directly in code by using the function `breakpoint()`.\n',
    'author': 'Stig B. Dørmænen',
    'author_email': 'stigbd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Informasjonsforvaltning/modelldcatnotordf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
