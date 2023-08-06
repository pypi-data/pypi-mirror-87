# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensourcetest_test_test',
 'opensourcetest_test_test.builtin',
 'opensourcetest_test_test.common',
 'opensourcetest_test_test.httpmodel',
 'opensourcetest_test_test.httpmodel.Base',
 'opensourcetest_test_test.httpmodel.Common',
 'opensourcetest_test_test.httpmodel.Common.FileOption',
 'opensourcetest_test_test.httpmodel.Common.StringOption',
 'opensourcetest_test_test.httpmodel.Parameter',
 'opensourcetest_test_test.httpmodel.TestCases',
 'opensourcetest_test_test.uimodel',
 'opensourcetest_test_test.uimodel.Base',
 'opensourcetest_test_test.uimodel.Common',
 'opensourcetest_test_test.uimodel.Conf',
 'opensourcetest_test_test.uimodel.Logs',
 'opensourcetest_test_test.uimodel.PageObject',
 'opensourcetest_test_test.uimodel.PageObject.Login_page',
 'opensourcetest_test_test.uimodel.PageObject.Register_page',
 'opensourcetest_test_test.uimodel.TestCases',
 'opensourcetest_test_test.uimodel.TestCases.Login',
 'opensourcetest_test_test.uimodel.TestCases.Register']

package_data = \
{'': ['*'],
 'opensourcetest_test_test': ['banner/*'],
 'opensourcetest_test_test.httpmodel': ['Conf/*', 'Parameter/Login/*'],
 'opensourcetest_test_test.uimodel': ['LocalSeleniumServer/*',
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
 'selenium>=3.141.0,<4.0.0',
 'xlrd>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['OST = opensourcetest_test_test.cli:main',
                     'opensourcetest_test_test = '
                     'opensourcetest_test_test.cli:main']}

setup_kwargs = {
    'name': 'opensourcetest-test-test',
    'version': '0.3.2',
    'description': 'We need more free software interface testing.',
    'long_description': '# OpenSourceTest\n夜行者社区接口自动化项目，提供的是更多地灵活性和可配置性\n',
    'author': 'chineseluo',
    'author_email': '848257135@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chineseluo/opensourcetest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.2,<4.0.0',
}


setup(**setup_kwargs)
