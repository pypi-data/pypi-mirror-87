# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_test', 'nonebot_plugin_test.drivers']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.5.0,<0.6.0',
 'nonebot2>=2.0.0-alpha.6,<3.0.0',
 'python-socketio>=4.6.0,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-test',
    'version': '0.1.0',
    'description': 'Test frontend for nonebot v2+',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# NoneBot Plugin Test\n\n_✨ 在浏览器中测试你的 NoneBot 机器人 ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/nonebot/plugin-test/master/LICENSE">\n    <img src="https://img.shields.io/github/license/nonebot/plugin-test.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-test">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-test.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">\n</p>\n\n## 使用方法\n\n加载插件\n\n```python\nnonebot.load_plugin("nonebot_plugin_test")\n```\n\n在日志中将会输出测试网站地址，通常为 `http://HOST:PORT/test/`\n\n## 准备开发\n\n首先你需要安装 npm 的本地依赖：\n\n```sh\nnpm install\n```\n\n**不建议单独为此项目新建虚拟环境，直接在你原有的 nonebot 虚拟环境下使用即可。**\n\n## 进行开发\n\n使用命令启动前端页面的开发服务器，你对前端页面的任何修改都可以预览：\n\n```sh\nnpm run serve\n```\n\n这时候的页面连接不到 `nonebot2` 的实例，所以只能进行页面的开发。\n\n下面介绍一下如何连接到已有的 `nonebot2` 项目上。\n\n由于开启了 [`devServer`](https://cli.vuejs.org/zh/config/#devserver) 中的 `writeToDisk` 选项， `webpack-dev-server` 会将每次编译产生的文件写入 `./nonebot_plugin_test/dist` 文件夹。\n\n打开你的 bot 源码目录以及虚拟环境，将原来已经安装的 `nonebot-test` 包移除掉：\n\n```sh\npip uninstall nonebot-test\n```\n\n将 bot 的依赖改为本地依赖：\n\n```diff\n- nonebot-test = { version = "^0.1.0", optional = true }\n+ nonebot-test = { path = "relative/path/to/nonebot-test/", develop = true }\n```\n\n然后使用 poetry 重新安装依赖即可：\n\n```sh\npoetry update\npoetry install\n```\n\n现在启动你的 bot，本地`nonebot-test` 包就可以开始工作了，打开 `localhost:2333` （**不需要打开前面所述的前端开发服务器:8080**）就可以查看实时最新的前端页面了。\n\n```sh\npython bot.py\n```\n',
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://v2.nonebot.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
