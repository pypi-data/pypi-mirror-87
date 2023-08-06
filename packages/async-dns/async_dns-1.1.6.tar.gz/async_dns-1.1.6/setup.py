# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_dns',
 'async_dns.core',
 'async_dns.core.config',
 'async_dns.resolver',
 'async_dns.resolver.doh',
 'async_dns.server']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-dns',
    'version': '1.1.6',
    'description': 'Asynchronous DNS client and server',
    'long_description': "# async_dns\n\n[![PyPI](https://img.shields.io/pypi/v/async_dns.svg)]()\n\n## Features\n\n- Built with `asyncio` in pure Python, no third party dependency is required\n- Support DNS over UDP / TCP\n- Support DNS over HTTPS\n- Support DNS over TLS\n\n## Prerequisite\n\n- Python >=3.6\n\n## Installation\n\n``` sh\n$ pip3 install async_dns\n# or\n$ pip3 install git+https://github.com/gera2ld/async_dns.git\n```\n\n## CLI\n\n### Resolver\n\n```\nusage: python3 -m async_dns.resolver [-h] [-n NAMESERVERS [NAMESERVERS ...]] [-t TYPES [TYPES ...]]\n                                     hostnames [hostnames ...]\n\nAsync DNS resolver\n\npositional arguments:\n  hostnames             the hostnames to query\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -n NAMESERVERS [NAMESERVERS ...], --nameservers NAMESERVERS [NAMESERVERS ...]\n                        name servers\n  -t TYPES [TYPES ...], --types TYPES [TYPES ...]\n                        query types, default as `any`\n```\n\nExamples:\n\n``` sh\n# Resolve an IP\n$ python3 -m async_dns.resolver www.google.com\n$ python3 -m async_dns.resolver -t mx -- gmail.com\n\n# Query via TCP\n$ python3 -m async_dns.resolver -n tcp://127.0.0.1 -- www.google.com\n\n# Query via TLS\n$ python3 -m async_dns.resolver -n tcps://dns.alidns.com -- www.google.com\n\n# Query from non-standard ports\n$ python3 -m async_dns.resolver -n udp://127.0.0.1:1053 -- www.google.com\n\n# Query from HTTPS\n$ python3 -m async_dns.resolver -n https://dns.alidns.com/dns-query -- www.google.com\n```\n\n**Note:** `--` is required before `hostname`s if the previous option can have multiple arguments.\n\n### Server\n\n```\nusage: python3 -m async_dns.server [-h] [-b BIND] [--hosts HOSTS] [-x [PROXY [PROXY ...]]]\n\nDNS server by Gerald.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -b BIND, --bind BIND  the address for the server to bind\n  --hosts HOSTS         the path of a hosts file, `none` to disable hosts, `local` to read from\n                        local hosts file\n  -x [PROXY [PROXY ...]], --proxy [PROXY [PROXY ...]]\n                        the proxy DNS servers, `none` to serve as a recursive server, `default` to\n                        proxy to default nameservers\n```\n\n**Note:** TLS and HTTPS are not supported in `async_dns` server. Consider [async-doh](https://github.com/gera2ld/async-doh) for DoH server support.\n\nExamples:\n\n``` sh\n# Start a DNS proxy server on :53\n$ python3 -m async_dns.server -b :53 --hosts /etc/hosts\n\n# Start a DNS server over TCP proxy\n$ python3 -m async_dns.server -x tcp://114.114.114.114\n\n# Start a DNS recursive server\n$ python3 -m async_dns.server -x none\n```\n\n## API\n\n``` python\nimport asyncio\nfrom async_dns import types\nfrom async_dns.resolver import ProxyResolver\n\nresolver = ProxyResolver()\nres = asyncio.run(resolver.query('www.baidu.com', types.A))\nprint(res)\n```\n\n### Routing\n\nProxyResolver supports routing based on domains:\n\n```python\nresolver = ProxyResolver(proxies=[\n    ('*.lan', ['192.168.1.1']),                             # query 'udp://192.168.1.1:53' for '*.lan' domains\n    (lambda d: d.endswith('.local'), ['tcp://127.0.0.1']),  # query tcp://127.0.0.1:53 for domains ending with '.local'\n    '8.8.8.8',                                              # equivalent to (None, ['8.8.8.8']), matches all others\n])\n```\n\n### Queries\n\nBoth `resolver.query(fqdn, qtype=ANY, timeout=3.0, tick=5)` and `resolver.query_safe(fqdn, qtype=ANY, timeout=3.0, tick=5)` do queries for domain names. The only difference is that `query_safe` returns `None` if there is an exception, while `query` always raises the exception.\n\n## DoH support\n\nThis library contains a simple implementation of DoH (aka DNS over HTTPS) client with partial HTTP protocol implemented.\n\nIf you need a more powerful DoH client based on [aiohttp](https://docs.aiohttp.org/en/stable/), or a DoH server, consider [async-doh](https://github.com/gera2ld/async-doh).\n\n## Test\n\n``` sh\n$ python3 -m unittest\n```\n",
    'author': 'Gerald',
    'author_email': 'gera2ld@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gera2ld/async_dns',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
