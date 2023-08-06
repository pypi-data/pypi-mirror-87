# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['liquid', 'liquid.python', 'liquid.python.tags', 'liquid.tags']

package_data = \
{'': ['*']}

install_requires = \
['diot', 'lark-parser<1.0.0', 'rich>=9.0.0,<10.0.0']

setup_kwargs = {
    'name': 'liquidpy',
    'version': '0.6.3',
    'description': 'A port of liquid template engine for python',
    'long_description': "# liquidpy\nA port of [liquid][1] template engine for python\n\n[![Pypi][2]][9] [![Github][3]][10] [![PythonVers][4]][9] [![Codacy][6]][12] [![Codacy coverage][7]][12] ![Docs building][13] ![Building][5]\n\nThis is compatible with [standard Liquid][1] template engine. Variations, such as Shopify and Jekyll are not fully supported yet.\n\n## Install\n```shell\npip install -U liquidpy\n```\n\n## Baisic usage\n```python\nfrom liquid import Liquid\nliq = Liquid('{{a}}')\nret = liq.render(a=1)\n# ret == '1'\n\n# with environments pre-loaded\nliq = Liquid('{{a}}', a=1)\nret = liq.render()\n# ret == '1'\n\n# With debug on:\nliq = Liquid('{{a}}', liquid_config={'debug': True})\n```\n\n## Python mode\n\nWe also support a python mode template engine, which acts more pythonic and powerful.\n```python\nfrom liquid import Liquid\n# standard liquid doesn't support this\nliq = Liquid('{{a + 1}}', {'mode': 'python'})\nret = liq.render(a=1)\n# ret == '2'\n```\n\nBoth modes can accept a path, a file-like object or a stream for the template:\n```python\nLiquid('/path/to/template')\n# or\nwith open('/path/to/template') as f:\n    Liquid(f)\n```\n\n## Full Documentation\n- Liquid's [documentation][1]\n- Liquidpy's [documentation][14]\n\n## Backward compatiblility warning\n\n`v0.6.0+` is a remodeled version to make it compatible with standard liquid engine. If you are using a previous version, stick with it. `0.6.0+` is not fully compatible with previous versions.\n\n[1]: https://shopify.github.io/liquid/\n[2]: https://img.shields.io/pypi/v/liquidpy.svg?style=flat-square\n[3]: https://img.shields.io/github/tag/pwwang/liquidpy.svg?style=flat-square\n[4]: https://img.shields.io/pypi/pyversions/liquidpy.svg?style=flat-square\n[5]: https://img.shields.io/github/workflow/status/pwwang/liquidpy/Build%20and%20Deploy?style=flat-square\n[6]: https://img.shields.io/codacy/grade/aed04c099cbe42dabda2b42bae557fa4?style=flat-square\n[7]: https://img.shields.io/codacy/coverage/aed04c099cbe42dabda2b42bae557fa4?style=flat-square\n[8]: https://liquidpy.readthedocs.io/en/latest/\n[9]: https://pypi.org/project/liquidpy/\n[10]: https://github.com/pwwang/liquidpy\n[12]: https://app.codacy.com/manual/pwwang/liquidpy/dashboard\n[13]: https://img.shields.io/github/workflow/status/pwwang/liquidpy/Build%20Docs?label=docs&style=flat-square\n[14]: https://pwwang.github.io/liquidpy/\n",
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/liquidpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
