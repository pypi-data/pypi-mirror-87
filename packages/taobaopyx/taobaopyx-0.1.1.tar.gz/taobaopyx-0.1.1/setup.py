# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taobaopyx']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.16.1,<0.17.0']

setup_kwargs = {
    'name': 'taobaopyx',
    'version': '0.1.1',
    'description': 'Asyncio version of taobaopy',
    'long_description': '# taobaopyx\n\nAsyncio version of taobaopy powered by httpx\n\n## Install\n\n```bash\npip install -U taobaopyx\n```\n\n## Use\n\n```python\nfrom taobaopyx.taobao import APINode, AsyncTaobaoAPIClient\nimport asyncio\nimport logging\n\nlogging.basicConfig(level=logging.DEBUG)\n\n\nclient = AsyncTaobaoAPIClient(app_key="fake_key", app_secret="fake_sescret")\n\ntaobao = APINode(client, "taobao")\n\n\nasync def get():\n    res = await taobao.mixnick.get(nick="nick")\n    print(res)\n\n\nasync def shutdown():\n    await client.aclose()\n\n\nasyncio.run(get())\nasyncio.run(shutdown())\n```\n',
    'author': 'duyixian',
    'author_email': 'duyixian1234@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/duyixian1234/taobaopyx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
