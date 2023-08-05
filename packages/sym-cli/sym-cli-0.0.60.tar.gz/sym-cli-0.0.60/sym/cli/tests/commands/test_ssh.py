from datetime import timedelta

import pytest
from expects import *

from sym.cli.errors import AccessDenied, SuppressedError
from sym.cli.helpers.config import Config
from sym.cli.helpers.ssh import maybe_gen_ssh_key, ssh_key_and_config
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.helpers.sandbox import Sandbox

INSTANCE_ID = "123"
IP_ADDRESS = "127.0.0.1"


def describe_instances_stub(make_stub):
    ec2 = make_stub("ec2")
    ec2.add_response(
        "describe_instances",
        {"Reservations": [{"Instances": [{"InstanceId": INSTANCE_ID}]}]},
    )


def send_command_stub(make_stub, command_id):
    ssm = make_stub("ssm")
    ssm.add_response(
        "send_command",
        {"Command": {"CommandId": command_id, "Status": "Pending"}},
    )
    ssm.add_response(
        "get_command_invocation",
        {"CommandId": command_id, "Status": "Success"},
        {"CommandId": command_id, "InstanceId": INSTANCE_ID},
    )


@pytest.fixture
def ssh_tester(
    command_tester,
    saml_client: SAMLClient,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
):
    def setup():
        sandbox.link_binary("ssh-keygen")
        capture_command.allow_call("ssh-keygen")

    def teardown():
        for conf in ssh_key_and_config(saml_client):
            expect(conf.path.exists()).to(be_true)

    return command_tester(["ssh", "test", IP_ADDRESS], setup=setup, teardown=teardown)


def test_ssh(ssh_tester, capture_command: CaptureCommand):
    def setup(make_stub):
        describe_instances_stub(make_stub)

    with ssh_tester(setup=setup):
        capture_command.assert_command(
            ["exec", "true"],
            ["ssh-keygen"],
            ["ssh", INSTANCE_ID, "-o BatchMode=yes"],
            ["ssh", INSTANCE_ID],
        )


def test_ssh_with_key(
    ssh_tester, saml_client: SAMLClient, capture_command: CaptureCommand
):
    def setup(make_stub):
        describe_instances_stub(make_stub)
        maybe_gen_ssh_key(saml_client)

    with ssh_tester(setup=setup):
        capture_command.assert_command(
            ["exec", "true"],
            ["ssh", INSTANCE_ID, "-o BatchMode=yes"],
            ["ssh", INSTANCE_ID],
        )


def test_ssh_needs_put(uuid, ssh_tester, capture_command: CaptureCommand):
    def setup(make_stub):
        describe_instances_stub(make_stub)
        send_command_stub(make_stub, str(uuid))

        capture_command.register_output(
            r"BatchMode",
            "Permission denied (publickey)",
            exit_code=255,
        )

    with ssh_tester(setup=setup):
        capture_command.assert_command(
            ["exec", "true"],
            ["ssh-keygen"],
            ["ssh", INSTANCE_ID, "-o BatchMode=yes"],
            ["ssh", INSTANCE_ID],
        )


def test_ssh_unknown_error(ssh_tester, capture_command: CaptureCommand):
    def setup(make_stub):
        describe_instances_stub(make_stub)

        capture_command.register_output(
            r"BatchMode",
            "Random Error",
            exit_code=255,
        )

    with ssh_tester(setup=setup, exception=SuppressedError) as result:
        capture_command.assert_command(
            ["exec", "true"],
            ["ssh-keygen"],
            ["ssh", INSTANCE_ID, "-o BatchMode=yes"],
        )

        expect(result.output).to(equal("Random Error"))


def test_ssh_with_key_and_instance(
    ssh_tester, saml_client: SAMLClient, capture_command: CaptureCommand
):
    def setup(_make_stub):
        Config.touch_instance(INSTANCE_ID)
        Config.add_instance_alias(INSTANCE_ID, alias=IP_ADDRESS, region="us-east-1")
        maybe_gen_ssh_key(saml_client)

    with ssh_tester(setup=setup):
        capture_command.assert_command(
            ["exec", "true"],
            ["ssh", INSTANCE_ID],
        )


def test_ssh_with_connection_closed(
    ssh_tester,
    saml_client: SAMLClient,
    capture_command: CaptureCommand,
):
    def setup(_make_stub):
        Config.touch_instance(INSTANCE_ID)
        Config.add_instance_alias(INSTANCE_ID, alias=IP_ADDRESS, region="us-east-1")
        maybe_gen_ssh_key(saml_client)

        capture_command.register_output(
            r"ssh",
            f"Connection to {INSTANCE_ID} closed",
            exit_code=255,
        )

    with ssh_tester(setup=setup, exception=SuppressedError) as result:
        capture_command.assert_command(
            ["exec", "true"],
            ["ssh", INSTANCE_ID],
        )
        expect(result.output).to(equal(f"Connection to {INSTANCE_ID} closed\n"))
        expect(Config.check_instance_ttl(INSTANCE_ID, timedelta(minutes=1))).to(be_true)


def test_ssh_with_target_not_connected(
    ssh_tester,
    saml_client: SAMLClient,
    capture_command: CaptureCommand,
):
    def setup(_make_stub):
        Config.touch_instance(INSTANCE_ID)
        Config.add_instance_alias(INSTANCE_ID, alias=IP_ADDRESS, region="us-east-1")
        maybe_gen_ssh_key(saml_client)

        capture_command.register_output(
            r"ssh",
            f"AccessDeniedException",
            exit_code=255,
        )

    with ssh_tester(setup=setup, exception=AccessDenied) as result:
        capture_command.assert_command(
            ["exec", "true"],
            ["ssh", INSTANCE_ID],
        )
        expect(result.output).to(contain("don't have access"))
        expect(Config.check_instance_ttl(INSTANCE_ID, timedelta(minutes=1))).to(be_false)


def test_ssh_no_login(command_login_tester):
    command_login_tester(["ssh", "test", "127.0.0.1"])
    command_login_tester(["ssh", "test", "127.0.0.1", "foo", "bar", "baz"])
    command_login_tester(["ssh", "127.0.0.1"])
    command_login_tester(["ssh", "127.0.0.1"], {"SYM_RESOURCE": "test"})
    command_login_tester(["ssh", "127.0.0.1"], {"ENVIRONMENT": "test"})
