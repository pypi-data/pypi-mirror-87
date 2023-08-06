# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['catmeow']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'setuptools>=50.3.2,<51.0.0']

entry_points = \
{'console_scripts': ['catmeow = catmeow:main']}

setup_kwargs = {
    'name': 'catmeow',
    'version': '0.2.2',
    'description': 'Simple CLI-application demostrating packaging and distibution',
    'long_description': '# Catmeow simple python package\n\nThis repo serves as an instruction on how to publish packaged to PyPI\n\n## Steps\n\n### configuring env\nIf you want to avoid entering your username, you can configure TestPyPI in your `$HOME/.pypirc`:\n\n```\n[testpypi]\nusername = <USER>\npassword = <PASS>\n```\n\n### build\n`python -m pep517.build .`\n\n### upload to test pypi\n`twine upload --repository testpypi dist/*`\n\n### download from test pypi\n`pip install --index-url https://test.pypi.org/simple/ catmeow`\n\n### uninstall\n`pip uninstall catmeow`\n\n## References\n[Instruction @medium](https://zjor.medium.com/packaging-a-runnable-python-module-de43ac12148)\n',
    'author': 'Sergey Royz',
    'author_email': 'zjor.se@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zjor/catmeow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
