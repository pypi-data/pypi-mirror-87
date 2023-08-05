# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['r2pyapi']

package_data = \
{'': ['*']}

install_requires = \
['r2pipe>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'r2pyapi',
    'version': '0.1.1',
    'description': 'High level radare2 python API',
    'long_description': '# r2pyapi\n\nHigh level radare2 python API \n\n# Usage\n\n``` python\nimport r2pipe\nfrom r2pyapi import R2Surface, R2Seeker, R2Reader\n\nr2 = r2pipe.open("test.exe")\n\n# instruction search\nwith R2Seeker(r2) as seeker:\n    results = seeker.seek_instructions("push ebp")\n    print(next(result))\n    # R2Instruction(offset=4288663, len=2, code=\'push ebp\')\n\n# read byte sequences\nwith R2Reader(r2) as reader:\n    bytes_read = reader.read_bytes_at(0x0401000, 4)\n    # [85, 139, 236, 131]\n\n# get sections\nr2_surf = R2Surface(r2)\nprint(r2_surf.sections)\n# [R2Section(vaddr=4198400, paddr=1024, size=51200, vsize=53248, name=\'.text\', perm=\'-r-x\'), ... ]\n\n# get import\nprint(r2_surf.find_import("MessageBoxA"))\n# R2Import(ordinal=1, bind=\'NONE\', type=\'FUNC\', name=\'MessageBoxA\', libname=\'USER32.dll\', plt=4251916)\n```\n',
    'author': 'Koh M. Nakagawa',
    'author_email': 'tsunekou1019@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
