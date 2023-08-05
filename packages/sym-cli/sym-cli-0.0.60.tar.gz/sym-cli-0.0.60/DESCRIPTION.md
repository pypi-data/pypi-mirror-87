# sym-cli

Sym CLI

## Usage

### Login

`sym login --email rick@symops.io --org sym`

Or, to run interactively: `sym login`

Currently, this saves the email and org name to a local configuration file that defaults to `$HOME/.config/sym/config.yml`.
Currently, this does NOT do any kind of validation or communication with the rest of the platform.
This location can be tweaked by editing the `XDG_CONFIG_HOME` environment variable (replaces `$HOME/.config`).

### Resources

`sym resources`

Once you run `sym login`, you can see the resource groups available by running `sym resources`.

Currently, this is based on a hard-coded list of resource groups defined in params.py. If logged in using a sym email address, then
there will be exactly one resource available: `test`.

### SSH

`sym ssh RESOURCE INSTANCE`

Initializes an SSH connection to an instance in the resource group.

`sym ssh test i-01073e9d0438334fc`

Creates an SSH connection to an instance `i-01073e9d0438334fc`. In order to create this connection, Sym first attempts a login via SAML
using `saml2aws` (or `aws-okta` as a fallback) for the currently logged in user (the email address in `config.yml` set via `sym login`).
This may require MFA.

`sym --saml-client=aws-profile ssh PROFILE INSTANCE`

### Write Creds

`sym write-creds test --profile PROFILE`

It can be convenient to save temporary credentials for a sym resource into an AWS profile. Then the AWS profile can be used for other commands
(with `sym` or other tools).

### Exec

`sym exec test -- COMMAND`

You can use `sym` to execute a command or script using the credentials for the resource group.

Similar to other commands, you can use an AWS profile instead of a sym resource group:

`sym --saml-client=aws-profile exec PROFILE -- COMMAND`

### Ansible Playbook

`sym ansible-playbook test -i ec2.py docker_test.yml`

There are several useful environment variables that can help with debugging:
* `SYM_LOG_DIR`: Set to a directory (i.e. `/tmp/sym/test`) to accumulate logs from sym commands.
* `SYM_DEBUG`: Set to `true` to turn on verbose logging from ansible and ssh

Like other commands, you can use an AWS profile instead of a sym resource group:

`sym --saml-client=aws-profile ansible-playbook PROFILE -i ec2.py docker_test.yml`

#### Send Command

As of 0.0.45, the default implementation for Ansible to communicate with EC2 instances is via SSM using
send command. To do this, we ship an implementation of ansible's connection API in our Sym CLI, and that location
is provided as a connection plugin argument to ansible. We provide options to that plugin implementation to
manage the connection and associated dependencies (s3 bucket for copying files over to the instance, etc).

This behavior can be enabled/disabled with a flag: `--send-command/--no-send-command`. `--send-command` is not required
since it is the default. Alternatively it can be toggled using the `SYM_SEND_COMMAND` environment variable.

#### SSH

When send command is _not_ used, then ansible falls back to the normal behavior - initiating an SSM session and then
opening an SSH tunnel with that session. When using SSH with `sym ansible-playbook`, sym will force ansible to use
openssh instead of a built-in `Paramiko` implementation that is sometimes used, but was found to be buggy with SSM.

When using SSH, ansible needs to decide whether to persist SSH sessions, which is important for performance, but on some
versions of OpenSSH and aws-cli can be unreliable. The mechanism for persisting sessions is SSH control master
persistence. Sym has the following behavior:
* If the version of OpenSSH on the local machine is lower than a min version (currently 8.1+), then it will disable control master
by default; otherwise, it will enable it by default.
* Control master can be explicitly enabled/disabled with the `--control-master/--no-control-master` flag, or the `SYM_USE_CONTROL_MASTER` env var.
* Control master (and compression) will be automatically disabled if `SYM_DEBUG` or `--debug` are set.

### Doctor

`sym doctor test --mode=ansible --inventory=test/integration/docker-ansible-ld/sym/ec2.py`

Use `doctor` to run checks against the current environment and collect all the logs (sym, ansible,
ssh, etc.) from the local environment and remote instances.
