# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdfmate']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0', 'asgiref>=3.3.0,<4.0.0', 'pyppeteer>=0.2.2,<0.3.0']

entry_points = \
{'console_scripts': ['pdfmate-setup = pdfmate.setup:main']}

setup_kwargs = {
    'name': 'pdfmate',
    'version': '0.4.9',
    'description': 'Pyppeteer-based async python wrapper to convert html to pdf',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/pdfmate)](https://pypi.python.org/pypi/pdfmate)\n[![PyPI version](https://img.shields.io/pypi/pyversions/pdfmate)](https://pypi.python.org/pypi/pdfmate)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# PDFMate\n\nAsync / sync wrapper for Pyppeteer\n\n### Install\n\n    pip install pdfmate\n\n# Usage\n\nFor simple async tasks:\n\n```python\nimport pdfmate\n\nasync def f():\n    await pdfmate.from_url(\'http://google.com\', \'out.pdf\')\n    await pdfmate.from_file(\'test.html\', \'out.pdf\')\n    await pdfmate.from_string(\'Hello!\', \'out.pdf\')\n```\n\nSync API is also provided at `pdfmate.sync` for all the above-mentioned functions:\n\n```python\nimport pdfmate\n\npdfmate.sync.from_url(\'http://google.com\', \'out.pdf\')\npdfmate.sync.from_file(\'test.html\', \'out.pdf\')\npdfmate.sync.from_string(\'Hello!\', \'out.pdf\')\n```\n\nYou can pass a list with multiple URLs or files:\n\n```python\npdfmate.sync.from_url([\'google.com\', \'yandex.ru\', \'engadget.com\'], \'out.pdf\')\npdfmate.sync.from_file([\'file1.html\', \'file2.html\'], \'out.pdf\')\n```\n\nAlso you can pass an opened file:\n\n```python\nwith open(\'file.html\') as f:\n    pdfmate.sync.pdfmate(f, \'out.pdf\')\n```\n\nIf you wish to further process generated PDF, you can read it to a\nvariable:\n\n```python\n# Ignore output_path parameter to save pdf to a variable\npdf = pdfmate.sync.from_url(\'http://google.com\')\n```\n\nYou can specify all [Pyppeteer\noptions](https://pyppeteer.github.io/pyppeteer/reference.html#pyppeteer.page.Page.pdf) used for saving PDF as shown below:\n\n```python\noptions = {\n    \'scale\': 2.0,\n    \'format\': \'Letter\',\n    \'margin\': {\n        \'top\': \'0.75in\',\n        \'right\': \'0.75in\',\n        \'bottom\': \'0.75in\',\n        \'left\': \'0.75in\',\n    },\n    \'pageRanges\': \'1-5,8\',\n}\n\npdfmate.sync.from_url(\'http://google.com\', \'out.pdf\', options=options)\n```\n\nYou can also pass any options through meta tags in your HTML:\n\n```python\nbody = """\n    <html>\n      <head>\n        <meta name="pdfmate-format" content="Legal"/>\n        <meta name="pdfmate-landscape" content="False"/>\n      </head>\n      Hello World!\n      </html>\n    """\n\npdfmate.sync.from_string(body, \'out.pdf\')\n```\n\n## Configuration\n\nEach API call takes an optional options parameter to configure print PDF behavior. However, to reduce redundancy, one can certainly set default configuration to be used for all API calls. It takes the\nconfiguration options as initial paramaters. The available options are:\n\n- `options` - the dict used by default for pyppeteer `page.pdf(options)` call. `options` passed as argument to API call will take precedence over the default options.\n- `meta_tag_prefix` - the prefix for `pdfmate` specific meta tags - by\n  default this is `pdfmate-`.\n- `environ` - the dict used to provide env variables to pyppeteer headless browser.\n\n```python\nimport pdfmate\n\npdfmate.configuration(options={\'format\': \'A4\'})\n\nasync def f():\n    # The resultant PDF at \'output_file\' will be in A4 size and 2.0 scale.\n    await pdfmate.from_string(html_string, output_file, options={\'scale\': 2.0})\n```\n\n### Setup for development\n\n    poetry install -v --no-root\n\n### Run tests\n\n    poetry run pytest tests/\n\n### Enable git-hooks with lint-staged\n\n    npx mrm lint-staged\n    npx husky install\n\n#### Credits\n\nThis is adapted version of PDFGen-Python and python-PDFKit library, so big thanks to them!\n\n- [PDFGen-Python](https://pypi.org/project/pdfmate/)\n- [python-pdfkit](https://github.com/JazzCore/python-pdfkit/)\n- [Pyppeteer](https://pypi.org/project/pyppeteer/)\n\n### Other projects\n\n- [django-pdf-reactor](https://github.com/terminalkitten/django-pdf-reactor/)\n\n### Is it any good?\n\n[Yes.](http://news.ycombinator.com/item?id=3067434)\n',
    'author': 'TK',
    'author_email': 'dk@terminalkitten.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/terminalkitten',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
