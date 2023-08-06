# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thingtalk',
 'thingtalk.domains',
 'thingtalk.models',
 'thingtalk.routers',
 'thingtalk.toolkits']

package_data = \
{'': ['*']}

install_requires = \
['async-cron>=1.6.2,<2.0.0',
 'email_validator>=1.1.1,<2.0.0',
 'fastapi>=0.61.0,<0.62.0',
 'gmqtt>=0.6.9,<0.7.0',
 'httpx>=0.16.0,<0.17.0',
 'ifaddr>=0.1.7,<0.2.0',
 'jsonschema>=3.2.0,<4.0.0',
 'loguru>=0.5.2,<0.6.0',
 'pyee>=8.1.0,<9.0.0',
 'tinydb>=4.2.0,<5.0.0',
 'ujson>=4.0.0,<5.0.0',
 'uvicorn[standard]>=0.12.1,<0.13.0',
 'zeroconf>=0.28.2,<0.29.0']

extras_require = \
{'docs': ['mkdocs-material>=6.1.6,<7.0.0']}

setup_kwargs = {
    'name': 'thingtalk',
    'version': '0.7.5',
    'description': 'Web of Things framework, high performance, easy to learn, fast to code, ready for production',
    'long_description': '<h1 align="center">Project ThingTalk</h1>\n\n<h2 align="center">Thing as a Service</h2>\n\n[![pypi-v](https://img.shields.io/pypi/v/thingtalk.svg)](https://pypi.python.org/pypi/thingtalk)\n[![python](https://img.shields.io/pypi/pyversions/thingtalk.svg)](https://github.com/hidaris/thingtalk)\n\n## What is `thingtalk` ?\n`thingtalk` is a library for the Web of Things protocol in Python Asyncio. This library is derived of webthing-python project (supporting Tornado) but adapted for fastapi (based on Uvicorn for better performance).\n\n### additional features\n1. additional_routes -- list of additional routes add to the server\n2. additional_middlewares -- list of additional middlewares add to the server\n3. additional_on_startup -- list of additional starup event handlers add to the server\n4. additional_on_shutdown -- list of additional shutdown event handlers add to the server\n5. thing.sync_property -- Sync a property value from cloud or mqtt broker etc, property set value with no action disclaim.\n6. thing.property_action -- addional action sync the property change to device. \n6. property.set_value(value, with_action=True) -- if with_action is True, Value instance should emit `update`, else `sync`\n7. Add the property change observer to notify the Thing about a property change or do some additional action:\n\n```python\nself.value.on("update", lambda _: self.thing.property_notify(self))\nself.value.on("sync", lambda _: self.thing.property_notify(self))\nself.value.on("update", lambda _: self.thing.property_action(self))\n```\n   \n\n\n## Installation\nthingtalk can be installed via pip, as such:\n\n`$ pip install thingtalk`\n\n## Running the Sample\n`$ wget\nhttps://raw.githubusercontent.com/hidaris/thingtalk/master/example/test.py`\n\n`$ uvicorn test:app --reload`\n\nThis starts a server and lets you search for it from your gateway through mDNS. To add it to your gateway, navigate to the Things page in the gateway\'s UI and click the + icon at the bottom right. If both are on the same network, the example thing will automatically appear.\n\n## Example Implementation\nIn this code-walkthrough we will set up a dimmable light and a humidity sensor (both using fake data, of course). Both working examples can be found in here.\n\nDimmable Light\nImagine you have a dimmable light that you want to expose via the web of things API. The light can be turned on/off and the brightness can be set from 0% to 100%. Besides the name, description, and type, a Light is required to expose two properties:\n\non: the state of the light, whether it is turned on or off\nSetting this property via a PUT {"on": true/false} call to the REST API toggles\nthe light.\n\nbrightness: the brightness level of the light from 0-100%\nSetting this property via a PUT call to the REST API sets the brightness level of this light.\nFirst we create a new Thing:\n\n``` python\nfrom thingtalk import Thing, Property, Value\n\n\nclass Light(Thing):\n    type = [\'OnOffSwitch\', \'Light\'],\n    description = \'A web connected lamp\'\n    \n    super().__init__(\n        \'urn:dev:ops:my-lamp-1234\',\n        \'My Lamp\',\n    )\n```\nNow we can add the required properties.\n\nThe on property reports and sets the on/off state of the light. For this, we need to have a Value object which holds the actual state and also a method to turn the light on/off. For our purposes, we just want to log the new state if the light is switched on/off.\n\n``` python\nasync def build(self):\n    on = Property(\n            \'on\',\n            Value(True, lambda v: print(\'On-State is now\', v)),\n            metadata={\n                \'@type\': \'OnOffProperty\',\n                \'title\': \'On/Off\',\n                \'type\': \'boolean\',\n                \'description\': \'Whether the lamp is turned on\',\n        })\n    await self.add_property(on)\n```\n\nThe brightness property reports the brightness level of the light and sets the level. Like before, instead of actually setting the level of a light, we just log the level.\n\n``` python\nbrightness = Property(\n         \'brightness\',\n        Value(50, lambda v: print(\'Brightness is now\', v)),\n        metadata={\n            \'@type\': \'BrightnessProperty\',\n            \'title\': \'Brightness\',\n            \'type\': \'number\',\n            \'description\': \'The level of light from 0-100\',\n            \'minimum\': 0,\n            \'maximum\': 100,\n            \'unit\': \'percent\',\n        })\nawait self.add_property(brightness)\n```\n\nNow we can add our newly created thing to the server and start it:\n\n``` python\n# If adding more than one thing, use MultipleThings() with a name.\n# In the single thing case, the thing\'s name will be broadcast.\nwith background_thread_loop() as loop:\n    app = WebThingServer(loop, Light).create()\n```\n\nThis will start the server, making the light available via the WoT REST API and announcing it as a discoverable resource on your local network via mDNS.\n\nSensor\nLet\'s now also connect a humidity sensor to the server we set up for our light.\n\nA MultiLevelSensor (a sensor that returns a level instead of just on/off) has one required property (besides the name, type, and optional description): level. We want to monitor this property and get notified if the value changes.\n\nFirst we create a new Thing:\n\n```python\nfrom thingtalk import Thing, Property, Value\n\nclass Light(Thing):\n    type = [\'MultiLevelSensor\'],\n    description = \'A web connected humidity sensor\'\n    \n    super().__init__(\n        \'urn:dev:ops:my-humidity-sensor-1234\',\n        \'My Humidity Sensor\',\n    )\n```\n\nThen we create and add the appropriate property:\n\nlevel: tells us what the sensor is actually reading\n\nContrary to the light, the value cannot be set via an API call, as it wouldn\'t make much sense, to SET what a sensor is reading. Therefore, we are creating a readOnly property.\n\n```python\nasync def build(self): \n    await self.add_property(\n        Property(\n            \'level\',\n            Value(0.0),\n            metadata={\n                \'@type\': \'LevelProperty\',\n                \'title\': \'Humidity\',\n                \'type\': \'number\',\n                \'description\': \'The current humidity in %\',\n                \'minimum\': 0,\n                \'maximum\': 100,\n                \'unit\': \'percent\',\n                \'readOnly\': True,\n            }))\n    return self\n```\n\n\nNow we have a sensor that constantly reports 0%. To make it usable, we need a thread or some kind of input when the sensor has a new reading available. For this purpose we start a thread that queries the physical sensor every few seconds. For our purposes, it just calls a fake method.\n\n```python\nself.sensor_update_task = \\\n    get_event_loop().create_task(self.update_level())\n\nasync def update_level(self):\n    try:\n        while True:\n            await sleep(3)\n            new_level = self.read_from_gpio()\n            logging.debug(\'setting new humidity level: %s\', new_level)\n            await self.level.notify_of_external_update(new_level)\n    except CancelledError:\n        pass\n```\n\nThis will update our Value object with the sensor readings via the self.level.notify_of_external_update(read_from_gpio()) call. The Value object now notifies the property and the thing that the value has changed, which in turn notifies all websocket listeners.\n',
    'author': 'hidaris',
    'author_email': 'zuocool@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hidaris/thingtalk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
