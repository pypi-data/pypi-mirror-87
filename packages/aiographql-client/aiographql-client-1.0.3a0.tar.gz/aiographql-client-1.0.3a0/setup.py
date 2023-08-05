# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiographql', 'aiographql.client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.5,<4.0',
 'cafeteria-asyncio>=0.2,<0.3',
 'graphql-core>=3.0,<4.0',
 'ujson>=2']

setup_kwargs = {
    'name': 'aiographql-client',
    'version': '1.0.3a0',
    'description': 'An asyncio GraphQL client built on top of aiohttp and graphql-core-next',
    'long_description': '# Asynchronous GraphQL Client\n[![PyPI version](https://badge.fury.io/py/aiographql-client.svg)](https://badge.fury.io/py/aiographql-client)\n[![Python Versions](https://img.shields.io/pypi/pyversions/aiographql-client)](https://pypi.org/project/aiographql-client/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Documentation Status](https://readthedocs.org/projects/aiographql-client/badge/?version=latest)](https://aiographql-client.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=twyla-ai_aiographql-client&metric=alert_status)](https://sonarcloud.io/dashboard?id=twyla-ai_aiographql-client)\n[![](https://github.com/twyla-ai/aiographql-client/workflows/Test%20Suite/badge.svg)](https://github.com/twyla-ai/aiographql-client/actions?query=workflow%3A%22Test+Suite%22)\n\nAn asynchronous GraphQL client built on top of aiohttp and graphql-core-next. The client by default introspects schemas and validates all queries prior to dispatching to the server.\n\n## Documentation\n\nFor the most recent project documentation, you can visit https://aiographql-client.readthedocs.io/.\n\n## Installation\n`pip install aiographql-client`\n\n## Example Usage\nHere are some example usages of this client implementation. For more examples, and advanced scenarios, \nsee [Usage Examples](https://aiographql-client.readthedocs.io/en/latest/examples.html) section in \nthe documentation.\n\n### Simple Query\n```py\nasync def get_logged_in_username(token: str) -> GraphQLResponse:\n    client = GraphQLClient(\n        endpoint="https://api.github.com/graphql",\n        headers={"Authorization": f"Bearer {token}"},\n    )\n    request = GraphQLRequest(\n        query="""\n            query {\n              viewer {\n                login\n              }\n            }\n        """\n    )\n    return await client.query(request=request)\n```\n\n```console\n>>> import asyncio\n>>> response = asyncio.run(get_logged_in_username("<TOKEN FROM GITHUB GRAPHQL API>"))\n>>> response.data\n{\'viewer\': {\'login\': \'username\'}}\n```\n\n### Query Subscription\n```py\nasync def print_city_updates(client: GraphQLClient, city: str) -> None:\n    request = GraphQLRequest(\n        query="""\n            subscription ($city:String!) {\n              city(where: {name: {_eq: $city}}) {\n                description\n                id\n              }\n            }\n        """,\n        variables={"city": city},\n    )\n    # subscribe to data and error events, and print them\n    await client.subscribe(\n        request=request, on_data=print, on_error=print, wait=True\n    )\n```\n\nFor custom event specific callback registration, see [Callback Registry Documentation](https://aiographql-client.readthedocs.io/en/latest/examples.html#callback-registry).\n\n### Query Validation Failures\nIf your query is invalid, thanks to graphql-core-next, we get a detailed exception in the traceback.\n\n```\naiographql.client.exceptions.GraphQLClientValidationException: Query validation failed\n\nCannot query field \'ids\' on type \'chatbot\'. Did you mean \'id\'?\n\nGraphQL request (4:13)\n3:           chatbot {\n4:             ids, bot_names\n               ^\n5:           }\n\nCannot query field \'bot_names\' on type \'chatbot\'. Did you mean \'bot_name\' or \'bot_language\'?\n\nGraphQL request (4:18)\n3:           chatbot {\n4:             ids, bot_names\n                    ^\n5:           }\n\n```\n\n### Query Variables & Operations\nSupport for multi-operation requests and variables is available via the client. For example,\nthe following request contains multiple operations. The instance specifies default values to use.\n\n```py\nrequest = GraphQLRequest(\n    query="""\n    query get_bot_created($id: Int) {\n      chatbot(where: {id: {_eq: $id}}) {\n        id, created\n      }\n    }\n    query get_bot_name($id: Int) {\n      chatbot(where: {id: {_eq: $id}}) {\n        id, bot_name\n      }\n    }\n    """,\n    variables={"id": 109},\n    operation="get_bot_name"\n)\n```\n\nThe default values can be overridden at the time of making the request if required. \n\n```py\nawait client.query(request=request, variables={"id": 20}, operation="get_bot_created")\n```\n',
    'author': 'Arun Neelicattu',
    'author_email': 'arun.neelicattu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/twyla-ai/aiographql-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
