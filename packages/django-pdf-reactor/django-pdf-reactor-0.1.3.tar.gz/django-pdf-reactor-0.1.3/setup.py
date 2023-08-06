# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdf_reactor']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1,<4.0',
 'channels-redis>=3.0.1,<4.0.0',
 'channels>=2.4.0,<3.0.0',
 'django-channels-graphql-ws>=0.7.4,<0.8.0',
 'nanoid>=2.0.0,<3.0.0',
 'nest_asyncio>=1.4.3,<2.0.0',
 'pdfmate>=0.4.9,<0.5.0',
 'pdoc>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'django-pdf-reactor',
    'version': '0.1.3',
    'description': 'PDF generator for Django, support for async generation in Django Channels worker or with Django 3.1 async views.',
    'long_description': "[![PyPI](https://img.shields.io/pypi/v/django-pdf-reactor)](https://pypi.python.org/pypi/pdfmate)\n[![PyPI version](https://img.shields.io/pypi/pyversions/django-pdf-reactor)](https://pypi.python.org/pypi/pdfmate)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## What is Django PDF Reactor?\n\nUse PDFGen wrapper for Pyppeteer to create PDF files in Django. Support for async generation in Django Channels worker or with Django 3.1 async views.\n\n### Channels\n\nMore about generating PDF in channels with Websocket support.\n\n### Async view\n\nMore about generating PDF in async view\n\n### Stunnel Support\n\nChromium will not visit https://localhost:8000, so run\n\n    brew install stunnel\n\nAdd ssl_proxy file\n\n    pid=\n    cert=/usr/local/etc/stunnel/stunnel.pem\n    foreground=yes\n    debug=7\n\n    [https]\n    accept=8000\n    connect=8001\n    TIMEOUTclose=1\n\nStart\n\n    sudo stunnel ssl_proxy\n\n### Support for PDF/A\n\nFor MacOSX:\n\n     brew install poppler ghostscript\n\nFor Ubuntu / Debian:\n\n     apt-get install poppler ghostscript\n\nA PDF/A document is just a PDF document that uses a specific subset of PDF that is designed to ensure it is 'self-contained'. It's not permitted to be reliant on information from external sources (e.g. font programs and hyperlinks).\n\nFrom wikipedia:\n\nOther key elements to PDF/A compatibility include:\n\n- Audio and video content are forbidden.\n- JavaScript and executable file launches are forbidden.\n- All fonts must be embedded and also must be legally embeddable for\n  unlimited, universal rendering. This also applies to the so-called  \n  PostScript standard fonts such as Times or Helvetica.\n- Colorspaces specified in a device-independent manner.\n- Encryption is disallowed.\n- Use of standards-based metadata is mandated.\n\n### Is it any good?\n\n[Yes.](http://news.ycombinator.com/item?id=3067434)\n\n#### Credits\n\n- [PDFGen-Python](https://pypi.org/project/pdfgen/)\n- [Pyppeteer](https://pypi.org/project/pyppeteer/)\n",
    'author': 'TK',
    'author_email': 'dk@terminalkitten.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/terminalkitten/django-pdf-reactor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
