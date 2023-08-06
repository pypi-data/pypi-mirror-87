# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['x690']

package_data = \
{'': ['*']}

install_requires = \
['t61codec>=1.0.1,<2.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'x690',
    'version': '0.3.0',
    'description': 'Pure Python X.690 implementation',
    'long_description': 'Pure Python `X.690`_ implementation\n===================================\n\n.. image:: https://github.com/exhuma/x690/workflows/Build%20&%20Publish%20Docs/badge.svg?branch=main\n    :alt: Build & Publish Docs\n\n.. _X.690: https://www.itu.int/rec/recommendation.asp?lang=en&parent=T-REC-X.690-201508-I\n\n\nThis module contains a pure Python implementation of the "x690" standard for\nBER encoding/decoding. Other encodings are currently unsupported but\npull-requests are welcome.\n\n\nType Extensions\n---------------\n\nIt allows defining and detecting new data-types by simply subclassing the base\nclass ``x690.types.Type``. An example for this can be seen in `puresnmp`_\n\n.. _puresnmp: https://github.com/exhuma/puresnmp/blob/4240aa644a1bca01f54683215833dc6711a22745/puresnmp/types.py#L28\n\n\nExamples\n========\n\nEncoding to bytes\n-----------------\n\nEncoding to bytes can be done by simply calling the Python builting ``bytes()``\non instances from ``x690.types``:\n\nEncoding of a single value\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code:: python\n\n    import x690.types as t\n\n    >>> myvalue = t.Integer(12)\n    >>> asbytes = bytes(myvalue)\n    >>> repr(asbytes)\n    b\'\\x02\\x01\\x0c\'\n\nEncoding of a composite value using Sequence\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code:: python\n\n    import x690.types as t\n\n    >>> myvalue = t.Sequence(\n    ...     t.Integer(12),\n    ...     t.Integer(12),\n    ...     t.Integer(12),\n    ... )\n    >>> asbytes = bytes(myvalue)\n    >>> repr(asbytes)\n    b\'0\\t\\x02\\x01\\x0c\\x02\\x01\\x0c\\x02\\x01\\x0c\'\n\n\nDecoding from bytes\n~~~~~~~~~~~~~~~~~~~\n\nDecode bytes by calling ``x690.types.pop_tlv`` on your byte data. This will\nreturn a tuple where the first value contains the decoded object, and the\nsecond one will contain any remaining bytes which were not decoded.\n\n.. code:: python\n\n    import x690.types as t\n    >>> data = b\'0\\t\\x02\\x01\\x0c\\x02\\x01\\x0c\\x02\\x01\\x0c\'\n    >>> decoded, remaining_bytes = t.pop_tlv(data)\n    >>> decoded\n    Sequence(Integer(12), Integer(12), Integer(12))\n    >>> remaining_bytes\n    b\'\'\n\n\nType-Hinting & Enforcing\n~~~~~~~~~~~~~~~~~~~~~~~~\n\n**New in 0.3.0**\n\nWhen decoding bytes, it is possible to specify an expcted type which does two\nthings: Firstly, it tells tools like ``mypy`` what the return type will be and\nsecondly, it runs an internal type-check which *ensures* that the returned\nvalue is of the expected type. ``x690.exc.UnexpectedType`` is raised otherwise.\n\nThis does of course only work if you know the type in advance.\n\n.. code:: python\n\n    import x690.types as t\n    >>> data = b\'0\\t\\x02\\x01\\x0c\\x02\\x01\\x0c\\x02\\x01\\x0c\'\n    >>> decoded, remaining_bytes = t.pop_tlv(data, enforce_type=t.Sequence)\n    >>> decoded\n    Sequence(Integer(12), Integer(12), Integer(12))\n    >>> remaining_bytes\n    b\'\'\n\n\nStrict Decoding\n~~~~~~~~~~~~~~~\n\n**New in 0.3.0**\n\nWhen decoding using ``pop_tlv`` and you don\'t expect any remaining bytes, use\n``strict=True`` which will raise ``x690.exc.IncompleteDecoding`` if there\'s any\nremaining data.\n\n.. code:: python\n\n    import x690.types as t\n    >>> data = b\'0\\t\\x02\\x01\\x0c\\x02\\x01\\x0c\\x02\\x01\\x0cjunk-bytes\'\n    >>> decoded, remaining_bytes = t.pop_tlv(data, strict=True)\n    Traceback (most recent call last):\n      ...\n    x690.exc.IncompleteDecoding: Strict decoding still had 10 remaining bytes!\n',
    'author': 'Michel Albert',
    'author_email': 'michel@albert.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://exhuma.github.io/x690/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
