# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli',
 'cli.actions',
 'cli.ansible',
 'cli.ansible.connection',
 'cli.commands',
 'cli.constants',
 'cli.data',
 'cli.helpers',
 'cli.helpers.check',
 'cli.helpers.config',
 'cli.helpers.ec2',
 'cli.saml_clients',
 'cli.tests',
 'cli.tests.commands',
 'cli.tests.decorators',
 'cli.tests.helpers',
 'cli.tests.helpers.ec2',
 'cli.tests.integration',
 'cli.tests.saml_clients']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'SecretStorage>=3.2.0,<4.0.0',
 'analytics-python>=1.2.9,<2.0.0',
 'boto3>=1.16.20,<2.0.0',
 'click-option-group>=0.5.1,<0.6.0',
 'click>=7.1.2,<8.0.0',
 'immutables>=0.14,<0.15',
 'keyring>=21.5.0,<22.0.0',
 'policyuniverse>=1.3.2,<2.0.0',
 'portalocker>=2.0.0,<3.0.0',
 'sentry-sdk>=0.19.3,<0.20.0',
 'validators>=0.18.1,<0.19.0']

entry_points = \
{'console_scripts': ['sym = sym.cli.sym:sym']}

setup_kwargs = {
    'name': 'sym-cli',
    'version': '0.0.61',
    'description': 'The CLI for Sym',
    'long_description': "# sym-cli\n\nSym CLI\n\n## Usage\n\n### Login\n\n`sym login --email rick@symops.io --org sym`\n\nOr, to run interactively: `sym login`\n\nCurrently, this saves the email and org name to a local configuration file that defaults to `$HOME/.config/sym/config.yml`.\nCurrently, this does NOT do any kind of validation or communication with the rest of the platform.\nThis location can be tweaked by editing the `XDG_CONFIG_HOME` environment variable (replaces `$HOME/.config`).\n\n### Resources\n\n`sym resources`\n\nOnce you run `sym login`, you can see the resource groups available by running `sym resources`.\n\nCurrently, this is based on a hard-coded list of resource groups defined in params.py. If logged in using a sym email address, then\nthere will be exactly one resource available: `test`.\n\n### SSH\n\n`sym ssh RESOURCE INSTANCE`\n\nInitializes an SSH connection to an instance in the resource group.\n\n`sym ssh test i-01073e9d0438334fc`\n\nCreates an SSH connection to an instance `i-01073e9d0438334fc`. In order to create this connection, Sym first attempts a login via SAML\nusing `saml2aws` (or `aws-okta` as a fallback) for the currently logged in user (the email address in `config.yml` set via `sym login`).\nThis may require MFA.\n\n`sym --saml-client=aws-profile ssh PROFILE INSTANCE`\n\n### Write Creds\n\n`sym write-creds test --profile PROFILE`\n\nIt can be convenient to save temporary credentials for a sym resource into an AWS profile. Then the AWS profile can be used for other commands\n(with `sym` or other tools).\n\n### Exec\n\n`sym exec test -- COMMAND`\n\nYou can use `sym` to execute a command or script using the credentials for the resource group.\n\nSimilar to other commands, you can use an AWS profile instead of a sym resource group:\n\n`sym --saml-client=aws-profile exec PROFILE -- COMMAND`\n\n### Ansible Playbook\n\n`sym ansible-playbook test -i ec2.py docker_test.yml`\n\nThere are several useful environment variables that can help with debugging:\n* `SYM_LOG_DIR`: Set to a directory (i.e. `/tmp/sym/test`) to accumulate logs from sym commands.\n* `SYM_DEBUG`: Set to `true` to turn on verbose logging from ansible and ssh\n\nLike other commands, you can use an AWS profile instead of a sym resource group:\n\n`sym --saml-client=aws-profile ansible-playbook PROFILE -i ec2.py docker_test.yml`\n\n#### Send Command\n\nAs of 0.0.45, the default implementation for Ansible to communicate with EC2 instances is via SSM using\nsend command. To do this, we ship an implementation of ansible's connection API in our Sym CLI, and that location\nis provided as a connection plugin argument to ansible. We provide options to that plugin implementation to\nmanage the connection and associated dependencies (s3 bucket for copying files over to the instance, etc).\n\nThis behavior can be enabled/disabled with a flag: `--send-command/--no-send-command`. `--send-command` is not required\nsince it is the default. Alternatively it can be toggled using the `SYM_SEND_COMMAND` environment variable.\n\n#### SSH\n\nWhen send command is _not_ used, then ansible falls back to the normal behavior - initiating an SSM session and then\nopening an SSH tunnel with that session. When using SSH with `sym ansible-playbook`, sym will force ansible to use\nopenssh instead of a built-in `Paramiko` implementation that is sometimes used, but was found to be buggy with SSM.\n\nWhen using SSH, ansible needs to decide whether to persist SSH sessions, which is important for performance, but on some\nversions of OpenSSH and aws-cli can be unreliable. The mechanism for persisting sessions is SSH control master\npersistence. Sym has the following behavior:\n* If the version of OpenSSH on the local machine is lower than a min version (currently 8.1+), then it will disable control master\nby default; otherwise, it will enable it by default.\n* Control master can be explicitly enabled/disabled with the `--control-master/--no-control-master` flag, or the `SYM_USE_CONTROL_MASTER` env var.\n* Control master (and compression) will be automatically disabled if `SYM_DEBUG` or `--debug` are set.\n\n### Doctor\n\n`sym doctor test --mode=ansible --inventory=test/integration/docker-ansible-ld/sym/ec2.py`\n\nUse `doctor` to run checks against the current environment and collect all the logs (sym, ansible,\nssh, etc.) from the local environment and remote instances.\n",
    'author': 'SymOps, Inc.',
    'author_email': 'pypi@symops.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/symopsio/sym-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
