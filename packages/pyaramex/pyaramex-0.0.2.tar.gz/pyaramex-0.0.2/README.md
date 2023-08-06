# pyaramex
A lightweight, unifying Python wrapper around Aramex web services.

* Supports the Tracking, Location, Shipping and Rates API's
* Lazy-loading of WSDL files

# Requirements

* Client Info, which must be obtained from Aramex directly
* All requests must be made via HTTPS - for more information, visit the Aramex Web Developer documentation

# Installation

```
$ pip install pyaramex
```

# Getting started

## Initialising the client

ClientInfo can either be provided to the client using environment variables or by initialising them directly when you initialise the Aramex object.

```python3
from pyaramex import Aramex

aramex = Aramex()
```

## Making requests

All Aramex services are named as they appear in the respective Web Services albeit using Python underscore syntax.

```python
"""
The rates client and Rates WSDL are loaded only when called, thereafter they're cached for the duration of the session
"""

rate_response = aramex.rates.get_rate()
```