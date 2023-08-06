# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chaine']

package_data = \
{'': ['*'],
 'chaine': ['crfsuite/*',
            'crfsuite/include/*',
            'crfsuite/lib/cqdb/*',
            'crfsuite/lib/cqdb/include/*',
            'crfsuite/lib/cqdb/src/*',
            'crfsuite/lib/crf/src/*',
            'crfsuite/swig/*',
            'liblbfgs/*',
            'liblbfgs/include/*',
            'liblbfgs/lib/*']}

setup_kwargs = {
    'name': 'chaine',
    'version': '0.2.0',
    'description': 'A Lightweight Conditional Random Field',
    'long_description': '# A Lightweight Conditional Random Field\n\nThis is a modern Python library without any third-party dependencies and a backend written in C implementing conditional random fields for natural language processing tasks like named entity recognition or part-of-speech tagging.\n\nYou can install the latest stable version from [PyPI](https://pypi.org/project/chaine):\n\n```\n$ pip install chaine\n```\n\nIf you are interested in the theoretical concepts behind conditional random fields, I can recommend the introducing paper by [Lafferty et al](https://repository.upenn.edu/cgi/viewcontent.cgi?article=1162&context=cis_papers).\n\n\n## Example\n\n```python\n>>> import chaine\n>>> sequences = [[["a", "a"], ["b", "b"]]]\n>>> labels = [["0", "1"]]\n>>> model = chaine.train(sequences, labels)\n>>> model.predict(sequences)\n[[\'0\', \'1\']]\n```\n\nCheck out the introducing [Jupyter notebook](https://github.com/severinsimmler/chaine/blob/master/notebooks/tutorial.ipynb).\n\n\n## Credits\n\nThis library makes use of and is partially based on:\n\n- [CRFsuite](https://github.com/chokkan/crfsuite)\n- [libLBFGS](https://github.com/chokkan/liblbfgs)\n- [python-crfsuite](https://github.com/scrapinghub/python-crfsuite)\n- [sklearn-crfsuite](https://github.com/TeamHG-Memex/sklearn-crfsuite)\n',
    'author': 'Severin Simmler',
    'author_email': 'severin.simmler@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
