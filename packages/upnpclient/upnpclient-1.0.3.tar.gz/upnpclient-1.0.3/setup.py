# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['upnpclient']

package_data = \
{'': ['*']}

install_requires = \
['ifaddr>=0.1.7,<0.2.0',
 'lxml>=4.0.0,<5.0.0',
 'python-dateutil>=2.0.0,<3.0.0',
 'requests>=2.0.0,<3.0.0',
 'six>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'upnpclient',
    'version': '1.0.3',
    'description': 'Python 3 library for accessing uPnP devices.',
    'long_description': '[![Build Status](https://travis-ci.org/flyte/upnpclient.svg?branch=develop)](https://travis-ci.org/flyte/upnpclient)\n\nuPnPclient\n============\n\n_uPnP client library for Python 3._\n\nThis library can be used to discover and consume uPnP devices and their services.\n\nIt\'s originally based on [Ferry Boender\'s work](https://github.com/fboender/pyupnpclient) and his blog post entitled [Exploring UPnP with Python](https://www.electricmonk.nl/log/2016/07/05/exploring-upnp-with-python/).\n\n### Installation\n\n```bash\npip install upnpclient\n```\n\n### Usage\n\nTypical usage:\n\n```python\nIn [1]: import upnpclient\n\nIn [2]: devices = upnpclient.discover()\n\nIn [3]: devices\nOut[3]: \n[<Device \'OpenWRT router\'>,\n <Device \'Harmony Hub\'>,\n <Device \'walternate: root\'>]\n\nIn [4]: d = devices[0]\n\nIn [5]: d.WANIPConn1.GetStatusInfo()\nOut[5]: \n{\'NewConnectionStatus\': \'Connected\',\n \'NewLastConnectionError\': \'ERROR_NONE\',\n \'NewUptime\': 14851479}\n\nIn [6]: d.WANIPConn1.GetNATRSIPStatus()\nOut[6]: {\'NewNATEnabled\': True, \'NewRSIPAvailable\': False}\n\nIn [7]: d.WANIPConn1.GetExternalIPAddress()\nOut[7]: {\'NewExternalIPAddress\': \'123.123.123.123\'}\n```\n\nIf you know the URL for the device description XML, you can access it directly.\n\n```python\nIn [1]: import upnpclient\n\nIn [2]: d = upnpclient.Device("http://192.168.1.1:5000/rootDesc.xml")\n\nIn [3]: d.services\nOut[3]: \n[<Service service_id=\'urn:upnp-org:serviceId:Layer3Forwarding1\'>,\n <Service service_id=\'urn:upnp-org:serviceId:WANCommonIFC1\'>,\n <Service service_id=\'urn:upnp-org:serviceId:WANIPConn1\'>]\n\nIn [4]: d.Layer3Forwarding1.actions\nOut[4]: \n[<Action \'SetDefaultConnectionService\'>,\n <Action \'GetDefaultConnectionService\'>]\n\nIn [5]: d.Layer3Forwarding1.GetDefaultConnectionService()\nOut[5]: {\'NewDefaultConnectionService\': \'uuid:46cb370a-d7f2-490f-ac01-fb0db6c8b22b:WANConnectionDevice:1,urn:upnp-org:serviceId:WANIPConn1\'}\n```\n\nSometimes the service or action name isn\'t a valid property name. In which case, service and actions can be accessed other ways:\n\n```python\nIn [1]: d["Layer3Forwarding1"]["GetDefaultConnectionService"]()\nOut[1]: {\'NewDefaultConnectionService\': \'uuid:46cb370a-d7f2-490f-ac01-fb0db6c8b22b:WANConnectionDevice:1,urn:upnp-org:serviceId:WANIPConn1\'}\n```\n\nTo view the arguments required to call a given action:\n\n```python\nIn [1]: d.WANIPConn1.AddPortMapping.argsdef_in\nOut[1]: \n[(\'NewRemoteHost\',\n  {\'allowed_values\': set(), \'datatype\': \'string\', \'name\': \'RemoteHost\'}),\n (\'NewExternalPort\',\n  {\'allowed_values\': set(), \'datatype\': \'ui2\', \'name\': \'ExternalPort\'}),\n (\'NewProtocol\',\n  {\'allowed_values\': {\'TCP\', \'UDP\'},\n   \'datatype\': \'string\',\n   \'name\': \'PortMappingProtocol\'}),\n (\'NewInternalPort\',\n  {\'allowed_values\': set(), \'datatype\': \'ui2\', \'name\': \'InternalPort\'}),\n (\'NewInternalClient\',\n  {\'allowed_values\': set(), \'datatype\': \'string\', \'name\': \'InternalClient\'}),\n (\'NewEnabled\',\n  {\'allowed_values\': set(),\n   \'datatype\': \'boolean\',\n   \'name\': \'PortMappingEnabled\'}),\n (\'NewPortMappingDescription\',\n  {\'allowed_values\': set(),\n   \'datatype\': \'string\',\n   \'name\': \'PortMappingDescription\'}),\n (\'NewLeaseDuration\',\n  {\'allowed_values\': set(),\n   \'datatype\': \'ui4\',\n   \'name\': \'PortMappingLeaseDuration\'})]\n```\n\nand then to call the action using those arguments:\n\n```python\nIn [1]: d.WANIPConn1.AddPortMapping(\n   ...:     NewRemoteHost=\'0.0.0.0\',\n   ...:     NewExternalPort=12345,\n   ...:     NewProtocol=\'TCP\',\n   ...:     NewInternalPort=12345,\n   ...:     NewInternalClient=\'192.168.1.10\',\n   ...:     NewEnabled=\'1\',\n   ...:     NewPortMappingDescription=\'Testing\',\n   ...:     NewLeaseDuration=10000)\nOut[1]: {}\n```\n\nSimilarly, the arguments you can expect to receive in response are listed:\n\n```python\nIn [1]: d.WANIPConn1.GetGenericPortMappingEntry.argsdef_out\nOut[1]: \n[(\'NewRemoteHost\',\n  {\'allowed_values\': set(), \'datatype\': \'string\', \'name\': \'RemoteHost\'}),\n (\'NewExternalPort\',\n  {\'allowed_values\': set(), \'datatype\': \'ui2\', \'name\': \'ExternalPort\'}),\n (\'NewProtocol\',\n  {\'allowed_values\': {\'TCP\', \'UDP\'},\n   \'datatype\': \'string\',\n   \'name\': \'PortMappingProtocol\'}),\n (\'NewInternalPort\',\n  {\'allowed_values\': set(), \'datatype\': \'ui2\', \'name\': \'InternalPort\'}),\n (\'NewInternalClient\',\n  {\'allowed_values\': set(), \'datatype\': \'string\', \'name\': \'InternalClient\'}),\n (\'NewEnabled\',\n  {\'allowed_values\': set(),\n   \'datatype\': \'boolean\',\n   \'name\': \'PortMappingEnabled\'}),\n (\'NewPortMappingDescription\',\n  {\'allowed_values\': set(),\n   \'datatype\': \'string\',\n   \'name\': \'PortMappingDescription\'}),\n (\'NewLeaseDuration\',\n  {\'allowed_values\': set(),\n   \'datatype\': \'ui4\',\n   \'name\': \'PortMappingLeaseDuration\'})]\n```\n\n#### HTTP Auth/Headers\n\nYou may pass a\n[requests compatible](http://docs.python-requests.org/en/master/user/authentication/)\nauthentication object and/or a dictionary containing headers to use on the HTTP\ncalls to your uPnP device.\n\nThese may be set on the `Device` itself on creation for use with every HTTP\ncall:\n\n```python\ndevice = upnpclient.Device(\n    "http://192.168.1.1:5000/rootDesc.xml"\n    http_auth=(\'myusername\', \'mypassword\'),\n    http_headers={\'Some-Required-Header\': \'somevalue\'}\n)\n```\n\nOr on a per-call basis:\n\n```python\ndevice.Layer3Forwarding1.GetDefaultConnectionService(\n    http_auth=(\'myusername\', \'mypassword\'),\n    http_headers={\'Some-Required-Header\': \'somevalue\'}\n)\n```\n\nIf you\'ve set either at `Device` level, they can be overridden per-call by\nsetting them to `None`.\n',
    'author': 'Ellis Percival',
    'author_email': 'flyte@failcode.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/flyte/upnpclient',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
