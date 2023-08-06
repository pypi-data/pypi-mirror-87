# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scikeras', 'scikeras.utils']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn>=0.22.0', 'tensorflow>=2.2.0']

setup_kwargs = {
    'name': 'scikeras',
    'version': '0.2.1',
    'description': 'Scikit-Learn API wrapper for Keras.',
    'long_description': '# Scikit-Learn Wrapper for Keras\n\n[![Build Status](https://github.com/adriangb/scikeras/workflows/Tests/badge.svg)](https://github.com/adriangb/scikeras/actions?query=workflow%3ATests+branch%3Amaster)\n[![Coverage Status](https://codecov.io/gh/adriangb/scikeras/branch/master/graph/badge.svg)](https://codecov.io/gh/adriangb/scikeras)\n[![Docs Status](https://readthedocs.org/projects/docs/badge/?version=latest)](https://scikeras.readthedocs.io/en/latest/?badge=latest)\n\nScikit-Learn compatible wrappers for Keras Models.\n\n## Why SciKeras\n\nSciKeras is derived from and API compatible with `tf.keras.wrappers.scikit_learn`. The original TensorFlow (TF) wrappers are not actively mantained,\nand [may be deprecated](https://github.com/tensorflow/tensorflow/pull/37201#pullrequestreview-391650001) at some point.\n\nAn overview of the advantages and differences as compared to the TF wrappers can be found in our\n[migration](https://scikeras.readthedocs.io/en/latest/migration.html) guide.\n\n## Installation\n\nThis package is available on PyPi:\n\n```bash\npip install scikeras\n```\n\nThe only dependencies are `scikit-learn>=0.22` and `TensorFlow>=2.2.0`.\n\n### Migrating from `tf.keras.wrappers.scikit_learn`\n\nPlease see the [migration](https://scikeras.readthedocs.io/en/latest/migration.html) section of our documentation.\n\n## Documentation\n\nDocumentation is available on [ReadTheDocs](https://scikeras.readthedocs.io/en/latest/).\n\n## Contributing\n\nSee [CONTRIBUTING.md](https://github.com/adriangb/scikeras/blob/master/CONTRIBUTING.md)\n',
    'author': 'Adrian Garcia Badaracco',
    'author_email': '1755071+adriangb@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adriangb/scikeras',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.7,<3.9',
}


setup(**setup_kwargs)
