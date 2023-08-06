# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinxawesome_theme']

package_data = \
{'': ['*'], 'sphinxawesome_theme': ['static/*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'sphinx>3',
 'sphinxawesome-sampdirective>=1.0.3,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.1,<3.0.0']}

entry_points = \
{'sphinx.html_themes': ['sphinxawesome_theme = sphinxawesome_theme']}

setup_kwargs = {
    'name': 'sphinxawesome-theme',
    'version': '1.18.0',
    'description': 'An awesome theme for the Sphinx documentation generator',
    'long_description': '====================\nSphinx awesome theme\n====================\n\n.. image:: https://img.shields.io/pypi/l/sphinxawesome-theme?color=blue\n   :target: https://opensource.org/licenses/MIT\n   :alt: MIT license\n\n.. image:: https://img.shields.io/pypi/v/sphinxawesome-theme\n   :target: https://pypi.org/project/sphinxawesome-theme\n   :alt: PyPI package version number\n\n.. image:: https://api.netlify.com/api/v1/badges/e6d20a5c-b49e-4ebc-80f6-59fde8f24e22/deploy-status\n   :target: https://app.netlify.com/sites/sphinxawesome-theme/deploys\n   :alt: Netlify Status\n\n\nThis is an awesome theme and a set of extensions\nfor the Sphinx_ documentation generator.\nSee how the theme looks on the `demo page`_.\n\n.. _Sphinx: http://www.sphinx-doc.org/en/master/\n.. _demo page: https://sphinxawesome.xyz\n\n\n--------\nFeatures\n--------\n\nThis theme is designed with readability and usability in mind.\nThe theme includes several extensions that enhance the usability:\n\n.. features-start\n\nAwesome code blocks\n    - Code blocks have a header section, displaying the optional caption,\n      as well as the programming language used for syntax highlighting\n    - The code block headers contain a **Copy** button, allowing you to copy\n      code snippets to the clipboard.\n    - The theme adds two new options to Sphinx\'s ``code-block`` directive:\n      ``emphasize-added`` and ``emphasize-removed``, allowing you to highlight\n      code changes within other highlighted code.\n\nAwesome new directive for highlighting placeholder variables\n    The theme supports a new directive ``samp``, which is the equivalent of the\n    built-in ``:samp:`` interpreted text role. This allows you to highlight placeholder\n    variables in code blocks.\n\nAwesome user experience improvements\n    These small features make the theme more usable. To name a few:\n\n    - Use the **Tab** key to navigate through all sections of the page. Every page has a\n      *Skip to Content* link to bypass navigation links.\n    - Link to notes, warnings, etc. Their titles have IDs and use the same “permalink”\n      mechanism as headings and other captions.\n    - Better “permalink” mechanism. Hovering over an element with a permalink reveals a\n      *Link* icon. Select the *Link* icon to copy the link to the clipboard.\n    - Collapsible navigation menu: all pages are reachable from all other pages.\n    - Collapsible code definitions: API documentation from docstrings using the\n      ``sphinx.ext.autodoc`` extension is collapsible for a better overview.\n    - CSS tooltips. Provide more accessible information compared to the ``title``\n      attribute which only works with a mouse.\n    - Press the ``/`` (Slash) key to focus the search input and start searching.\n\n.. features-end\n\n------------\nInstallation\n------------\n\nInstall the theme as a Python package:\n\n.. install-start\n\n.. code:: console\n\n   $ pip install sphinxawesome-theme\n\n.. install-end\n\nRead the full `installation instructions`_ for more information.\n\n.. _installation instructions: https://sphinxawesome.xyz/docs/install/#how-to-install-the-theme\n\n-----\nUsage\n-----\n\n.. use-start\n\nTo use the theme, set the ``html_theme`` configuration setting\nin the Sphinx configuration file ``conf.py``:\n\n.. code:: python\n\n   html_theme = "sphinxawesome_theme"\n\n.. use-end\n\nRead the full `usage information`_ for more information.\n\n.. _usage information: https://sphinxawesome.xyz/docs/use/#how-to-use-the-theme\n',
    'author': 'Kai Welke',
    'author_email': 'kai687@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai687/sphinxawesome-theme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
