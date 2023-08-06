# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiorecollect']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0']

setup_kwargs = {
    'name': 'aiorecollect',
    'version': '1.0.0',
    'description': 'A Python 3, asyncio-based library for the Recollect Waste API',
    'long_description': '# 🗑  aiorecollect: A Python 3 Library for Pinboard\n\n[![CI](https://github.com/bachya/aiorecollect/workflows/CI/badge.svg)](https://github.com/bachya/aiorecollect/actions)\n[![PyPi](https://img.shields.io/pypi/v/aiorecollect.svg)](https://pypi.python.org/pypi/aiorecollect)\n[![Version](https://img.shields.io/pypi/pyversions/aiorecollect.svg)](https://pypi.python.org/pypi/aiorecollect)\n[![License](https://img.shields.io/pypi/l/aiorecollect.svg)](https://github.com/bachya/aiorecollect/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/bachya/aiorecollect/branch/dev/graph/badge.svg)](https://codecov.io/gh/bachya/aiorecollect)\n[![Maintainability](https://api.codeclimate.com/v1/badges/65fe7eb308dca67c1038/maintainability)](https://codeclimate.com/github/bachya/aiorecollect/maintainability)\n[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)\n\n`aiorecollect` is a Python 3, asyncio-based library for the Recollect Waste API. It\nallows users to programmatically retrieve schedules for waste removal in their area,\nincluding trash, recycling, compost, and more.\n\nSpecial thanks to @stealthhacker for the inspiration!\n\n# Installation\n\n```python\npip install aiorecollect\n```\n\n# Python Versions\n\n`aiorecollect` is currently supported on:\n\n* Python 3.7\n* Python 3.8\n* Python 3.9\n\n# Place and Service IDs\n\nTo use `aiorecollect`, you must know both your Recollect Place and Service IDs:\n\n1. In Chrome open developer tools and go to network tab.\n2. Go to your city\'s Recollect collection calendar.\n3. Search for and select your address in the UI.\n4. Watch for a request that looks like `https://api.recollect.net/api/places/(place_id)/services/(service_id)/events...`\n5. Use the place_id and service_id when instantiating a new `Client`.\n\n# Usage\n\n```python\nimport asyncio\nfrom datetime import date\n\nfrom aiorecollect import Client\n\n\nasync def main() -> None:\n    """Run."""\n    client = await Client("<PLACE ID>", "<SERVICE ID>")\n\n    # The client has a few attributes that you can access:\n    client.place_id\n    client.service_id\n\n    # Get all pickup events on the calendar:\n    pickup_results = await client.async_get_pickup_events()\n\n    # ...or get all pickup events within a certain date range:\n    pickup_results = await client.async_get_pickup_events(\n        start_date=date(2020, 10, 1), end_date=date(2020, 10, 31)\n    )\n\n    # ...or just get the next pickup event:\n    next_pickup = await client.async_get_next_pickup_event()\n\n\nasyncio.run(main())\n```\n\n## The `PickupEvent` Object\n\nThe `PickupEvent` object that is returned from the above calls comes with three\nproperties:\n\n* `date`: a `datetime.date` that denotes the pickup date\n* `pickup_types`: a list of `PickupType` objects that will occur with this event\n* `area_name`: the name of the area in which the event is occurring\n\n## The `PickupType` Object\n\nThe `PickupType` object contains the "internal" name of the pickup type _and_ a\nhuman-friendly representation when it exists:\n\n* `name`: the internal name of the pickup type\n* `friendly_name`: the humany-friendly name of the pickup type (if it exists)\n\n## Connection Pooling\n\nBy default, the library creates a new connection to Recollect with each coroutine. If\nyou are calling a large number of coroutines (or merely want to squeeze out every second\nof runtime savings possible), an\n[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection\npooling:\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom aiorecollect import Client\n\n\nasync def main() -> None:\n    """Run."""\n    async with ClientSession() as session:\n        client = await Client("<PLACE ID>", "<SERVICE ID>", session=session)\n\n        # Get to work...\n\n\nasyncio.run(main())\n```\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/bachya/aiorecollect/issues)\n  or [initiate a discussion on one](https://github.com/bachya/aiorecollect/issues/new).\n2. [Fork the repository](https://github.com/bachya/aiorecollect/fork).\n3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`\n4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`\n5. Install the dev environment: `script/setup`\n6. Code your new feature or bug fix.\n7. Write tests that cover your new functionality.\n8. Run tests and ensure 100% code coverage: `script/test`\n9. Update `README.md` with any new documentation.\n10. Add yourself to `AUTHORS.md`.\n11. Submit a pull request!\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/aiorecollect',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
