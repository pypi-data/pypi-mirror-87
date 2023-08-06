# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protocol_lib']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.7.4.3,<4.0.0.0']

setup_kwargs = {
    'name': 'protocol-lib',
    'version': '0.5.0',
    'description': 'Protocols for better structural typing',
    'long_description': '# protocol-lib\n\n![Build](https://github.com/eganjs/protocol-lib/workflows/ci/badge.svg)\n\nProtocols for better structural typing\n\n## Goals\n\nImplement Protocols for:\n- [x] Container\n- [x] Hashable\n- [x] Iterable\n- [x] Iterator\n- [x] Reversible\n- [ ] Generator\n- [ ] Sized\n- [ ] Callable\n- [ ] Collection\n- [ ] Sequence\n- [ ] MutableSequence\n- [ ] ByteString\n- [ ] Set\n- [ ] MutableSet\n- [ ] Mapping\n- [ ] MutableMapping\n- [ ] MappingView\n- [ ] ItemsView\n- [ ] KeysView\n- [ ] ValuesView\n- [ ] Awaitable\n- [ ] Coroutine\n- [ ] AsyncIterable\n- [ ] AsyncIterator\n- [ ] AsyncGenerator\n\n## Updating project config\n\nTo do this make edits to the `.projenrc.js` file in the root of the project and run `npx projen` to update existing or generate new config. Please also use `npx prettier --trailing-comma all --write .projenrc.js` to format this file.\n',
    'author': 'Joseph Egan',
    'author_email': 'joseph.s.egan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eganjs/protocol-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
