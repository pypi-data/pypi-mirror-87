# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['click_keyring']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'cryptography>=2.9,<3.0', 'keyring>=21.0.0,<22.0.0']

setup_kwargs = {
    'name': 'click-keyring',
    'version': '0.2.0',
    'description': 'A click option decorator to store and retrieve credentials using keyring.',
    'long_description': '# click-keyring\n\n**click-keyring** provides a customized [click](https://click.palletsprojects.com) password option decorator to store and retrieve credentials using [keyring](https://keyring.readthedocs.io/en/latest/).\n\nWhen a command is decorated with `click-keyring`:\n* `click-keyring` generates a keyring service name using the command name by default (this can be customized).\n* `click-keyring` uses the service name to look up an existing password using keyring.\n* If an existing password is found, it is used as the param value.\n* If not found, the user is prompted to enter a password.\n* The new password is then saved to the keyring backend.\n\n## Installation\n```bash\npip install click-keyring\n```\n\n## Example\nSee the examples folder for additional examples.\n\n```python\nimport click\nfrom click_keyring import keyring_option\n\n\n@keyring_option(\'-p\', \'--password\')\n@click.option(\'-u\', \'--username\', prompt=\'Username\')\n@click.command()\ndef simple_cmd(username, password):\n    """\n    Example of click_keyring using defaults.\n\n    The password will be saved to keyring with service name\n    matching the click command name (in this case "simple_cmd").\n\n    This can be overridden by setting `prefix` and/or `keyring_option`\n     on the decorator.\n    """\n    click.echo()\n    click.echo(\'** Command Params. User: {}, Password: {}\'.format(username, password))\n\n\nif __name__ == \'__main__\':\n    simple_cmd()\n```\n\nWhen executed the first time, both username and password will be prompted.\n\n```bash\n~/g/c/examples python ./simple.py\nUsername: testuser\nPassword:\n\n** Command Params. User: testuser, Password: testpw\n~/g/c/examples\n```\n\nSubsequent executions using the same username will retrieve the password from the keyring backend.\n\n```bash\n~/g/c/examples python ./simple.py\nUsername: testuser\n\n** Command Params. User: testuser, Password: testpw\n~/g/c/examples\n```\n\n## Service Names\nBy default, the value of the `click.Command.name` attribute is used as the service name.  \nThe name is based on the function name or, if provided, the name argument on the `@click.command` decorator.\n\n```python\n@keyring_option(\'-p\', \'--password\')\n@click.option(\'-u\', \'--username\', prompt=\'Username\')\n@click.command()\ndef simple_cmd(username, password):\n    # service name will be the value of `simple_cmd.name`\n    # This will likely be "simple-cmd" as click replaces underscores with hyphens.\n    pass\n```\n\nA custom service name can be specified using the `prefix` argument.\n\n```python\n@keyring_option(\'-p\', \'--password\', prefix=\'customnservice\')\n@click.option(\'-u\', \'--username\', prompt=\'Username\')\n@click.command()\ndef simple_cmd(username, password):\n    # service name will be "customnservice"\n    pass\n```\n\nOther options on the command can be included in the service name using the `other_options` argument. \nThis is an iterable of option names.  The values provided for those options is appended to the service name. \n\n```python\n@keyring_option(\'-p\', \'--password\', prefix=\'customnservice\', other_options=(\'hostname\',))\n@click.option(\'-n\', \'--hostname\')\n@click.option(\'-u\', \'--username\', prompt=\'Username\')\n@click.command()\ndef simple_cmd(username, hostname, password):\n    # service name will be "customnservice_[value provided for hostname]"\n    pass\n```\n\n',
    'author': 'Kris Seraphine',
    'author_email': 'kris.seraphine@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/baryonyx5/click-keyring',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
