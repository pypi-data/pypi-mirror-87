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
    'version': '0.2.3',
    'description': 'MC Protocol(MELSEC Communication Protocol) implementation by Python',
    'long_description': '# pymcprotocol\nMC Protocol(MELSEC Communication Protocol) implementation by Python\n\n## Installation \n```console \npip install pymcprotocol\n```\n\n## Protocol type\nNow, pymcprotocol supports only mcprotocol 3E type.\n4E type is implemented. But not tested.\n1C~4C type does not suuport.\n\n## Support PLC series\n- Q Series\n- L Series\n- QnA Series\n- iQ-L Series\n- iQ-R Series\n\nA series does not support 3E or 4E type.  \nSo you cannot communicate. \n\n## How to use mc protocol\n### 1. Set up PLC\nFirst, you need to set up PLC to open port for mcprotocol from Gxworks2 or Gxworks3.  \n- Open port you want to communicate.  \n- Select "Communication Data Code". If you select ascii type, you also need to set "ascii" in setaccessopt method. (default is "bainary")\n- If you would like to write in to PLC, you also have to check __Enable online change__\n\n### 2. Connect by Python\n```python\nimport pymcprotocol\n\n#If you use Q series PLC\npymc3e = pymcprotocol.Type3E()\n#if you use L series PLC,\npymc3e = pymcprotocol.Type3E(plctype="L")\n#if you use QnA series PLC,\npymc3e = pymcprotocol.Type3E(plctype="QnA")\n#if you use iQ-L series PLC,\npymc3e = pymcprotocol.Type3E(plctype="iQ-L")\n#if you use iQ-R series PLC,\npymc3e = pymcprotocol.Type3E(plctype="iQ-R")\n\n#If you use 4E type\npymc4e = pymcprotocol.Type4E()\n\n#If you use ascii byte communication, (Default is "binary")\npymc3e.setaccessopt(commtype="ascii")\npymc3e.connect("192.168.1.2", 1025)\n\n```\n\n### 3. Send command\n```python\n\n#read from D100 to D110\nwordunits_values = pymc3e.batchread_wordunits(headdevice="D100", readsize=10)\n\n#read from X10 to X20\nbitunits_values = pymc3e.batchread_bitunits(headdevice="X10", readsize=10)\n\n#write from D10 to D15\npymc3e.batchread_wordunits(headdevice="D10", values=[0, 10, 20, 30, 40])\n\n#write from Y10 to Y15\npymc3e.batchread_bitunits(headdevice="Y10", values=[0, 1, 0, 1, 0])\n\n#read "D1000", "D2000" and  dword "D3000".\nword_values, dword_values = pymc3e.randomread(word_devices=["D1000", "D2000"], dword_devices=["D3000"])\n\n#write 1000 to "D1000", 2000 to "D2000" and 655362 todword "D3000"\npymc3e.randomwrite(word_devices=["D1000", "D1002"], word_value=[1000, 2000], \n                   dword_devices=["D1004"], dword_values=[655362])\n\n#write 1(ON) to "X0", 0(OFF) to "X10"\npymc3e.randomwrite_bitunits(bit_devices=["X0", "X10"], values=[1, 0])\n\n```\n\n### 4. Remote Operation\n```python\n\n#remote run, clear all device\npymc3e.remote_run(clear_mode=2, force_exec=True)\n\n#remote stop\npymc3e.remote_stop()\n\n#remote latch clear. (have to PLC be stopped)\npymc3e.remote_latchclear()\n\n#remote pause\npymc3e.remote_pause(force_exec=False)\n\n#remote reset\npymc3e.remote_reset()\n\n```\n\n### API Reference\nAPI reference is depoloyed on here.  \nhttps://pymcprotocol.netlify.app/',
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
