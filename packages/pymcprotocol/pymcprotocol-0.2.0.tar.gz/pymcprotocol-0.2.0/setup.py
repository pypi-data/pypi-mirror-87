# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymcprotocol']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymcprotocol',
    'version': '0.2.0',
    'description': 'MC Protocol(MELSEC Communication Protocol) implementation by Python',
    'long_description': '# pymcprotocol\nMC Protocol(MELSEC Communication Protocol) implementation by Python\n\n## Installation \n```console \npip install pymcprotocol\n```\n\n## Protocol type\nNow, pymcprotocol supports only mcprotocol 3E type.\nIn the future, support 4E type. (And if possible, 1C~4C type too...)\n\n## How to use mc protocol\n### 1. Set up PLC\nFirst, you need to set upopen your PLC port to communicate by mcprotocol in Gxworks2 or Gxworks3.  \n- Open port you want to communicate.  \n- Select "Communication Data Code". If you select ascii type, you also need to set "ascii" in setaccessopt method. (default is "bainary")\n- If you would like to write in to PLC, you also have to check __Enable online change__\n\n### 2. Connect by Python\n```python\nimport pymcprotocol\n\n#If you use Q series PLC\npymc3e = pymcprotocol.Type3E()\n#if you use L series PLC,\npymc3e = pymcprotocol.Type3E(plctype="L")\n#if you use iQ series PLC,\npymc3e = pymcprotocol.Type3E(plctype="iQ")\n\n#If you use ascii byte communication, (Default is "binary")\npymc3e.setaccessopt(commtype="ascii")\npymc3e.connect("192.168.1.2", 1025)\n\n```\n\n### 3. Send command\n```python\n#read from D100 to D110\npymc3e.batchread_wordunits(headdevice="D100", readsize=10)\n\n#read from X10 to X20\npymc3e.batchread_bitunits(headdevice="X10", readsize=10)\n\n#write from D10 to D15\npymc3e.batchread_wordunits(headdevice="D10", values=[0, 10, 20, 30, 40])\n\n#write from Y10 to Y15\npymc3e.batchread_bitunits(headdevice="Y10", values=[0, 1, 0, 1, 0])\n\npymc3e.close()\n```\n\n### API Reference\nAPI reference is depoloyed on here.  \nhttps://pymcprotocol.netlify.app/',
    'author': 'Yohei Osawa',
    'author_email': 'yohei.osawa.318.niko8@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pymcprotocol.netlify.app/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
