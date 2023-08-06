# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['busylight', 'busylight.api', 'busylight.effects', 'busylight.lights']

package_data = \
{'': ['*']}

install_requires = \
['bitvector-for-humans>=0.14.0,<0.15.0',
 'hidapi>=0.9,<0.11',
 'typer>=0,<1',
 'webcolors>=1.11.1,<2.0.0']

extras_require = \
{'webapi': ['uvicorn>=0.12.2,<0.13.0', 'fastapi>=0.61.1,<0.63.0']}

entry_points = \
{'console_scripts': ['busylight = busylight.__main__:cli']}

setup_kwargs = {
    'name': 'busylight-for-humans',
    'version': '0.7.9',
    'description': 'Control USB connected LED lights, like a human.',
    'long_description': '![BusyLight Project Logo][1]\n\n![Python 3.7 Test][37] ![Python 3.8 Test][38] ![Python 3.9 Test][39]\n\n[BusyLight for Humans™][0] gives you control of USB attached LED\nlights from a variety of vendors. Lights can be controlled via\nthe command-line, using a HTTP API or imported directly into your own\npython projects. Need a light to let you know when a host is down, or\nwhen the dog wants out? How about a light that indicates "do not disturb"?\n\nThe possibilities are _literally_ endless.\n\n![All Supported Lights][DemoGif]\n\n<em>Back to Front, Left to Right</em> <br>\n<b>BlyncLight, BlyncLight Plus, Busylight</b> <br>\n<b>Blink(1), Flag, BlinkStick</b>\n\n## Features\n- Control Lights via [Command-Line][BUSYLIGHT.1]\n- Control Lights via [Web API][WEBAPI]\n- Supports Lights from Five Vendors\n  * Agile Innovations BlinkStick \n  * Embrava Blynclight\n  * Kuando BusyLight\n  * Luxafor Flag\n  * ThingM Blink1\n- Supported on MacOS, Linux, probably Windows and BSD too!\n- Tested extensively on Raspberry Pi 3b+, Zero W and 4\n\n## Basic Install \n\n```console\n$ python3 -m pip install busylight-for-humans \n```\n\n## Web API Install\n\nInstall `uvicorn` and `FastAPI` in addition to `busylight`:\n\n```console\n$ python3 -m pip install busylight-for-humans[webapi]\n```\n\n## Linux Post-Install Activities\nLinux controls access to USB devices via the udev subsystem and by default denies non-root users access to devices it doesn\'t recognize. I\'ve got you covered!\n\nYou\'ll need root access to configure the udev rules:\n\n```console\n$ busylight udev-rules -o 99-busylights.rules\n$ sudo cp 99-busylights.rules /etc/udev/rules.d\n$ sudo udevadm control -R\n$ # unplug/plug your light\n$ busylight on\n```\n\n## Command-Line Examples\n\n```console\n$ busylight on               # light turns on green\n$ busylight on red           # now it\'s shining a friendly red\n$ busylight on 0xff0000      # still red\n$ busylight on #00ff00       # now it\'s blue!\n$ busylight blink            # it\'s slowly blinking on and off with a red color\n$ busylight blink green fast # blinking faster green and off\n$ busylight --all on         # turn all lights on green\n$ busylight --all off        # turn all lights off\n```\n\n## HTTP API Examples\n\nFirst start the `busylight` API server:\n```console\n$ busylight serve\nINFO:     Started server process [20189]\nINFO:     Waiting for application startup.\nINFO:     Application startup complete.\nINFO:     Uvicorn running on http://0.0.0.0:8888 (Press CTRL+C to quit)\n```\n\nThe API is fully documented and available @ `https://localhost:8888/redoc`\n\n\nNow you can use the web API endpoints which return JSON payloads:\n\n```console\n  $ curl http://localhost:8888/1/lights\n  $ curl http://localhost:8888/1/lights/on\n  $ curl http://localhost:8888/1/lights/off\n  $ curl http://localhost:8888/1/light/0/on/purple\n  $ curl http://localhost:8888/1/light/0/off\n  $ curl http://localhost:8888/1/lights/on\n  $ curl http://localhost:8888/1/lights/off\n  $ curl http://localhost:8888/1/lights/rainbow\n```\n\n[0]: https://pypi.org/project/busylight-for-humans/\n[1]: https://github.com/JnyJny/busylight/blob/master/docs/assets/BusyLightLogo.png\n[BUSYLIGHT.1]: https://github.com/JnyJny/busylight/blob/master/docs/busylight.1.md\n[WEBAPI]: https://github.com/JnyJny/busylight/blob/master/docs/busylight_api.pdf\n\n[37]: https://github.com/JnyJny/busylight/workflows/Python%203.7/badge.svg\n[38]: https://github.com/JnyJny/busylight/workflows/Python%203.8/badge.svg\n[39]: https://github.com/JnyJny/busylight/workflows/Python%203.9/badge.svg\n\n[DemoGif]: https://github.com/JnyJny/busylight/raw/master/demo/demo.gif\n',
    'author': 'JnyJny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JnyJny/busylight.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
