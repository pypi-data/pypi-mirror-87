# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tdxapi', 'tdxapi.enums', 'tdxapi.managers', 'tdxapi.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<21.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'tdxapi',
    'version': '0.7.0',
    'description': 'A Python TeamDynamix API wrapper',
    'long_description': '# tdxapi\n\nA Python TeamDynamix API wrapper\n\nNOTE: tdxapi is under active development. While safe to use, parts of the API may change.\n\n## Dependencies\n\n* python 3.6+\n* requests\n* attrs\n* python-dateutil\n\n## Supported APIs\n\n### General\n* Accounts\n* Applications\n* Attachments\n* Attributes\n* Groups\n\n### Asset/Configuration Management\n* Asset Statuses\n* Assets (except bulk import)\n* Configuration Item Types\n* Configuration Items\n* Configuration Relationship Types\n* Product Models\n* Product Types\n* Vendors\n\n### Reporting\n* Reports\n\n### Roles\n* Functional Roles\n* Resource Pools\n* Security Roles\n\n### Tickets\n* Impacts\n* Priorities\n* Sources\n* Ticket Statuses\n* Ticket Tasks\n* Ticket Types\n* Tickets (except patch)\n* Urgencies\n\n\n## Installation\n\n```\npip install tdxapi\n```\n\n## Quickstart\n\nCreate a TdxClient object representing a connection to a TeamDynamix instance. Currently, only logging in via the administrative account is supported. You can connect to your sandbox with ```use_sandbox=True```:\n\n```\nfrom tdxapi import TdxClient\n\ntdx = TdxClient(\n    "<Organization>",\n    beid="<Organization BEID>",\n    wskey="<Organization Web Services Key>"\n)\n```\n\nNon-Application based APIs can be accessed directly from the TdxClient instance. For example, getting a list of all Accounts:\n\n```\nfor account in tdx.accounts.all():\n    print(account.name)\n```\n\nApplication based APIs require an application object to be created by using the appropriate method and application id. For example to create an asset application:\n\n```\napp = tdx.asset_app(123)\n```\n\nNow we can perform asset related tasks, like retrieving an asset and updating its information:\n\n```\nkevins_pc = app.assets.get(123456)\nkevins_pc.purchase_cost = 1000.00\n\napp.assets.save(kevins_pc)\n```\n\nIf an API supports adding new objects there will be a ```new()``` method to return a new object instance. Using ```new()``` will set the object\'s ```app_id```, if applicable, and populate ```attributes``` with the applicable custom attributes based on object type:\n\n```\nnew_asset = app.assets.new()\n\nnew_asset.name = "Kevin\'s Office Printer"\nnew_asset.serial_number = "123XYZ"\nnew_asset.status_id = 123               # In Use\nnew_asset.manufacturer_id = 456         # HP\nnew_asset.product_model_id = 789        # LaserJet Pro M118dw\n\napp.assets.save(new_asset)\n``` \n\nAlternatively, you can use keyword arguments when creating new objects:\n\n```\nnew_asset = app.assets.new(\n    name="kevins office printer",\n    serial_number="123XYZ",\n    status_id=123,\n    manufacturer_id=456,\n    product_model_id=789\n)\n\napp.assets.save(new_asset)\n```\n\nCustom attributes are stored in a list-like container with added functionality to make working with them easier. Updating attributes only requires the attribute id and the value: \n\n```\nkevins_pc = app.assets.get(123456)\n\nkevins_pc.attributes.update(21212, datetime.now())      # date/time attribute\nkevins_pc.attributes.update(31313, "PO# 1234567")       # text attribute\nkevins_pc.attributes.update(41414, 11223)               # single choice attribute\nkevins_pc.attributes.update(51515, [13579, 24680])      # multiple choice attribute\n```\n\nTo search by attributes set the ```custom_attributes``` argument to a list of tuples containing attribute id and value:\n\n```\n# Find assets with a specific PO Number\nassets = app.assets.search(custom_attributes=[(31313, "PO# 1234567")])\n```\n\nThat\'s it for now. Better documentation and more API support coming soon.',
    'author': 'Marcelo Bajana Jr',
    'author_email': 'placcd@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/placcd/tdxapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
