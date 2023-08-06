# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['firedantic', 'firedantic.tests']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-firestore>=1.9.0,<2.0.0',
 'grpcio>=1.32.0,<2.0.0',
 'pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'firedantic',
    'version': '0.1.4',
    'description': 'Pydantic base model for Firestore',
    'long_description': '# Firedantic\n\n[![Build Status](https://travis-ci.org/digitalliving/firedantic.svg?branch=master)](https://travis-ci.org/digitalliving/firedantic)\n\nDatabase models for Firestore using Pydantic base models.\n\n\n## Installation\n\nThe package is available on PyPi:\n\n```bash\npip install firedantic\n```\n\n\n## Usage\n\nIn your application you will need to configure the firestore db client and\noptionally the collection prefix, which by default is empty.\n\n```python\nfrom mock import Mock\nfrom os import environ\n\nimport google.auth.credentials\nfrom firedantic import configure\nfrom google.cloud import firestore\n\n# Firestore emulator must be running if using locally.\nif environ.get("FIRESTORE_EMULATOR_HOST"):\n    client = firestore.Client(\n        project="firedantic-test",\n        credentials=Mock(spec=google.auth.credentials.Credentials)\n    )\nelse:\n    client = firestore.Client()\n\nconfigure(client, prefix="firedantic-test-")\n```\n\nOnce that is done, you can start defining your Pydantic models, e.g:\n\n```python\nfrom pydantic import BaseModel\n\nfrom firedantic import Model\n\nclass Owner(BaseModel):\n    """Dummy owner Pydantic model."""\n    first_name: str\n    last_name: str\n\n\nclass Company(Model):\n    """Dummy company Firedantic model."""\n    __collection__ = "companies"\n    company_id: str\n    owner: Owner\n\n# Now you can use the model to save it to Firestore\nowner = Owner(first_name="John", last_name="Doe")\ncompany = Company(company_id="1234567-8", owner=owner)\ncompany.save()\n\n# Prints out the firestore ID of the Company model\nprint(company.id)\n```\n\nQuerying is done via a MongoDB-like `find()`:\n\n```python\nfrom firedantic import Model\n\nclass Product(Model):\n    __collection__ = "products"\n    product_id: str\n    stock: int\n\nProduct.find({"product_id": "abc-123"})\nProduct.find({"stock": {">=": 3}})\n```\n\nThe query operators are found at [https://firebase.google.com/docs/firestore/query-data/queries#query_operators](https://firebase.google.com/docs/firestore/query-data/queries#query_operators).\n\n\n## Development\n\nPRs are welcome!\n\n\n\nTo run tests locally, you should run:\n\n```bash\npoetry install\npoetry run invoke test\n# or\npoetry run py test\n```\n\n\n## License\n\nThis code is released under the BSD 3-Clause license. Details in the\n[LICENSE](./LICENSE) file.\n',
    'author': 'Digital Living International Ltd',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/digitalliving/firedantic',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
