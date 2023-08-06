# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygrammalecte']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20.0,<3.0.0']

setup_kwargs = {
    'name': 'pygrammalecte',
    'version': '1.2.0',
    'description': 'Grammalecte, le correcteur grammatical en Python',
    'long_description': '# pygrammalecte\n\n[![PyPI](https://img.shields.io/pypi/v/pygrammalecte.svg)](https://pypi.python.org/pypi/pygrammalecte)\n[![PyPI](https://img.shields.io/pypi/l/pygrammalecte.svg)](https://github.com/vpoulailleau/pygrammalecte/blob/master/LICENSE)\n[![Travis](https://api.travis-ci.com/vpoulailleau/pygrammalecte.svg?branch=master)](https://travis-ci.com/vpoulailleau/pygrammalecte)\n[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Downloads](https://pepy.tech/badge/pygrammalecte)](https://pepy.tech/project/pygrammalecte)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/44347ade656fa1e652ae/test_coverage)](https://codeclimate.com/github/vpoulailleau/pygrammalecte/test_coverage)\n[![Maintainability](https://api.codeclimate.com/v1/badges/44347ade656fa1e652ae/maintainability)](https://codeclimate.com/github/vpoulailleau/pygrammalecte/maintainability)\n\n(english version at the bottom of this document)\n\nGrammalecte, le correcteur grammatical en Python.\n\nPour être précis, ce projet n’est pas Grammalecte, mais un «\xa0wrapper\xa0» permettant de l’utiliser facilement en Python.\n\n## Installation\n\nVous devez utiliser un Python en version supérieure ou égale à 3.7.\n\nL’utilisation d’un environnement virtuel est fortement recommandé.\n\n```sh\npython3 -m pip install pygrammalecte\n```\n\n## Utilisation\n\n### Vérification d’une chaîne de caractères\n\n```python\nfrom pygrammalecte import grammalecte_text\n\ntexte_bidon = """\\\nCoucou, je veut du fromage.\nJe sais coder en VHDL.\nLe VHDL est est compliquer.\n"""\n\nfor message in grammalecte_text(texte_bidon):\n    print(message)\n```\n\n### Vérification d’un fichier\n\nVous devez fournir le chemin du fichier en `str` ou en `pathlib.Path`. Le fichier doit être un fichier texte brut (pas un fichier Word ou OpenDocument par exemple).\n\n```python\nfrom pathlib import Path\n\nfrom pygrammalecte import grammalecte_file\n\nfilepath = Path("toto.txt")\n\nfor message in grammalecte_file(filepath):\n    print(message)\n```\n\n### Messages générés\n\nLes fonctions `grammalecte_file` et `grammalecte_text` sont des générateurs, vous pouvez donc les utiliser dans une boucle `for`. Elles génèrent des `GrammalecteMessage`.\n\nDeux types de `GrammalecteMessage` existent\xa0:\n\n- `GrammalecteSpellingMessage` qui a comme attributs\xa0:\n\n  - `line`\xa0: numéro de la ligne dans le texte vérifié\n  - `start`\xa0: numéro du caractère de début de l’erreur dans la ligne\n  - `end`\xa0: numéro du caractère de fin de l’erreur dans la ligne\n  - `word`\xa0: le mot non reconnu par `Grammalecte`\n  - `message`\xa0: message d’erreur\n\n- `GrammalecteGrammarMessage` qui a comme attributs\xa0:\n  - `line`\xa0: numéro de la ligne dans le texte vérifié\n  - `start`\xa0: numéro du caractère de début de l’erreur dans la ligne\n  - `end`\xa0: numéro du caractère de fin de l’erreur dans la ligne\n  - `url`\xa0: l’URL fournie par `Grammalecte`\n  - `color`\xa0: une couleur fournie par `Grammalecte`, c’est une liste de 3 entiers entre 0 et 255.\n  - `suggestions`\xa0: propositions de correction\n  - `message`\xa0: message d’erreur\n  - `rule`\xa0: identifiant de la règle violée\n  - `type`\xa0: type de la règle (`"conj"`…)\n\n## Changelog\n\n### Version v1.2.0\n\n- Utilisation de Grammalecte v1.12.0\n\n### Version v1.1.0\n\n- Ajout de l\'attribut `message` pour `GrammalecteSpellingMessage`\n\n### Version v1.0.0\n\n- Refactoring\n- Ajout de l\'intégration continue\n\n### Version v0.1.0\n\n- Première version\xa0!\n- Utilisation de Grammalecte v1.11.0\n\n## English version\n\nThis is a wrapper for the french grammatical checker called Grammalecte.\n',
    'author': 'Vincent Poulailleau',
    'author_email': 'vpoulailleau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vpoulailleau/pygrammalecte',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
