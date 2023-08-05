# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nhc2_coco']

package_data = \
{'': ['*']}

install_requires = \
['get-mac==0.8.2', 'netifaces==0.10.9', 'paho-mqtt==1.4.0']

setup_kwargs = {
    'name': 'nhc2-coco',
    'version': '1.1.0',
    'description': 'Python controller for a Niko Home Control II installation',
    'long_description': "# pynhc2\n\nLicense: MIT\n\n## Usage\n\n### Create a NHC2 object\n\n```\nNHC2(address, username, password, port, ca_path, switches_as_lights)\n```\n\n* __address__ - IP or host of the connected controller \n* __username__ - The UUID of the profile\n* __password__ - The password\n* __port__ - (optional) The MQTT port. Default = 8883\n* __ca_path__ - (optional) Path of the CA file. Default = included CA file.\n* __switches_as_lights__ - (optional) socket and switched-generic show up as lights.\n\n example:\n\n ```\n coco = NHC2('192.168.1.2', 'abcdefgh-ijkl-mnop-qrst-uvwxyz012345', 'secret_password')\n ```\n \n### What is supported?\nlight, socket, switched-generic, dimmer\n\n### What now?\n TODO - write doc.\n \n TODO - refactor into logical groups that match niko documentation (NHC Relay Action, NHC Dimmer Action, etc)\n \n## What can you do to help?\n\n * Contribute to this project with constructive issues, suggestions, PRs, etc.\n * Help me in any way to get support for more entities (eg heating)\n",
    'author': 'filipvh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/filipvh/nhc2-coco',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
