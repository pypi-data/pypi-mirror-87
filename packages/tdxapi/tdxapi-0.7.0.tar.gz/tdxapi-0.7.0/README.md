# tdxapi

A Python TeamDynamix API wrapper

NOTE: tdxapi is under active development. While safe to use, parts of the API may change.

## Dependencies

* python 3.6+
* requests
* attrs
* python-dateutil

## Supported APIs

### General
* Accounts
* Applications
* Attachments
* Attributes
* Groups

### Asset/Configuration Management
* Asset Statuses
* Assets (except bulk import)
* Configuration Item Types
* Configuration Items
* Configuration Relationship Types
* Product Models
* Product Types
* Vendors

### Reporting
* Reports

### Roles
* Functional Roles
* Resource Pools
* Security Roles

### Tickets
* Impacts
* Priorities
* Sources
* Ticket Statuses
* Ticket Tasks
* Ticket Types
* Tickets (except patch)
* Urgencies


## Installation

```
pip install tdxapi
```

## Quickstart

Create a TdxClient object representing a connection to a TeamDynamix instance. Currently, only logging in via the administrative account is supported. You can connect to your sandbox with ```use_sandbox=True```:

```
from tdxapi import TdxClient

tdx = TdxClient(
    "<Organization>",
    beid="<Organization BEID>",
    wskey="<Organization Web Services Key>"
)
```

Non-Application based APIs can be accessed directly from the TdxClient instance. For example, getting a list of all Accounts:

```
for account in tdx.accounts.all():
    print(account.name)
```

Application based APIs require an application object to be created by using the appropriate method and application id. For example to create an asset application:

```
app = tdx.asset_app(123)
```

Now we can perform asset related tasks, like retrieving an asset and updating its information:

```
kevins_pc = app.assets.get(123456)
kevins_pc.purchase_cost = 1000.00

app.assets.save(kevins_pc)
```

If an API supports adding new objects there will be a ```new()``` method to return a new object instance. Using ```new()``` will set the object's ```app_id```, if applicable, and populate ```attributes``` with the applicable custom attributes based on object type:

```
new_asset = app.assets.new()

new_asset.name = "Kevin's Office Printer"
new_asset.serial_number = "123XYZ"
new_asset.status_id = 123               # In Use
new_asset.manufacturer_id = 456         # HP
new_asset.product_model_id = 789        # LaserJet Pro M118dw

app.assets.save(new_asset)
``` 

Alternatively, you can use keyword arguments when creating new objects:

```
new_asset = app.assets.new(
    name="kevins office printer",
    serial_number="123XYZ",
    status_id=123,
    manufacturer_id=456,
    product_model_id=789
)

app.assets.save(new_asset)
```

Custom attributes are stored in a list-like container with added functionality to make working with them easier. Updating attributes only requires the attribute id and the value: 

```
kevins_pc = app.assets.get(123456)

kevins_pc.attributes.update(21212, datetime.now())      # date/time attribute
kevins_pc.attributes.update(31313, "PO# 1234567")       # text attribute
kevins_pc.attributes.update(41414, 11223)               # single choice attribute
kevins_pc.attributes.update(51515, [13579, 24680])      # multiple choice attribute
```

To search by attributes set the ```custom_attributes``` argument to a list of tuples containing attribute id and value:

```
# Find assets with a specific PO Number
assets = app.assets.search(custom_attributes=[(31313, "PO# 1234567")])
```

That's it for now. Better documentation and more API support coming soon.