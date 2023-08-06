# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_docs', 'nonebot_plugin_docs.drivers']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-alpha.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-docs',
    'version': '2.0.0a7',
    'description': 'View NoneBot2 Docs Locally',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# nonebot-plugin-docs\n\n_✨ NoneBot 本地文档插件 ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/nonebot/nonebot2/master/LICENSE">\n    <img src="https://img.shields.io/github/license/nonebot/nonebot2.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-docs">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-docs.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">\n</p>\n\n## 使用方式\n\n加载插件并启动 Bot ，在浏览器内打开 `http://host:port/docs/`。\n\n具体网址会在控制台内输出。\n',
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nonebot/nonebot2/blob/master/packages/nonebot-plugin-docs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
