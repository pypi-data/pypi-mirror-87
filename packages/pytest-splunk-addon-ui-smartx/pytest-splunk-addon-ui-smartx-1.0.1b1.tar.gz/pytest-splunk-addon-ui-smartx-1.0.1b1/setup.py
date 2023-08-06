# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_splunk_addon_ui_smartx',
 'pytest_splunk_addon_ui_smartx.alert_actions',
 'pytest_splunk_addon_ui_smartx.alert_actions.components',
 'pytest_splunk_addon_ui_smartx.components',
 'pytest_splunk_addon_ui_smartx.components.controls',
 'pytest_splunk_addon_ui_smartx.pages']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx',
 'configparser',
 'future',
 'msedge-selenium-tools',
 'pytest-html',
 'pytest-splunk-addon==1.3.6',
 'selenium',
 'sphinx-panels',
 'sphinx_rtd_theme',
 'urllib3==1.21.1',
 'webdriver-manager']

extras_require = \
{'docker': ['lovely-pytest-docker>=0.1.0']}

entry_points = \
{'pytest11': ['ucc-smartx = pytest_splunk_addon_ui_smartx.plugin']}

setup_kwargs = {
    'name': 'pytest-splunk-addon-ui-smartx',
    'version': '1.0.1b1',
    'description': 'Library to support testing Splunk Add-on UX',
    'long_description': None,
    'author': 'rfaircloth-splunk',
    'author_email': 'rfaircloth@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
