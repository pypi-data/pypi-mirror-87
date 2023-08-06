======
BotAPI
======

|PyPI| |Python| |Codecov| |build| |License| |Requirements|

.. |PyPI| image:: https://img.shields.io/pypi/v/botapi?color=blue
    :target: https://pypi.org/project/botapi
    :alt: PyPI

.. |License| image:: https://img.shields.io/github/license/EdiBoba/botapi?color=brightgreen
    :target: https://github.com/EdiBoba/botapi/blob/master/LICENSE.txt
    :alt: GitHub

.. |Build| image:: https://travis-ci.org/EdiBoba/botapi.svg?branch=master
    :target: https://travis-ci.org/EdiBoba/botapi

.. |Requirements| image:: https://requires.io/github/EdiBoba/botapi/requirements.svg?branch=master
    :target: https://requires.io/github/EdiBoba/botapi/requirements/?branch=master
    :alt: Requirements Status

.. |Codecov| image:: https://codecov.io/gh/EdiBoba/botapi/branch/master/graph/badge.svg?token=92ZGI6R4P5
    :target: https://codecov.io/gh/EdiBoba/botapi

.. |BlackCode| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |Bandit| image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status

.. |Python| image:: https://img.shields.io/pypi/pyversions/botapi
    :target: https://pypi.org/project/botapi
    :alt: PyPI - Python Version

Build json API fast and simple

Key Features
------------

- Provides simple API.
- Supports serialize/deserialize class objects to/from dictionary.
- Field type may be the same with model type (self_base Field attribute)

Installation
------------

.. code-block:: text

   pip install botapi

Getting started
---------------

Let's take some data:

.. code-block:: python

    order = {
        'user': {
            'name': 'Jack',
            'surname': 'Doe',
            'phone': '123456789',
        },
        'paid': True,
        'items': [
            {
                'name': 'product 1',
                'id': 1,
                'quantity': 2,
                'subtotal': 10.5
            },
            {
                'name': 'product 2',
                'id': 2,
                'quantity': 1,
                'subtotal': 5
            }
        ]
    }

Write models:

.. code-block:: python

    from botapi import Model, Field, ListField

    class Item(Model):
    name = Field()
    item_id = Field(alias='id')


    # inherit model
    class CartItem(Item):
        quantity = Field(base=int)
        subtotal = Field()


    class UserModel(Model):
        name = Field()
        surname = Field()
        phone = Field()


    class OrderModel(Model):
        user = Field(base=UserModel)
        paid = Field(base=bool, default=False)
        cart = ListField(item_base=CartItem, default=[], alias='items')

Deserialize and work with data:

.. code-block:: python

    # deserialize data
    obj = OrderModel(**order)

    # work with data
    obj.user.name = 'John'
    obj.paid = True
    obj.cart[0].subtotal = 12.5

Serialize model:

.. code-block:: python

    # may be you want to add some data
    comment = 'call before delivery'

    # serialize data
    print(obj.serialize(data_to_update={'comment': comment}))

Output:

.. code-block:: text

    {'paid': True, 'items': [{'name': 'product 1', 'quantity': 2, 'id': 1, 'subtotal': 12.5}, {'name': 'product 2', 'quantity': 1, 'id': 2, 'subtotal': 5}], 'user': {'name': 'John', 'surname': 'Doe', 'phone': '123456789'}, 'comment': 'call before delivery'}

Requirements
------------
- Python_ >= 3.6

.. _Python: https://www.python.org/

License
-------

``BotAPI`` is distributed under the `Apache License 2.0 license
<https://github.com/EdiBoba/botapi/blob/master/LICENSE.txt>`_.