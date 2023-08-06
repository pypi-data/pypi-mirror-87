# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensourcetest',
 'opensourcetest.builtin',
 'opensourcetest.common',
 'opensourcetest.httpmodel',
 'opensourcetest.httpmodel.Base',
 'opensourcetest.httpmodel.Common',
 'opensourcetest.httpmodel.Common.FileOption',
 'opensourcetest.httpmodel.Common.StringOption',
 'opensourcetest.httpmodel.Parameter',
 'opensourcetest.httpmodel.TestCases',
 'opensourcetest.uimodel',
 'opensourcetest.uimodel.Base',
 'opensourcetest.uimodel.Common',
 'opensourcetest.uimodel.Conf',
 'opensourcetest.uimodel.Logs',
 'opensourcetest.uimodel.PageObject',
 'opensourcetest.uimodel.PageObject.Login_page',
 'opensourcetest.uimodel.PageObject.Register_page',
 'opensourcetest.uimodel.TestCases',
 'opensourcetest.uimodel.TestCases.Login',
 'opensourcetest.uimodel.TestCases.Register']

package_data = \
{'': ['*'],
 'opensourcetest': ['banner/*'],
 'opensourcetest.httpmodel': ['Conf/*', 'Parameter/Login/*'],
 'opensourcetest.uimodel': ['LocalSeleniumServer/*',
                            'LocalSeleniumServer/selenium_run_script/*',
                            'LocalSeleniumServer/selenium_server_jar/*',
                            'LocalSeleniumServer/selenium_server_script/*']}

install_requires = \
['PyYAML>=5.1.2,<6.0.0',
 'allure-pytest>=2.8.19,<3.0.0',
 'docker>=4.4.0,<5.0.0',
 'jmespath>=0.9.5,<0.10.0',
 'loguru>=0.5.3,<0.6.0',
 'mkdocs-material>=6.0.2,<7.0.0',
 'mkdocs>=1.1.2,<2.0.0',
 'pydantic>=1.4,<2.0',
 'pytest-html>=2.1.1,<3.0.0',
 'pytest>=5.2,<6.0',
 'requests>=2.22.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0']

entry_points = \
{'console_scripts': ['OST = opensourcetest.cli:main',
                     'Opensourcetest = opensourcetest.cli:main',
                     'Ost = opensourcetest.cli:main',
                     'opensourcetest = opensourcetest.cli:main']}

setup_kwargs = {
    'name': 'opensourcetest',
    'version': '0.2.1',
    'description': 'We need more free software interface testing.',
    'long_description': '# OpenSourceTest\n\n# [![pyversions](https://img.shields.io/badge/opensourcetest-v0.2.x-brightgreen)](https://pypi.org/project/opensourcetest/)[![pyversions](https://img.shields.io/badge/pypi-v0.2.x-orange)](https://pypi.org/project/opensourcetest-test-test/)[![pyversions](https://img.shields.io/badge/pytest-5.x-green)](https://docs.pytest.org)[![pyversions](https://img.shields.io/badge/requests-2.x-green)](http://docs.python-requests.org/en/master/ )[![pyversions](https://img.shields.io/badge/allure-2.x-green)](https://docs.qameta.io/allure/  )\n\n`OpenSourceTest`将为您创建更加自由的软件接口测试，不是为了简单而简单，而是为您提供更自由的扩展的，适用于不同功能场景的`UI`自动化或接口自动化测试框架。\n\n## 设计思想\n\n- 不丢弃轮子本身的优秀特性\n- 不过度封装\n- 提供更加多的可操作对象给使用者，即时你使用基本框架已经满足需求\n- 拥抱开源\n\n## 主要特点\n\n### 支持创建`UI`自动化测试框架\n\n- 以[`yaml`][yaml]格式定义`UI`元素对象，[`yaml`][yaml]对象自动注入\n- 支持本地及远程分布式测试\n- 支持生成不同浏览器测试报告\n- 支持docker容器测试\n\n### 支持创建接口自动化测试框架\n\n- 继承 [`requests`][requests]的所有强大功能\n- 以[`yaml`][yaml]格式定义接口，[`yaml`][yaml]对象自动注入\n- 使用[`jmespath`][jmespath]提取和验证[`json`][json]响应\n\n### 其他\n\n- 完美兼容[`pytest`][pytest]，您可以使用您想使用的任何[`pytest`][pytest]格式\n- 完美兼容[`allure`][allure]，您可以使用您想使用的任何[`allure`][allure]命令\n- 支持**CLI**命令，直接创建您所需要的项目架构\n\n## 打赏支持\n\n**OpenSourceTest由作者：成都-阿木木在空闲时间维护。虽然我致力于OpenSourceTest，因为我热爱这个项目，并且每天都在日常工作中使用它，但是如果可能的话，希望可以得到打赏支持，以证明远离朋友、家人和牺牲个人时间的合理性。**\n\n\u200b\t**这些钱也将被用来维护框架，以及直播，展会等活动**\n\n\u200b\t**感谢您对OpenSourceTest计划的赞助**\n\n\u200b\t**成为打赏者[become a sponsor](docs/sponsors.md)**\n\n\u200b\t**联系作者：[成都-阿木木](mailto:848257135@qq.com)**\n\n## OpenSourceTest 社区\n\n欢迎测试小伙伴加群，讨论测试框架技术！\n\n![community](/docs/images/community.jpg)\n\n[json]: http://json.com/\n[yaml]: http://www.yaml.org/\n[requests]: http://docs.python-requests.org/en/master/\n[pytest]: https://docs.pytest.org/\n[pydantic]: https://pydantic-docs.helpmanual.io/\n[jmespath]: https://jmespath.org/\n[allure]: https://docs.qameta.io/allure/',
    'author': 'chineseluo',
    'author_email': '848257135@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chineseluo/opensourcetest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
