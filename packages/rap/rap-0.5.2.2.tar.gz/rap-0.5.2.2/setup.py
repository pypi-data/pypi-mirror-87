# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rap',
 'rap.common',
 'rap.manager',
 'rap.middleware',
 'rap.middleware.conn',
 'rap.middleware.msg',
 'rap.middleware.request',
 'rap.server']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.0,<2.0.0', 'pycrypto==2.6.1']

setup_kwargs = {
    'name': 'rap',
    'version': '0.5.2.2',
    'description': 'rap(par[::-1]) is a simple and fast python async rpc',
    'long_description': '# rap\nrap(par[::-1]) is advanced and fast python async rpc\n\n> Inspired by the sky [aiorpc](https://github.com/choleraehyq/aiorpc)\n# Installation\n```Bash\npip install rap\n```\n\n# Usage\n\n## Server\n```Python\nimport asyncio\n\nfrom rap.server import Server\n\n\ndef sync_sum(a: int, b: int):\n    return a + b\n\n\nasync def mock_io(a: int, b: int):\n    await asyncio.sleep(1)  # mock io time\n    return a + b\n\n\nasync def async_gen(a):\n    for i in range(a):\n        yield i\n\n\nloop = asyncio.new_event_loop()\nrpc_server = Server()\nrpc_server.register(sync_sum)\nrpc_server.register(mock_io)\nrpc_server.register(async_gen)\nserver = loop.run_until_complete(rpc_server.create_server())\n\ntry:\n    loop.run_forever()\nexcept KeyboardInterrupt:\n    server.close()\n    loop.run_until_complete(server.wait_closed())\n```\n\n## Client\nFor the client, there is no difference between `async def` and `def`. In fact, `rap` is still called by the method of `call_by_text`. Using `async def` can be decorated by `client.register` and can also be written with the help of IDE Correct code\n```Python\nimport asyncio\n\nfrom rap.client import Client\n\n\nclient = Client()\n\n\ndef sync_sum(a: int, b: int) -> int:\n    pass\n\n# in register, must use async def...\n@client.register\nasync def mock_io(a: int, b: int) -> int:\n    pass\n\n\n# in register, must use async def...\n@client.register\nasync def async_gen(a: int):\n    yield\n\n\nasync def main():\n    await client.connect()\n    print(f"sync result: {await client.call(sync_sum, 1, 2)}")\n    print(f"sync result: {await client.raw_call(\'sync_sum\', 1, 2)}")\n    print(f"async result: {await mock_io(1, 3)}")\n    async for i in async_gen(10):\n        print(f"async gen result:{i}")\n    await client.wait_close()\n\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```',
    'author': 'So1n',
    'author_email': 'so1n897046026@gamil.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/so1n/rap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
