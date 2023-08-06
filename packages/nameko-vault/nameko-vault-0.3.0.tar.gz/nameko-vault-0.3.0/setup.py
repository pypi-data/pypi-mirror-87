# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nameko_vault']

package_data = \
{'': ['*']}

install_requires = \
['hvac>=0.10.5,<0.11.0', 'nameko>=2.12.0,<3.0.0']

setup_kwargs = {
    'name': 'nameko-vault',
    'version': '0.3.0',
    'description': 'A Nameko extension to provide connection with Vault',
    'long_description': '# nameko-vault\n\nExtension for [Nameko](https://www.nameko.io/) that integrates with\n[Vault](https://www.vaultproject.io/).\n\nTo use this tool it is necessary to configure the following parameters in your\nnameko config.yml file:\n\n```\nVAULT_URL: <vault_api_url>\nVAULT_TOKEN: <authentication_token>\n```\n\n## Usage\n\nTo use the tool it\'s needed inform the mount point of the path in which you want\nto obtain any secrets. This mount point can be informed when instantiating the\nprovider or passing this information directly to the method being used.\n\n### Example 1:\n```python\n# path: example/path/secret\nvault = VaultProvider(mount_point="example")\nvault.get_kv_secret(path="path/secret")\n```\n\n### Example 2:\n```python\n# path: example/path/secret\nvault = VaultProvider()\nvault.get_kv_secret(mount_point="example", path="path/secret")\n```\n\n## List Secrets\n\nThe method `get_kv_secrets_list` returns a list of secrets contained in a given\npath\n\n```python\nvault = VaultProvider()\nvault.get_kv_secrets_list(mount_point="example", path="path")\n```\n```\n[\'path/test1\', \'path/test2\']\n```\n\n\n## Get KV Secret Data\n\nThe method `get_kv_secret` returns the content cotained in a given path\n\n```python\nvault = VaultProvider()\nvault.get_kv_secret(mount_point="example", path="path/test")\n```\n```\n[\n   {\n      "data":{\n         "pass":"test",\n         "user":"sample"\n      },\n      "metadata":{\n         "created_time":"2020-07-01T17:44:48.054175763Z",\n         "deletion_time":"",\n         "destroyed":False,\n         "version":1\n      }\n   }\n]\n```\n\n## Create or Update KV Secret\nMethod to create an secret or update an existing one in a given path. \n\n```python\nvault = VaultProvider()\nsecret = {"example": "Test", "number": 42}\nvault.create_or_update_kv_secret(mount_point="example", path="path/test", secret=secret)\n```\n```\n{\n   \'request_id\': \'4ce62ee7-0f88-3efc-d745-5e2fbc423789\',\n   \'lease_id\': \'\',\n   \'renewable\': False,\n   \'lease_duration\': 0,\n   \'data\': {\n      \'created_time\': \'2020-09-10T00:25:40.92411625Z\',\n      \'deletion_time\': \'\',\n      \'destroyed\': False,\n      \'version\': 1\n   },\n   \'wrap_info\': None,\n   \'warnings\': None,\n   \'auth\': None\n}\n```\n\n## Patch KV Secret\nMethod to update an existing path. Either to add a new key/value to the secret and/or update the value for an existing key. Raises an `hvac.exceptions.InvalidRequest` if the path hasn’t been written to previously.\n\n```python\nvault = VaultProvider()\nsecret = {"example": "New Test"}\nvault.patch_kv_secret(mount_point="example", path="path/test", secret=secret)\n```\n```\n{\n   \'request_id\': \'7bf2a869-dc66-efa2-3679-814ef76fb447\',\n   \'lease_id\': \'\',\n   \'renewable\': False,\n   \'lease_duration\': 0,\n   \'data\': {\n      \'created_time\': \'2020-09-10T00:31:32.6783082Z\',\n      \'deletion_time\': \'\',\n      \'destroyed\': False,\n      \'version\': 2\n   },\n   \'wrap_info\': None,\n   \'warnings\': None,\n   \'auth\': None\n}\n```\n',
    'author': 'Instruct Developers',
    'author_email': 'oss@instruct.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/instruct-br/nameko-vault',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
